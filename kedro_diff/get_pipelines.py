"""get_pipelines.

Get json from a specific commit
"""
import json
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
    for item in os.listdir(str(src)):
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
        meta_path = (
            Path()
            / ".kedro-diff"
            / (commit.replace("/", "_") + "-commit-metadata.json")
        ).absolute()
        meta_path.parent.mkdir(exist_ok=True)
        subprocess.call(f"git checkout {commit} --quiet", shell=True, cwd=tmpdirname)

        subprocess.call(
            f"kedro get-json --meta --output {meta_path} --quiet --commit {commit}",
            shell=True,
            cwd=tmpdirname,
        )

        meta = json.loads(meta_path.read_text())
        for pipeline in meta["pipelines"]:
            pipeline_path = (
                Path()
                / ".kedro-diff"
                / ("_".join([commit, pipeline]).replace("/", "_") + ".json")
            ).absolute()
            subprocess.call(
                f"kedro get-json --output {pipeline_path} --pipeline-name {pipeline} --quiet",
                shell=True,
                cwd=tmpdirname,
            )


if __name__ == "__main__":
    import sys

    to_json(sys.argv[1], sys.argv[2])
