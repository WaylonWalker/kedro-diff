from typing import TYPE_CHECKING, List, Optional, Tuple

from rich.console import Console

if TYPE_CHECKING:
    from kedro.pipeline.node import Node


class NodeDiff:
    """NodeDiff.

    Compare kedro two Nodes
    """

    def __init__(
        self,
        node1: Optional["Node"] = None,
        node2: Optional["Node"] = None,
        name: Optional[str] = None,
        verbose_level: int = 1,
    ) -> None:
        """
        verbose levels
        0: silent
        1: (default) prints only node diffs
        2: prints regardless of equality

        """
        self.node1 = node1
        self.node2 = node2
        self.name = name
        self.console = Console()
        self.verbose_level = verbose_level

    @property
    def is_changed(self) -> bool:
        return self.node1 != self.node2

    def is_none(self) -> bool:
        return self.node1 is self.node2 is None

    @property
    def is_new(self) -> bool:
        return self.node1 is None

    @property
    def is_deleted(self) -> bool:
        return self.node2 is None

    @property
    def mod_name(self) -> Optional[str]:
        if not self.is_changed:
            return self.name
        if self.is_new:
            return self.name
        if self.is_deleted:
            return f"[strike]{self.name}[/strike]"

    @property
    def attrs(self) -> List:
        if self.is_deleted:
            _node = self.node1
        else:
            _node = self.node2
        # breakpoint()
        return [a for a in _node.keys() if not a.startswith("_")]

    def get_attr(self, attr) -> Tuple:
        try:
            attr1 = getattr(self.node1, attr)
        except AttributeError:
            try:
                attr1 = self.node1[attr]
            except KeyError:
                attr1 = None
            except TypeError:
                attr1 = None

        try:
            attr2 = getattr(self.node2, attr)
        except AttributeError:
            try:
                attr2 = self.node2[attr]
            except KeyError:
                attr2 = None
            except TypeError:
                attr2 = None

        if callable(attr1) or callable(attr2):
            return None, None
        return attr1, attr2

    def diff_attr(self, attr) -> None:
        attr1, attr2 = self.get_attr(attr)
        if callable(attr1) or callable(attr2):
            return
        if attr1 != attr2:
            attr_name = f"{attr}:      "[:10]
            self.console.print(
                f"[gold1]    {attr_name} [red][strike]{attr1}[/strike] [green]{attr2}"
            )

    def diff(self) -> None:
        if not self.is_none:
            if self.verbose_level > 1:
                self.console.print(f"[bright_black]  {self.name} is None")
        elif not self.is_changed:
            if self.verbose_level > 1:
                self.console.print(f"[bright_black]  {self.name} is unchanged")
        elif self.is_new:
            self.console.print(f"[green]+ {self.name}")
            for attr in self.attrs:
                _, attr2 = self.get_attr(attr)
                if attr2 is not None:
                    if len(attr2) > 0:
                        self.console.print(f"[green]    {attr}: {attr2}")
            # self.console.print(f"[green]    inputs: {self.node2.inputs}")
            # self.console.print(f"[green]    outputs: {self.node2.outputs}")
            # self.console.print(f"[green]    tags: {self.node2.tags}")
        elif self.is_deleted:
            self.console.print(f"[red]- {self.mod_name}")
            for attr in self.attrs:
                attr1, _ = self.get_attr(attr)
                if attr1 is not None:
                    if len(attr1) > 0:
                        self.console.print(f"[red]    {attr}: nodediff[strike]{attr1}")
        elif self.is_changed:
            self.console.print(f"[green]+ [gold1]{self.name}")

            for attr in self.attrs:
                self.diff_attr(attr)
        else:
            print("else")
            # if self.node1.inputs != self.node2.inputs:
            #     self.console.print(
            #         f"[gold1]    I: [red][strike]{self.node1.inputs}[/strike] [green]{self.node2.inputs}"
            #     )
            # if self.node1.outputs != self.node2.outputs:
            #     self.console.print(
            #         f"[gold1]    O: [red][strike]{self.node1.outputs}[/strike] [green]{self.node2.outputs}"
            #     )
            # if self.node1.tags != self.node2.tags:
            #     self.console.print(
            #         f"[gold1]    T: [red][strike]{self.node1.tags}[/strike] [green]{self.node2.tags}"
            #     )
            # if self.node1.tags != self.node2.tags:
            #     self.console.print(
            #         f"[gold1]    T: [red][strike]{self.node1.tags}[/strike] [green]{self.node2.tags}"
            #     )


if __name__ == "__main__":
    from kedro.pipeline.node import node

    node1 = node(lambda x: x, "input", "output", name="id")
    node1_b = node(lambda x: x, "input", "output", name="id")
    node2 = node(lambda x: x, "input", "output", name="id")
    node3 = node(lambda x: x, "input3", "output", name="id")
    node4 = node(lambda x: x, "input", "output4", name="id")
    node5 = node(lambda x: x, "input", "output", tags=["new-tag"], name="id")

    NodeDiff(node1, node1, name="is").diff()
    NodeDiff(node1, node1, name="verbose_is", verbose_level=2).diff()
    NodeDiff(node1, node1_b, name="equal").diff()
    NodeDiff(node1, node1_b, name="verbose_equal", verbose_level=2).diff()
    NodeDiff(node1, None, name="deleted_node").diff()
    NodeDiff(None, None, name="none").diff()
    NodeDiff(None, None, name="verbose_none", verbose_level=2).diff()
    NodeDiff(None, node1, name="new_node").diff()
    NodeDiff(node1, node2, name="name_changed").diff()
    NodeDiff(node1, node3, name="input_changed").diff()
    NodeDiff(node1, node4, name="output_changed").diff()
    NodeDiff(node1, node5, name="tag_changed", verbose_level=2).diff()
    NodeDiff(node5, node1, name="tag_dropped", verbose_level=2).diff()
