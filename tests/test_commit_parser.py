"""
Test commit parser.
"""
from kedro_diff.commit_parser import parse_commit
from kedro_diff.errors import KedroDiffError
import pytest


@pytest.mark.parametrize(
    "commit,expected",
    [
        (("master", "main"), ("master", "main")),
        (("main", "master"), ("main", "master")),
        (("master", "develop"), ("master", "develop")),
        (("master", "develop/new-feat"), ("master", "develop/new-feat")),
        ("master..main", ("master", "main")),
        ("master...main", ("master", "main")),
        (("master...main",), ("master", "main")),
        (("master..main",), ("master", "main")),
        (("..main",), ("HEAD", "main")),
        (("...main",), ("HEAD", "main")),
        (("main",), ("HEAD", "main")),
        ("master...develop/new-feat", ("master", "develop/new-feat")),
        ("main", ("HEAD", "main")),
        ("develop/new-feat", ("HEAD", "develop/new-feat")),
        ("..develop/new-feat", ("HEAD", "develop/new-feat")),
        (("main", "master", "develop"), KedroDiffError),
        (("main..master..develop"), KedroDiffError),
        (("main..master..develop..mine..yours..ours..thiers"), KedroDiffError),
        ((), KedroDiffError),
        ((""), KedroDiffError),
        # pytest.param(("master", "main", "develop"), 42, marks=pytest.mark.xfail),
    ],
)
def test_parse(commit, expected):
    """
    Test Commit input is parsed as expected.
    """
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected):
            commit1, commit2 = parse_commit(commit)
    else:
        commit1, commit2 = parse_commit(commit)
        assert commit1 == expected[0]
        assert commit2 == expected[1]
