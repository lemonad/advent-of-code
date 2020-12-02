Day 2: Password Philosophy
================
Jonas Nockert (@lemonad)

I’m using R for this year’s Advent of Code. Learning as I go, which is
quite obvious here : )

``` r
lines <- read_lines("./input/december02.input")
lines %>% head(n = 3)
```

    ## [1] "13-15 c: cqbhncccjsncqcc" "2-3 v: zvdvfd"           
    ## [3] "9-14 b: rbrbnbbbqdfrht"

``` r
lines %>% tail(n = 3)
```

    ## [1] "2-9 t: cntttttcgtttt"    "5-6 r: rrrrbh"          
    ## [3] "10-12 j: jjjjjjjjjzjjdj"

``` r
matches <- lines %>%
  str_match("^(\\d+)\\-(\\d+) ([a-z]): ([a-z]+)") %>%
  as_tibble() %>%
  transmute(
    low = as.integer(V2),
    high = as.integer(V3),
    c = V4,
    password = V5
  )
```

    ## Warning: The `x` argument of `as_tibble.matrix()` must have unique column names if `.name_repair` is omitted as of tibble 2.0.0.
    ## Using compatibility `.name_repair`.
    ## This warning is displayed once every 8 hours.
    ## Call `lifecycle::last_warnings()` to see where this warning was generated.

``` r
n_valid <- str_count(matches$password, fixed(matches$c)) %>% {
  . >= matches$low & . <= matches$high
  } %>%
  sum()
```

There are 410 valid passwords (for the sled rental place down the
street).

``` r
n_actually_valid <- xor(
  str_sub(matches$password, matches$low, matches$low) == matches$c,
  str_sub(matches$password, matches$high, matches$high) == matches$c
) %>%
  sum()
```

There are 694 valid passwords for the Official Toboggan Corporate
Authentication System.
