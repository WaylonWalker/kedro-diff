from itertools import product

import pytest
from kedro.pipeline.node import node

from kedro_diff.node_diff import NodeDiff

datasets = ["cars", "trains", None]
names = ["node1", "node2", None]

nodes = [
    {"name": name, "inputs": inputs, "outputs": outputs, "func": lambda x: x}
    for name, inputs, outputs in product(names, datasets, datasets)
]


changed_nodes = [
    {"node1": node1, "node2": node2, "expected": (node1 != node2)}
    for node1, node2 in product(nodes, nodes)
]


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "node1": {"name": "node1", "inputs": None, "outputs": None},
            "node2": None,
            "expected": True,
        },
        {
            "node1": None,
            "node2": {"name": "node1", "inputs": None, "outputs": None},
            "expected": True,
        },
        *changed_nodes,
    ],
)
def test_is_changed(runargs):
    def run(node1, node2, expected):
        assert (
            NodeDiff(node1, node2).is_changed == expected
        ), f"node1:{node1},  node2: {node1}, expected: {expected}"

    run(**runargs)


def test_is_none_true():
    assert NodeDiff(None, None).is_none is True


def test_is_none_false():
    assert NodeDiff(None, nodes[0]).is_none is False


def test_is_new_true():
    assert NodeDiff(None, nodes[0]).is_new is True


def test_is_new_false():
    assert NodeDiff(nodes[0], nodes[0]).is_new is False
    assert NodeDiff(nodes[0], None).is_new is False


def test_is_deleted_true():
    assert NodeDiff(nodes[0], None).is_deleted is True


def test_is_deleted_false():
    assert NodeDiff(nodes[0], nodes[0]).is_new is False
    assert NodeDiff(None, nodes[0]).is_deleted is False


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "expected": {"inputs", "outputs", "name", "func"},
        },
        {
            "node1": None,
            "node2": nodes[0],
            "expected": {"inputs", "outputs", "name", "func"},
        },
        {
            "node1": nodes[0],
            "node2": None,
            "expected": {"inputs", "outputs", "name", "func"},
        },
        {
            "node1": {"func": lambda x: x},
            "node2": None,
            "expected": {"func"},
        },
    ],
)
def test_attrs(runargs):
    def run(node1, node2, expected):
        assert set(NodeDiff(node1, node2).attrs) == expected

    run(**runargs)


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "name",
            "expected": (
                nodes[0]["name"],
                nodes[0]["name"],
            ),
        },
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "not_here",
            "expected": (
                None,
                None,
            ),
        },
        {
            "node1": None,
            "node2": nodes[0],
            "attr": "name",
            "expected": (
                None,
                nodes[0]["name"],
            ),
        },
        {
            "node1": nodes[0],
            "node2": None,
            "attr": "name",
            "expected": (
                nodes[0]["name"],
                None,
            ),
        },
        {
            "node1": {"func": lambda x: x},
            "node2": None,
            "attr": "func",
            "expected": (None, None),
        },
    ],
)
def test_get_attr(runargs):
    def run(node1, node2, attr, expected):
        assert NodeDiff(node1, node2).get_attr(attr) == expected

    run(**runargs)


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "name",
        },
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "inputs",
        },
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "outputs",
        },
        {
            "node1": nodes[0],
            "node2": nodes[0],
            "attr": "func",
        },
    ],
)
def test_diff_attr_none(runargs, caplog, capsys):
    def run(node1, node2, attr):
        NodeDiff(node1, node2).diff_attr(attr)
        assert caplog.text == ""
        assert capsys.readouterr().out == ""

    run(**runargs)


@pytest.mark.parametrize(
    "runargs",
    [
        {
            "node1": {
                "name": "node1",
                "inputs": "cars",
                "outputs": "carsout",
                "func": lambda x: x,
            },
            "node2": {
                "name": "node1",
                "inputs": "cars",
                "outputs": "carsout1",
                "func": lambda x: x,
            },
            "expected_ins": ["node1", "outputs", "carsout", "carsout1"],
        },
    ],
)
def test_diff(runargs, caplog, capsys):
    def run(node1, node2, expected_ins):
        NodeDiff(node1, node2, "node1").diff()
        assert caplog.text == ""
        log = capsys.readouterr().out
        for expected in expected_ins:
            assert expected in log

    run(**runargs)


def test_diff_none_none(caplog, capsys):
    NodeDiff(None, None, "node1").diff()
    assert caplog.text == ""
    log = capsys.readouterr().out
    assert "" in log


def test_diff_none_none_verbose(caplog, capsys):
    NodeDiff(None, None, "node1", verbose_level=2).diff()
    assert caplog.text == ""
    log = capsys.readouterr().out
    assert "is None" in log


def test_diff_Node_equal(caplog, capsys):

    node1 = node(lambda x: x, "input", "output", name="id")
    node2 = node(lambda x: x, "input", "output", name="id")
    NodeDiff(node1, node2, "node1").diff()
    assert caplog.text == ""
    log = capsys.readouterr().out
    assert "unchanged" not in log
    assert log == ""


def test_diff_Node_equal_verbose(caplog, capsys):

    node1 = node(lambda x: x, "input", "output", name="id")
    node2 = node(lambda x: x, "input", "output", name="id")
    NodeDiff(node1, node2, "node1", verbose_level=2).diff()
    assert caplog.text == ""
    log = capsys.readouterr().out
    assert "unchanged" in log


def test_attrs_none_none():
    assert NodeDiff(None, None, "node1").attrs == []


def test_diff_Node_attrs(caplog, capsys):

    node1 = node(lambda x: x, "input", "output", name="id")
    node2 = node(lambda x: x, "input", "output", name="id")
    expecteds = ["func", "inputs", "outputs"]
    for expected in expecteds:
        assert expected in NodeDiff(node1, node2, "node1").attrs
    assert caplog.text == ""
    log = capsys.readouterr().out
    assert "unchanged" not in log
    assert log == ""
