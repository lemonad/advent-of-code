Day 6: Custom Customs
================
Jonas Nockert (@lemonad)

I’m using R for this year’s Advent of Code. Learning as I go, which is
quite obvious here : )

It seems the biggest problem of part one is the grouping with empty
lines. Especially since I struggle with parsing in R, it always seem to
result in much more code than I initially expect.

``` r
lines <- read_file("input/december06.input")
lines %>%
  str_split("\\n\\n") %>%
  unlist() %>%
  lapply(function(x) {
    str_replace_all(x, "\\n", "") %>%
    str_split("") %>%
    unlist() %>%
    unique %>%
    length
  }) %>%
  reduce(sum)
```

    ## [1] 6625

Okay, that’s quite readable but, still, it’s basically trial and error
with the `unlist`’s.

## Part two

Uh oh, there’s not much to reuse from part one here.

``` r
lines %>%
  str_split("\\n\\n") %>%
  unlist() %>%
  str_split("\\n") %>%
  lapply(
    function(x) {
      str_split(x, "") %>%
      reduce(intersect) %>%
      length()
    }
  ) %>%
  unlist() %>%
  sum()
```

    ## [1] 3354

Hm, not the right answer (but someone else’s answer so I’m assuming it
is pretty close). Let’s investigate…

``` r
lines %>%
  str_split("\\n\\n") %>%
  unlist() %>%
  str_split("\\n") %>%
  tail(n = 2)
```

    ## [[1]]
    ## [1] "ljamgiu"    "giumrlenkh" "ismuglp"    "ugmlsi"     "auiomgslf" 
    ## 
    ## [[2]]
    ## [1] "tibudoa"   "obuatifgp" ""

Aha, so the intersection of the last set of strings is "", I guess there
is some new line at the end.

``` r
lines %>%
  str_split("\\n\\n") %>%
  unlist() %>%
  .[str_detect(., "\\n$")]
```

    ## [1] "tibudoa\nobuatifgp\n"

Yes, there’s only one trailing newline and it’s on the very last line.
Gah, I’ve forgotten to trim whitespace when reading the input. Let’s try
this again:

``` r
lines <- trimws(read_file("input/december06.input"))
lines %>%
  str_split("\\n\\n") %>%
  unlist() %>%
  str_split("\\n") %>%
  lapply(
    function(x) {
      str_split(x, "") %>%
      reduce(intersect) %>%
      length()
    }
  ) %>%
  unlist() %>%
  sum()
```

    ## [1] 3360

That did the trick : )
