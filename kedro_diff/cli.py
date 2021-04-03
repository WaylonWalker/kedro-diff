"""kedro_diff cli module."""
import json
import logging
from pathlib import Path
from typing import IO, TYPE_CHECKING, Tuple

import click
from kedro.framework.session import KedroSession
from rich import print

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
@click.pass_obj
def get_json(
    metadata: "ProjectMetadata", output: IO, verbose: int, quiet: bool
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

    pipeline: str = context.pipeline.to_json()  # type: ignore
    if verbose >= 0:
        print(pipeline)
    output.write(pipeline.encode("utf-8"))


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
    """Diff two commits."""
    from kedro_diff.commit_parser import parse_commit
    from kedro_diff.get_pipelines import to_json

    commit1, commit2 = parse_commit(commit)
    to_json(metadata.project_path, commit1)
    to_json(metadata.project_path, commit2)
    if stat:
        pipe1 = json.loads((Path(".kedro-diff") / (commit1 + ".json")).read_text())[
            "pipeline"
        ]
        pipe2 = json.loads((Path(".kedro-diff") / (commit2 + ".json")).read_text())[
            "pipeline"
        ]
        if len(pipe1) != len(pipe2):
            new_nodes = set([node["name"] for node in pipe2]).difference(
                set([node["name"] for node in pipe1])
            )

            dropped_nodes = set([node["name"] for node in pipe1]).difference(
                set([node["name"] for node in pipe2])
            )

            print(
                f'[red]M[/red] __default__ | {len(new_nodes) + len(dropped_nodes)} [green]{"+" * len(new_nodes)}[/green][red]{"-"*len(dropped_nodes)}[/red]'
            )


if __name__ == "__main__":
    cli()
