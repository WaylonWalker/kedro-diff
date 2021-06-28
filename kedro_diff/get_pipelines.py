"""get_pipelines.

Get json from a specific commit
"""
import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Optional, Union


def copytree(
    src: Union[str, Path],
    dst: Union[str, Path],
    symlinks: bool = False,
    ignore: Optional[Callable] = None,
) -> None:
    """Copy src director into dst directory."""
    ignore_items = [
        ".envrc",
        ".venv",
        ".kedro-diff",
    ]
    items = [item for item in os.listdir(str(src)) if item not in ignore_items]

    for item in items:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def to_json(project_path: Union[str, Path], commit: str, verbose: int = 0) -> None:
    """Get json from specific commit."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        logger = get_logger(verbose=verbose)
        logger.info(f"copying {project_path} into {tmpdirname}")
        copytree(project_path, tmpdirname)
        subprocess.call(
            f'git checkout "{commit}" --force --quiet', shell=True, cwd=tmpdirname
        )

        pipeline_path = (Path() / ".kedro-diff").absolute()
        subprocess.call(
            f"kedro get-json --output '{pipeline_path}' --commit '{commit}' --quiet",
            shell=True,
            cwd=tmpdirname,
        )


if __name__ == "__main__":
    import sys

    to_json(sys.argv[1], sys.argv[2])
