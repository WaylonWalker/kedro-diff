import json

import pytest

from kedro_diff.commit_parser import load_commit_metadata


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "meta1": {
                "commit": "main",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                ],
            },
            "meta2": {
                "commit": "HEAD",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                    "twenty_nodes",
                ],
            },
        },
        {
            "meta1": {
                "commit": "main",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                ],
            },
            "meta2": {
                "commit": "hs0af0ahj",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                    "twenty_nodes",
                ],
            },
        },
        {
            "meta1": {
                "commit": "main",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                ],
            },
            "meta2": {
                "commit": "feat/new-nodes",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                    "twenty_nodes",
                ],
            },
        },
        {
            "meta1": {
                "commit": "main",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                ],
            },
            "meta2": {
                "commit": "feat/new.nodes",
                "sha": "hs0af0ahj",
                "pipelines": [
                    "__default__",
                    "ten_nodes",
                    "twenty_nodes",
                ],
            },
        },
    ],
)
def test_load_commit_metadata(tmpdir, runargs):
    def run(meta1, meta2):
        p = tmpdir.mkdir(".kedro-diff")
        meta_file1 = p.join(
            f"{meta1['commit'].replace('/', '_').replace(' ', '_')}-commit-metadata.json"
        )
        meta_file2 = p.join(
            f"{meta2['commit'].replace('/', '_').replace(' ', '_')}-commit-metadata.json"
        )
        meta_file1.write(json.dumps(meta1))
        meta_file2.write(json.dumps(meta2))
        load_commit_metadata(
            f"{meta1['commit']}..{meta2['commit']}", root_dir=tmpdir, full_sha=False
        )

    run(**runargs)
