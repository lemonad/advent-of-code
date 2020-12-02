Day 1: Report Repair
================
Jonas Nockert (@lemonad)

I’m using R for this year’s Advent of Code. Learning as I go, which is
quite obvious here : )

``` r
lines <- read_lines("./input/december01.input") %>%
  parse_number() %>%
  sort()

lines %>% head()
```

    ## [1] 389 399 456 496 764 766

``` r
lines %>% tail()
```

    ## [1] 1983 1989 1993 1999 2005 2006

Find all pairs of numbers that sum to &lt;= 2020 and store as a list of
`c(num1 + num2, num1, num2)` lists:

``` r
up_to_2020 <- map(
  rev(lines),
  function(x) {
    which((lines < x) & (lines + x <= 2020)) %>%
      map(function(y) c(x + lines[y], x, lines[y]))
  }
) %>%
  flatten()

up_to_2020 %>% head(3)
```

    ## [[1]]
    ## [1] 2019 1630  389
    ## 
    ## [[2]]
    ## [1] 2016 1627  389
    ## 
    ## [[3]]
    ## [1] 1999 1610  389

Out of all pairs summing to &lt;= 2020, which pair sums to exactly 2020?
Compute its product.

``` r
pair_2020 <- up_to_2020[map(up_to_2020, 1) == 2020] %>%
  head(1) %>%
  unlist() %>%
  tail(2)
```

Numbers 1564 and 456 sum to 2020 and their product is 713184.

Now, use the pairs above in order to find triples that sum to 2020:

``` r
triple_2020 <- map(
  up_to_2020,
  function(x) {
    which((lines < x[1]) & (lines + x[1] == 2020)) %>%
      map(function(y) c(lines[y], x[2], x[3]))
  }
) %>%
  flatten() %>%
  head(1) %>%
  unlist()
```

Numbers 764, 857, and 399 sum to 2020 and their product is 261244452.
