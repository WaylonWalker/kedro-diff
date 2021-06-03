"""kedro_diff cli module."""
import json
import logging
import subprocess
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Tuple

import click
from kedro.framework.session import KedroSession
from rich import print

from kedro_diff.diff import KedroDiff

from .sample_data import create_simple_sample

if TYPE_CHECKING:
    from kedro.framework.startup import ProjectMetadata

__version__ = "0.0.0"


def silent_loggers() -> None:
    """All logs need to be silent in order for a clean kedro diff output."""
    known_kedro_loggers = [
        "ProfileTimeTransformer",
        "hooks_handler",
        "kedro.__init__",
        "kedro",
        "kedro.config",
        "kedro.config.config",
        "kedro.extras.decorators.memory_profiler",
        "kedro.framework.cli",
        "kedro.framework.session.session",
        "kedro.framework.session.store",
        "kedro.framework.session",
        "kedro.io.cached_dataset",
        "kedro.io.data_catalog",
        "kedro.io",
        "kedro.journal",
        "kedro.pipeline",
        "kedro.pipeline.decorators",
        "kedro.pipeline.node",
        "kedro.pipeline.pipeline",
        "kedro.runner",
        "kedro.runner.runner",
        "kedro.versioning.journal",
        "py4",
    ]
    for logger in [
        *known_kedro_loggers,
        *list(logging.root.manager.loggerDict.keys()),  # type: ignore
    ]:
        logging.getLogger(logger).setLevel(logging.ERROR)


@click.group(name="kedro-diff")
@click.version_option(__version__, "-V", "--version", help="Prints version and exits")
def cli() -> None:
    """Kedro diff cli group."""
    pass


@cli.command()
@click.option("-o", "--output", type=click.File("wb"))
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="verbosity level, -v enables diff related logs, -vv enables all logs",
)
@click.option("-q", "--quiet", is_flag=True, help="runs completely quiet")
@click.option("-p", "--pipeline-name", help="name of pipeline")
@click.option("-p", "--commit", help="name of commit")
@click.option("-m", "--meta", is_flag=True, help="gets metadata needed for diff")
@click.pass_obj
def get_json(
    metadata: "ProjectMetadata",
    output: IO,
    verbose: int,
    quiet: bool,
    pipeline_name: str = "__default__",
    commit: str = "HEAD",
) -> None:
    """Get pipeline json from project context."""
    if quiet:
        verbose = -1
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    if verbose < 1:
        logger.setLevel(logging.ERROR)

    if verbose < 2:
        silent_loggers()

    session = KedroSession.create(metadata.package_name)
    context = session.load_context()

    meta_path = (
        Path(output.name)
        / (commit.replace("/", "_").replace(" ", "_") + "-commit-metadata.json")
    ).absolute()

    sha = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")

    diffmeta = {
        "commit": commit,
        "sha": sha,
        "pipelines": list(context.pipelines.keys()),
    }
    meta_path.write_text(json.dumps(diffmeta))

    for pipeline_name, pipeline in context.pipelines.items():
        output_file = Path(output.name) / (
            "_".join([commit, pipeline_name]).replace("/", "_") + ".json"
        )
        # pipeline: str = context.pipelines[pipeline_name].to_json()  # type: ignore
        pipeline = pipeline.to_json()
        if verbose >= 0:
            print(pipeline)
        # output_file.write_text(pipeline.encode("utf-8"))
        # breakpoint()
        output_file.write_text(pipeline)
    return


@cli.command()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="verbosity level, -v enables diff related logs, -vv enables all logs",
)
@click.argument("commit", nargs=-1)
@click.option("--stat", is_flag=True, help="generate short stats only")
@click.pass_obj
def diff(
    metadata: "ProjectMetadata", verbose: int, commit: Tuple[str, ...], stat: bool
) -> None:
    """ Diff two commits."""
    from kedro_diff.commit_parser import load_commit_metadata, parse_commit
    from kedro_diff.get_pipelines import to_json

    commit1, commit2 = parse_commit(commit)
    to_json(metadata.project_path, commit1)
    to_json(metadata.project_path, commit2)
    meta1, meta2 = load_commit_metadata(commit)
    all_pipelines = sorted({*meta1["pipelines"], *meta2["pipelines"]})
    for pipeline in all_pipelines:
        pipe1 = load_json(commit1, pipeline)
        pipe2 = load_json(commit2, pipeline)
        diff = KedroDiff(pipe1, pipe2, name=pipeline)
        if stat:
            diff.stat()
        else:
            diff.diff()


def load_json(commit: str, pipeline_name: str) -> Any:
    """
    Tries to load pipeline data from, if one is not found it returns an empty pipeline.

    Parameters
    --------
        commit : str
            a commit to load pipeline data for.
        pipeline_name : str
            a pipeline to load pipeline data for.

    Returns
    --------
        dict
            pipeline data

    """
    try:
        return json.loads(
            (
                Path(".kedro-diff")
                / ("_".join([commit, pipeline_name]).replace("/", "_") + ".json")
            ).read_text()
        )
    except FileNotFoundError:
        return create_simple_sample(0)


def diff_stat(commit1: str, commit2: str, pipeline_name: str = "__default__") -> None:
    """
    Does a diff --stat for the given pipeline_name between two commits.

    Parameters
    --------
        commit1 : str
            first commit to load pipeline data for.
        commit2 : str
            second commit to load pipeline data for.
        pipeline_name : str
            a pipeline to load pipeline data for.
    """
    pipe1 = load_json(commit1, pipeline_name)
    pipe2 = load_json(commit2, pipeline_name)

    diff = KedroDiff(pipe1, pipe2, name=pipeline_name)
    diff.stat()


if __name__ == "__main__":
    cli()
