"""Commit Parser.

Parses user input into two commits to compare
"""
import logging
from more_itertools import flatten
from kedro_diff.errors import KedroDiffError

__version__ = "0.0.0"


from typing import Union, Tuple


def parse_commit(commit: Union[str, Tuple[str, ...]]) -> Tuple[str, str]:
    """
    Parses input commit into two commits for comparing.

    Exampe:
    parse_commit('develop..main')

    """
    # split commits in case of `kedro diff main..branch`
    if isinstance(commit, str):
        if "..." in commit:
            return parse_commit(tuple(commit.split("...")))
        return parse_commit(tuple(commit.split("..")))
    else:
        if "..." in str(commit):
            return parse_commit(list(flatten([c.split("...") for c in commit])))
        if ".." in str(commit):
            return parse_commit(list(flatten([c.split("..") for c in commit])))

    if len(commit) == 0:
        raise KedroDiffError(
            f"at least one commit must be passed to compare\n recieved {commit}"
        )
    if len(commit) > 2:
        raise KedroDiffError(
            f"no more than 2 commits may be compared\n recieved {commit}"
        )

    if len(commit) == 2:
        commit1 = commit[0]
        commit2 = commit[1]

    # set to HEAD in case of `kedro diff branch`
    # if len(commit) == 1:
    else:
        commit1 = "HEAD"
        commit2 = commit[0]

    # overrite commit1 in cases of `kedro diff ..branch
    if commit1 == "":
        commit1 = "HEAD"
    if commit2 == "":
        raise KedroDiffError(
            f"at least one commit must be passed to compare\n recieved {commit}"
        )
    logger = logging.getLogger(__name__)
    logger.info(f"comparing {commit1} to {commit2}")

    return commit1, commit2


if __name__ == "__main__":
    import sys

    print(sys.argv[1:])
    print(parse_commit(sys.argv[1:]))