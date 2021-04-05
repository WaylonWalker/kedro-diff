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
        return set(
            [
                str({node["name"]: node["inputs"]})
                for node in self.pipe2
                if node["name"] in self.not_new_dropped_nodes
            ]
        ).difference(
            set(
                [
                    str({node["name"]: node["inputs"]})
                    for node in self.pipe1
                    if node["name"] in self.not_new_dropped_nodes
                ]
            )
        )

    @property
    def num_changes(self) -> int:
        return len(self.new_nodes) + len(self.dropped_nodes) + len(self.change_input)

    @property
    def _stat_msg(self) -> str:
        return f'[red]M[/red] {self.name.ljust(20)[:20]} | {self.num_changes} [green]{"+" * (len(self.new_nodes) + len(self.change_input))}[/green][red]{"-"*len(self.dropped_nodes)}[/red]'

    def stat(self) -> None:
        self.console.print(self._stat_msg)


if __name__ == "__main__":
    from kedro_diff.sample_data import create_simple_sample

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
