from typing import Dict

from rich.console import Console


class KedroDiff:
    def __init__(self, pipe1: Dict, pipe2: Dict, name: str = "__default__") -> None:
        self.pipe1 = pipe1["pipeline"]
        self.pipe2 = pipe2["pipeline"]
        self.name = name
        self.console = Console()

    @property
    def new_nodes(self) -> set:
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
            + len(self.change_input)
            + len(self.change_output)
            + len(self.change_tag)
        )

    @property
    def num_adds(self) -> int:
        return self.num_changes - len(self.dropped_nodes)

    @property
    def num_drops(self) -> int:
        return len(self.dropped_nodes)

    @property
    def _stat_msg(self) -> str:
        return f'[red]M[/red] {self.name.ljust(30)[:30]} | {self.num_changes} [green]{"+" * self.num_adds}[/green][red]{"-"*self.num_drops}[/red]'

    def stat(self) -> None:
        self.console.print(self._stat_msg)


def example() -> None:
    from kedro_diff.sample_data import create_simple_sample
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

    KedroDiff(pipe10, pipe10_change_one_input, name="ten_nodes_one_input_change").stat()

    KedroDiff(
        pipe10, pipe10_change_one_output, name="ten_nodes_one_output_change"
    ).stat()
    KedroDiff(pipe10, pipe10_change_one_tag, name="ten_nodes_one_tag_change").stat()
