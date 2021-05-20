from itertools import product

import pytest

from kedro_diff.node_diff import NodeDiff

datasets = ["cars", "trains", None]
names = ["node1", "node2", None]

nodes = [
    {"name": name, "inputs": inputs, "outputs": outputs}
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
            "expected": {"inputs", "outputs", "name"},
        },
        {"node1": None, "node2": nodes[0], "expected": {"inputs", "outputs", "name"}},
        {"node1": nodes[0], "node2": None, "expected": {"inputs", "outputs", "name"}},
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
    ],
)
def test_get_attr(runargs):
    def run(node1, node2, attr, expected):
        assert NodeDiff(node1, node2).get_attr(attr) == expected

    run(**runargs)
