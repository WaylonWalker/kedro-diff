import json
from pathlib import Path

import pytest

from kedro_diff import KedroDiff
from kedro_diff.sample_data import create_simple_sample

DATA = Path(__file__).parent / "sample-data"

pipe_params = [
    {
        "name": "__default__",
        "pipe1": create_simple_sample(0),
        "pipe2": create_simple_sample(1),
        "expected_contains": ("M", "1", "__default__", "+"),
        "expected_not_contains": ("-", "++", "??", "data_engineering"),
    },
    {
        "name": "__default__",
        "pipe1": create_simple_sample(1),
        "pipe2": create_simple_sample(0),
        "expected_contains": ("M", "1", "__default__", "-"),
        "expected_not_contains": ("+", "--", "??", "data_engineering"),
    },
    {
        "name": "data_engineering",
        "pipe1": create_simple_sample(0),
        "pipe2": create_simple_sample(1),
        "expected_contains": ("M", "1", "data_engineering", "+"),
        "expected_not_contains": ("-", "++", "??", "__default__"),
    },
    {
        "name": "__default__",
        "pipe1": create_simple_sample(10, name_prefix="first"),
        "pipe2": create_simple_sample(10, name_prefix="second"),
        "expected_contains": ("M", "20", "__default__", "+" * 10, "-" * 10),
        "expected_not_contains": ("+" * 11, "-" * 11, "??", "data_engineering"),
    },
]


def load_pipes(*files):
    return (json.loads((DATA / file).read_text()) for file in files)


@pytest.mark.parametrize("params", pipe_params)
def test_diff_stat_msg(params):
    def run(name, pipe1, pipe2, expected_contains, expected_not_contains):
        res = KedroDiff(pipe1, pipe2, name=name)._stat_msg

        for expected in expected_contains:
            assert expected in res

        for not_expected in expected_not_contains:
            assert not_expected not in res

    run(**params)


@pytest.mark.parametrize("params", pipe_params)
def test_diff_stat(capsys, params):
    def run(name, pipe1, pipe2, expected_contains, expected_not_contains):
        KedroDiff(pipe1, pipe2, name=name).stat()
        capture = capsys.readouterr()
        assert capture.err == ""

        res = capture.out

        for expected in expected_contains:
            assert expected in res

        for not_expected in expected_not_contains:
            assert not_expected not in res

    run(**params)
