Day 4: Passport Processing
================
Jonas Nockert (@lemonad)

I’m using R for this year’s Advent of Code. Learning as I go, which is
quite obvious here : )

Parsing is still trial and error for me in R so let’s begin with the
simple example we are given.

``` r
example_input <- trimws("
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
")
```

It would be nice if one could get that to a list of key value pairs, one
per passport \[…30 minutes later\]:

``` r
parse_passports <- function(str) {
  str %>%
    # Separate passports.
    str_split("\n\n") %>%
    unlist() %>%
    # Separate pairs in the passport.
    str_split("[ \n]+") %>%
    # Separate `key:value` into two list elements.
    lapply(str_split, pattern = ":") %>%
    # Transform elements into key value pairs.
    map(
      function(passport) {
        set_names(
          passport %>% map(2),
          passport %>% map(1)
        )
      }
    )
}
```

Lets try it out on the example by looking at the first passport:

``` r
parse_passports(example_input) %>% map(1)
```

    ## [[1]]
    ## [1] "gry"
    ## 
    ## [[2]]
    ## [1] "2013"
    ## 
    ## [[3]]
    ## [1] "#ae17e1"
    ## 
    ## [[4]]
    ## [1] "#cfa07d"

Seems ok. It’s quite possible that a valid passport is just one with 8
pairs (or 7 if North Pole Credentials instead of a passport). However,
we have key value pairs so we should be able to simply check that all
required fields (excluding `cid`) exists:

``` r
n_valid <- function(passports) {
  passports %>%
    map(
      function(x) {
        all(c("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid") %in% names(x))
      }
    ) %>%
    unlist() %>%
    sum()
}
```

Let’s try it out on the example input. We’re expecting it to contain two
valid passports:

``` r
example_passports <- parse_passports(example_input)
n_valid(example_passports)
```

    ## [1] 2

Without further ado:

``` r
passports <- parse_passports(trimws(read_file("./input/december04.input")))
n_valid(passports)
```

    ## [1] 245

### Part two

Ah, validation. I know what I want to do but not how to do it. The rules
seem simple enough though:

``` r
validate_year <- function(value, range) {
  str_detect(value, "^\\d{4}$") && as.integer(value) %in% range
}

validate_height <- function(value) {
  m <- str_match(value, "^(\\d+)(cm|in)$")
  !is.na(m[1]) && (
    (m[3] == "in" && m[2] %in% 59:76) ||
      (m[3] == "cm" && m[2] %in% 150:193)
  )
}

validate_hair_color <- function(value) {
  str_detect(value, "^#[0-9a-f]{6}$")
}

validate_eye_color <- function(value) {
  str_detect(value, "^(amb|blu|brn|gry|grn|hzl|oth)$")
}

validate_password_id <- function(value) {
  str_detect(value, "^[0-9]{9}$")
}
```

Let’s run some quick tests:

``` r
all(
  validate_year("1994", 1990:2000),
  !validate_year("1994", 1995:2000),
  !validate_year("abc", 1995:2000),
  validate_height("180cm"),
  validate_height("70in"),
  !validate_height("200cm"),
  !validate_height("20in"),
  validate_hair_color("#123abc"),
  !validate_hair_color("#xyz123"),
  !validate_hair_color("123abc"),
  validate_eye_color("blu"),
  !validate_eye_color("green"),
  validate_password_id("000000001"),
  !validate_password_id("1")
)
```

    ## [1] TRUE

All tests pass so next up is figuring out how to apply validation. I’m
thinking that the validation step could just remove all the pairs that
are invalid so we can re-use the previously defined `valid` function:

``` r
validated_pairs <- function(pairs) {
    valid <- keep(
      names(pairs),
      function(y) {
        case_when(
          y == "byr" ~ validate_year(pairs[[y]], 1920:2002),
          y == "iyr" ~ validate_year(pairs[[y]], 2010:2020),
          y == "eyr" ~ validate_year(pairs[[y]], 2020:2030),
          y == "hgt" ~ validate_height(pairs[[y]]),
          y == "hcl" ~ validate_hair_color(pairs[[y]]),
          y == "ecl" ~ validate_eye_color(pairs[[y]]),
          y == "pid" ~ validate_password_id(pairs[[y]]),
          TRUE ~ FALSE
        )
      }
    )
    # Return only valid pairs.
    pairs[valid]
}
```

Using this on the example input should give, hm, two valid passports..?

``` r
# Aha, we can use point-free style _and_ pipes with the functions above!
example_passports %>% lapply(validated_pairs) %>% n_valid()
```

    ## [1] 2

Okay, but how many passports are valid now? Should be less than the 245
above:

``` r
passports %>% lapply(validated_pairs) %>% n_valid()
```

    ## [1] 133

I went through the list of invalid pairs, half-expecting to see
something fun but… nothing. I’ll say this though — out of 292 passports,
only 133 were valid — I think putting a little quality control on the
wish list would be in order :)
