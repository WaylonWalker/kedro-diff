import json
from pathlib import Path

import pytest

from kedro_diff import KedroDiff

DATA = Path(__file__).parent / "sample-data"

pipe_params = [
    {
        "name": "__default__",
        "pipe1_file": "empty.json",
        "pipe2_file": "one-node.json",
        "expected_contains": ("M", "1", "__default__", "+"),
        "expected_not_contains": ("-", "++", "??", "data_engineering"),
    },
    {
        "name": "data_engineering",
        "pipe1_file": "empty.json",
        "pipe2_file": "one-node.json",
        "expected_contains": ("M", "1", "data_engineering", "+"),
        "expected_not_contains": ("-", "++", "??", "__default__"),
    },
]


def load_pipes(*files):
    return (json.loads((DATA / file).read_text()) for file in files)


@pytest.mark.parametrize("params", pipe_params)
def test_diff_stat_msg(params):
    def run(name, pipe1_file, pipe2_file, expected_contains, expected_not_contains):
        pipe1, pipe2 = load_pipes(pipe1_file, pipe2_file)
        res = KedroDiff(pipe1, pipe2, name=name)._stat_msg

        for expected in expected_contains:
            assert expected in res

        for not_expected in expected_not_contains:
            assert not_expected not in res

    run(**params)


@pytest.mark.parametrize("params", pipe_params)
def test_diff_stat(capsys, params):
    def run(name, pipe1_file, pipe2_file, expected_contains, expected_not_contains):
        pipe1, pipe2 = load_pipes(pipe1_file, pipe2_file)
        KedroDiff(pipe1, pipe2, name=name).stat()
        capture = capsys.readouterr()
        assert capture.err == ""

        res = capture.out

        for expected in expected_contains:
            assert expected in res

        for not_expected in expected_not_contains:
            assert not_expected not in res

    run(**params)
