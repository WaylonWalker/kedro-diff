## Unreleased
_Currently a Work in Progress, Check back soon for an official release_

please note that some of what is currently shown in the readme is (readme driven development)  They are upcoming features to the project.

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

## Roadmap

### 1.0.0

- [x] commit parser
- [x] get `pipeline.to_json()` for `__default__` for two different commits
- [x] get `pipeline.to_json()` for all pipelines for two different commits
- [x] --stat compares the number of nodes added or dropped in `__default__`
- [x] --stat compares the number of nodes added or dropped in all pipelines
- [x] --stat compares attribute changes (inputs, outputs, tags) in all pipelines
- [x] compare input names
- [x] compare output names
- [ ] speed up getting repeat pipelines from the same commit (no need to reaload a new session)
- [ ] speed up getting repeat commits by checking commit hash (reuse existing json)
- [ ] minimize untested code

### 2.0.0

_super-size `pipeline.to_json()`_
- [x] compare all attributes on a node ( not just inputs, outputs, tags)
- [ ] allow users to specify custom to_json method
- [ ] function names
- [ ] function hashes
- [ ] catalog _filepath
- [ ] catalog _sql

## Testing

This project strives for 100% test coverage where it makes sense.  Other kedro
plugins I have created have suffered development speed by the complexity of
fully testing on a full kedro project. There are so many pieces to get into
place that it becomes difficult to test accross multiple versions of kedro or
keep the tests working as kedro changes.  Minimal functionality will be placed
into modules that require a kedro full kedro project in place to work.
