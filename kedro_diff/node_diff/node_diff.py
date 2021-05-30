from typing import Dict, List, Optional, Tuple, Union, TYPE_CHECKING

from rich.console import Console

if TYPE_CHECKING:
    from kedro.pipeline.node import Node


class NodeDiff:
    """NodeDiff.

    Compare kedro two Nodes
    """

    def __init__(
        self,
        node1: Optional[Union[Dict, "Node"]] = None,
        node2: Optional[Union[Dict, "Node"]] = None,
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

    @property
    def is_none(self) -> bool:
        return self.node1 is self.node2 is None

    @property
    def is_new(self) -> bool:
        return self.node1 is None

    @property
    def is_deleted(self) -> bool:
        return self.node2 is None

    @property
    def attrs(self) -> List:
        if self.is_deleted:
            _node = self.node1
        else:
            _node = self.node2

        if _node is None:
            return []
        # try:
        if isinstance(_node, dict):
            _node_dict = _node
            return [a for a in _node_dict.keys() if not a.startswith("_")]
        # except AttributeError:
        return [a for a in dir(_node) if not a.startswith("_")]

    def get_attr(self, attr: str) -> Tuple:

        try:
            if self.node1 is None:
                attr1 = None
            elif isinstance(self.node1, dict):
                attr1 = self.node1[attr]
            else:
                attr1 = getattr(self.node1, attr)
        except KeyError:
            attr1 = None

        try:
            if self.node2 is None:
                attr2 = None
            elif isinstance(self.node2, dict):
                attr2 = self.node2[attr]
            else:
                attr2 = getattr(self.node2, attr)
        except KeyError:
            attr2 = None

        if callable(attr1) or callable(attr2):
            return None, None
        return attr1, attr2

    def diff_attr(self, attr: str) -> None:
        attr1, attr2 = self.get_attr(attr)
        attr1 = "" if attr1 is None else attr1
        attr2 = "" if attr2 is None else attr2
        if attr1 != attr2:
            attr_name = f"{attr}:      "[:10]
            self.console.print(
                f"[{self.diff_color}]    {attr_name} [red][strike]{attr1}[/strike] [green]{attr2}"
            )

    def diff_attrs(self) -> None:
        for attr in self.attrs:
            self.diff_attr(attr)

    @property
    def diff_color(self) -> str:
        if self.is_deleted:
            return "red"
        if self.is_new:
            return "green"
        return "gold1"

    def diff(self) -> None:
        if self.is_none:
            if self.verbose_level > 1:
                self.console.print(f"[bright_black]  {self.name} is None")
        elif not self.is_changed:
            if self.verbose_level > 1:
                self.console.print(f"[bright_black]  {self.name} is unchanged")
        elif self.is_new:
            self.console.print(f"[green]+ {self.name}")
            self.diff_attrs()
            # for attr in self.attrs:
            #     _, attr2 = self.get_attr(attr)
            #     if attr2 is not None:
            #         if len(attr2) > 0:
            #             self.console.print(f"[green]    {attr}: {attr2}")
        elif self.is_deleted:
            self.console.print(f"[red]- [strike]{self.name}[/strike]")
            self.diff_attrs()
            # for attr in self.attrs:
            #     attr1, _ = self.get_attr(attr)
            #     if attr1 is not None:
            #         if len(attr1) > 0:
            #             self.console.print(f"[red]    {attr}: nodediff[strike]{attr1}")
        elif self.is_changed:
            self.console.print(f"[green]+ [{self.diff_color}]{self.name}")
            self.diff_attrs()
