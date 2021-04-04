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
    def _stat_msg(self) -> str:
        return f'[red]M[/red] {self.name.ljust(20)[:20]} | {len(self.new_nodes) + len(self.dropped_nodes)} [green]{"+" * len(self.new_nodes)}[/green][red]{"-"*len(self.dropped_nodes)}[/red]'

    def stat(self) -> None:
        self.console.print(self._stat_msg)


if __name__ == "__main__":
    from kedro_diff.sample_data import create_simple_sample, empty, one_node, two_nodes

    console = Console()
    console.print("[gold1]KedroDiff Examples[/]\n")
    console.print("[brightblack]KedroDiff.stat()[/]\n")
    KedroDiff(empty, one_node).stat()
    KedroDiff(empty, two_nodes, name="two_new_nodes").stat()
    KedroDiff(empty, create_simple_sample(12), name="twelve_new_nodes").stat()
    KedroDiff(
        create_simple_sample(10, name_prefix="first"),
        create_simple_sample(12),
        name="twelve_new_nodes_ten_dropped_nodes",
    ).stat()
