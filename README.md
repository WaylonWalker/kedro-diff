# kedro-diff

kedro diff aims to be a familiar interface into comparing two points in history.  Git diffs are fantastic tools but often are too granular to see what has changed inside the pipeline.  `kedro diff` aims to be a familiar tool at a higher level so we can see changes to nodes (names, inputs, outputs, tags).

## Example

``` diff
kedro diff --stat develop..master
M  __default__      | 6 ++++-
M  data_science     | 3 +++
M  data_engineering | 3 ++-
?? new_pipeline

4 pipelines changed, 5 insertions(+), 4 deletions(-)
```

## Usage

``` diff
# diff develop into master
kedro diff develop..master

kedro diff develop master

# diff current state with main
kedro diff main

# diff current state with main
kedro diff ..main

# comparing pipelines from two branches
kedro diff master new_branch data_science
```

## More examples

``` diff
kedro diff develop..master
╭──────────────────────────────────────────────────────────────────────────────╮
│ modified: data_engineering                                                   │
╰──────────────────────────────────────────────────────────────────────────────╯
+ strip_whitespace
+ lowercase_columns
+ get_trains
- get_tains
╭──────────────────────────────────────────────────────────────────────────────╮
│ modified: data_science                                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
+ split_data
```
