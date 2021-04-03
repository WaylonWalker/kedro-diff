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
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def to_json(project_path: Union[str, Path], commit: str, verbose: int = 0) -> None:
    """Get json from specific commit."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        if verbose < 1:
            logger.setLevel(logging.ERROR)
        logger.info(f"copying {project_path} into {tmpdirname}")
        copytree(project_path, tmpdirname)
        path = (Path() / ".kedro-diff" / (commit + ".json")).absolute()
        path.parent.mkdir(exist_ok=True)
        subprocess.call(f"git checkout {commit} --quiet", shell=True, cwd=tmpdirname)
        subprocess.call(
            f"kedro get-json --output {path} --quiet", shell=True, cwd=tmpdirname
        )


if __name__ == "__main__":
    import sys

    to_json(sys.argv[1], sys.argv[2])
