"""Diff.

Core diffing logic for kedro diff.
"""
from typing import Dict

from rich.console import Console
from rich.panel import Panel

from kedro_diff.sample_data import create_simple_sample


class KedroDiff:
    """KedroDiff.

    Compare kedro two pipelines

    Parameters
    --------
        pipe1 : Dict
            base pipeline
        pipe2 : Dict
            pipeline to compare to the base pipeline
        name : str
            name of the pipeline that is being compared

    Examples
    --------
        >>> from kedro_diff import KedroDiff
        >>> diff = KedroDiff.from_sample({"num_nodes": 2}, {"num_nodes": 4})
        >>> diff.stat()
        M __default__                    | 2 ++
    """

    def __init__(self, pipe1: Dict, pipe2: Dict, name: str = "__default__") -> None:
        self.pipe1 = pipe1["pipeline"]
        self.pipe2 = pipe2["pipeline"]
        self.name = name
        self.console = Console()

    @classmethod
    def from_sample(
        cls, pipe1_args: Dict, pipe2_args: Dict, name: str = "__default__"
    ) -> "KedroDiff":
        """
        Creates a KedroDiff from `create_simple_sample` arguuments.

        Parameters
        --------
        pipe1_args : dict
            arguments used to create pipe1
        pipe2_args : dict
            arguments used to create pipe2
        name : str
            name of the pipeline that is being compared

        See Also
        --------
        kedro_diff.sample_data.create_simple_sample

        Examples
        --------
            >>> from kedro_diff import KedroDiff
            >>> diff = KedroDiff.from_sample({"num_nodes": 2}, {"num_nodes": 4})
            >>> diff.stat()
            M __default__                    | 2 ++

        """
        pipe1 = create_simple_sample(**pipe1_args)
        pipe2 = create_simple_sample(**pipe2_args)
        return cls(pipe1=pipe1, pipe2=pipe2, name=name)

    @property
    def new_nodes(self) -> set:
        """
        Compares

        Returns
        --------
        set
            a set of new nodes.

        """
        return set([node["name"] for node in self.pipe2]).difference(
            set([node["name"] for node in self.pipe1])
        )

    @property
    def dropped_nodes(self) -> set:
        return set([node["name"] for node in self.pipe1]).difference(
            set([node["name"] for node in self.pipe2])
        )

    @property
    def not_new_dropped_nodes(self) -> set:
        return (
            set([node["name"] for node in self.pipe2])
            - self.new_nodes
            - self.dropped_nodes
        )

    @property
    def change_input(self) -> set:
        return self.change_attr("inputs")

    @property
    def change_output(self) -> set:
        return self.change_attr("outputs")

    @property
    def change_tag(self) -> set:
        return self.change_attr("tags")

    def change_attr(self, attr: str) -> set:
        return set(
            [
                str({node["name"]: node[attr]})
                for node in self.pipe2
                if node["name"] in self.not_new_dropped_nodes
            ]
        ).difference(
            set(
                [
                    str({node["name"]: node[attr]})
                    for node in self.pipe1
                    if node["name"] in self.not_new_dropped_nodes
                ]
            )
        )

    @property
    def num_changes(self) -> int:
        return (
            len(self.new_nodes)
            + len(self.dropped_nodes)
            + len(self.change_input) * 2
            + len(self.change_output) * 2
            + len(self.change_tag) * 2
        )

    @property
    def num_adds(self) -> int:
        return (
            len(self.new_nodes)
            + len(self.change_input)
            + len(self.change_output)
            + len(self.change_tag)
        )

    @property
    def num_drops(self) -> int:
        return (
            len(self.dropped_nodes)
            + len(self.change_input)
            + len(self.change_output)
            + len(self.change_tag)
        )

    @property
    def _stat_msg(self) -> str:
        return f'[red]M[/red] {self.name.ljust(30)[:30]} | {self.num_changes} [green]{"+" * self.num_adds}[/green][red]{"-"*self.num_drops}[/red]'

    def stat(self) -> None:
        self.console.print(self._stat_msg)

    def diff(self) -> None:
        if self.num_changes == 0:
            return
        self.console.print(
            Panel(
                f"modified: {self.name.ljust(88)}",
                title="[bright_black]kedro-diff[/bright_black]",
                title_align="right",
                expand=False,
            ),
        )
        for node in sorted(self.new_nodes):
            self.console.print(f"[green]+ {node}[/green]")
        for node in sorted(self.dropped_nodes):
            self.console.print(f"[red]- {node}[/red]")
        self.console.print(
            f"{self.num_adds} insertions([green]+[/green]), {self.num_drops} deletions([red]-[/red])"
        )


def example() -> None:
    from copy import deepcopy

    pipe10 = create_simple_sample(10)

    pipe10_change_one_input = deepcopy(pipe10)
    pipe10_change_one_input["pipeline"][2]["inputs"] = ["input1"]

    pipe10_change_one_output = deepcopy(pipe10)
    pipe10_change_one_output["pipeline"][2]["outputs"] = ["output1"]

    pipe10_change_one_tag = deepcopy(pipe10)
    pipe10_change_one_tag["pipeline"][2]["tags"] = ["tag1"]

    console = Console()
    console.print("[gold1]KedroDiff Examples[/]\n")
    console.print("[brightblack]KedroDiff.stat()[/]\n")

    KedroDiff(create_simple_sample(0), create_simple_sample(1)).stat()

    KedroDiff(
        create_simple_sample(0), create_simple_sample(2), name="two_new_nodes"
    ).stat()

    KedroDiff(
        create_simple_sample(0), create_simple_sample(12), name="twelve_new_nodes"
    ).stat()

    KedroDiff(
        create_simple_sample(10, name_prefix="first"),
        create_simple_sample(12),
        name="twelve_new_nodes_ten_dropped_nodes",
    ).stat()

    diff_change_one_input = KedroDiff(
        pipe10, pipe10_change_one_input, name="ten_nodes_one_input_change"
    )
    diff_change_one_input.stat()

    KedroDiff(
        pipe10, pipe10_change_one_output, name="ten_nodes_one_output_change"
    ).stat()
    KedroDiff(pipe10, pipe10_change_one_tag, name="ten_nodes_one_tag_change").stat()

    console.print("\n\n")
    console.print("[brightblack]KedroDiff.diff()[/]\n")

    KedroDiff(create_simple_sample(1), create_simple_sample(1)).diff()
    KedroDiff(create_simple_sample(0), create_simple_sample(1)).diff()
    KedroDiff(
        create_simple_sample(10, name_prefix="first"),
        create_simple_sample(12),
        name="twelve_new_nodes_ten_dropped_nodes",
    ).diff()

    diff_change_one_input.diff()
