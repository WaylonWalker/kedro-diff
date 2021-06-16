"""Commit Parser.

Parses user input into two commits to compare
"""
import subprocess
import json
import logging
from pathlib import Path
from typing import Dict, Tuple, Union

from more_itertools import flatten

from kedro_diff.errors import KedroDiffError, RevParseError

__version__ = "0.0.0"


def get_full_sha(commit):
    proc = subprocess.Popen(
        ["git", "rev-parse", commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    status = proc.wait()
    if status != 0:
        raise RevParseError(proc.stderr.read())
    sha = proc.stdout.read().decode("utf-8").replace("\n", "")
    return sha


def parse_commit(
    commit: Union[str, Tuple[str, ...]], verbose: int = 0, full_sha: bool = True
) -> Tuple[str, str]:
    """
    Parse input commit into two commits for comparing.

    Exampe:
    parse_commit('develop..main')

    """
    # split commits in case of `kedro diff main..branch`
    if isinstance(commit, str):
        if "..." in commit:
            return parse_commit(
                tuple(commit.split("...")), verbose=verbose, full_sha=full_sha
            )
        return parse_commit(
            tuple(commit.split("..")), verbose=verbose, full_sha=full_sha
        )
    else:
        if "..." in str(commit):
            return parse_commit(
                tuple(flatten([c.split("...") for c in commit])),
                verbose=verbose,
                full_sha=full_sha,
            )
        if ".." in str(commit):
            return parse_commit(
                tuple(flatten([c.split("..") for c in commit])),
                verbose=verbose,
                full_sha=full_sha,
            )

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
    if verbose < 1:
        logger.setLevel(logging.ERROR)
    logger.info(f"comparing {commit1} to {commit2}")

    if full_sha:
        sha1 = get_full_sha(commit1)
        sha2 = get_full_sha(commit2)
        return sha1, sha2

    return commit1, commit2


def load_commit_metadata(
    commit: Union[str, Tuple[str, ...]],
    verbose: int = 0,
    root_dir: Union[str, Path] = ".",
    full_sha: bool = True,
) -> Tuple[Dict, Dict]:
    commit1, commit2 = parse_commit(commit, verbose=verbose, full_sha=full_sha)
    meta1 = json.loads(
        (
            Path(root_dir)
            / ".kedro-diff"
            / (commit1.replace("/", "_").replace(" ", "_") + "-commit-metadata.json")
        )
        .absolute()
        .read_text()
    )
    meta2 = json.loads(
        (
            Path(root_dir)
            / ".kedro-diff"
            / (commit2.replace("/", "_").replace(" ", "_") + "-commit-metadata.json")
        )
        .absolute()
        .read_text()
    )
    return meta1, meta2


if __name__ == "__main__":
    import sys

    print(sys.argv[1:])
    print(parse_commit(tuple(sys.argv[1:])))
