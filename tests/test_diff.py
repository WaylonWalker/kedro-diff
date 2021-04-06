import json
from copy import deepcopy
from pathlib import Path

import pytest

from kedro_diff import KedroDiff
from kedro_diff.sample_data import create_simple_sample

DATA = Path(__file__).parent / "sample-data"

pipe10 = create_simple_sample(10)
pipe10_change_one_input = deepcopy(pipe10)
pipe10_change_one_input["pipeline"][2]["inputs"] = "input1"

pipe10_change_one_output = deepcopy(pipe10)
pipe10_change_one_output["pipeline"][2]["outputs"] = ["output1"]

pipe10_change_one_tag = deepcopy(pipe10)
pipe10_change_one_tag["pipeline"][2]["tags"] = ["tag1"]


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
    {
        "name": "__default__",
        "pipe1": pipe10,
        "pipe2": pipe10_change_one_input,
        "expected_contains": ("M", "2", "__default__", "+", "-"),
        "expected_not_contains": ("+" * 2, "-" * 2, "??", "data_engineering"),
    },
    {
        "name": "__default__",
        "pipe1": pipe10,
        "pipe2": pipe10_change_one_output,
        "expected_contains": ("M", "2", "__default__", "+", "-"),
        "expected_not_contains": ("+" * 2, "-" * 2, "??", "data_engineering"),
    },
    {
        "name": "__default__",
        "pipe1": pipe10,
        "pipe2": pipe10_change_one_tag,
        "expected_contains": ("M", "2", "__default__", "+", "-"),
        "expected_not_contains": ("+" * 2, "-" * 2, "??", "data_engineering"),
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


def test_diff_from_sample():
    diff = KedroDiff.from_sample({"num_nodes": 2}, {"num_nodes": 4})
    assert "__default__" in diff._stat_msg
    assert "++" in diff._stat_msg
    assert "+++" not in diff._stat_msg
    assert "-" not in diff._stat_msg
