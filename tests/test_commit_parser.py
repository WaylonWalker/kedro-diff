"""Test commit parser."""

import pytest

from kedro_diff.commit_parser import parse_commit
from kedro_diff.errors import KedroDiffError


@pytest.mark.parametrize(
    "commit,expected",
    [
        (("master", "main"), ("master", "main")),
        (("main", "master"), ("main", "master")),
        (("master", "develop"), ("master", "develop")),
        (("master", "develop/new-feat"), ("master", "develop/new-feat")),
        (("master", "develop~2"), ("master", "develop~2")),
        (
            ("master", "1c96dd23af05edf42ae46251022e51b7"),
            ("master", "1c96dd23af05edf42ae46251022e51b7"),
        ),
        ("master..main", ("master", "main")),
        ("master...main", ("master", "main")),
        (("master...main",), ("master", "main")),
        (("master..main",), ("master", "main")),
        (
            ("master..1c96dd23af05edf42ae46251022e51b7",),
            ("master", "1c96dd23af05edf42ae46251022e51b7"),
        ),
        (("master..main~2",), ("master", "main~2")),
        (("..main",), ("HEAD", "main")),
        (("...main",), ("HEAD", "main")),
        (("main",), ("main", "HEAD")),
        (("main~2",), ("main~2", "HEAD")),
        ("master...develop/new-feat", ("master", "develop/new-feat")),
        ("main", ("main", "HEAD")),
        ("develop/new-feat", ("develop/new-feat", "HEAD")),
        ("..develop/new-feat", ("HEAD", "develop/new-feat")),
        (("main", "master", "develop"), KedroDiffError),
        (("main..master..develop"), KedroDiffError),
        (("main..master..develop..mine..yours..ours..thiers"), KedroDiffError),
        ((), KedroDiffError),
        ((""), KedroDiffError),
    ],
)
def test_parse(commit, expected):
    """Test Commit input is parsed as expected."""
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected):
            commit1, commit2 = parse_commit(commit)
    else:
        commit1, commit2 = parse_commit(commit)
        assert commit1 == expected[0]
        assert commit2 == expected[1]
