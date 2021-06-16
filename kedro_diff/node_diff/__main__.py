from kedro.pipeline.node import node

from kedro_diff.node_diff import NodeDiff

node1 = node(lambda x: x, "input", "output", name="id")
node1_b = node(lambda x: x, "input", "output", name="id")
node2 = node(lambda x: x, "input", "output", name="new-id")
node3 = node(lambda x: x, "input3", "output", name="id")
node4 = node(lambda x: x, "input", "output4", name="id")
node5 = node(lambda x: x, "input", "output", tags=["new-tag"], name="id")

# Node that is the same node should not print
NodeDiff(node1, node1, name="is").diff()
# Node that is the same node should print unchanged if verbose
NodeDiff(node1, node1, name="verbose_is", verbose_level=2).diff()
# Node that is an equvalent node should not print
NodeDiff(node1, node1_b, name="equal").diff()
# Node that is an equvalent node should print unchanged if verbose
NodeDiff(node1, node1_b, name="verbose_equal", verbose_level=2).diff()
# Node Identifies as deleted
NodeDiff(node1, None, name="deleted_node").diff()
# Node Identifies as none should not print
NodeDiff(None, None, name="none").diff()
# Node Identifies as none should print unchanged if verbose
NodeDiff(None, None, name="verbose_none", verbose_level=2).diff()
# Node Identifies as new
NodeDiff(None, node1, name="new_node").diff()
#
NodeDiff(node1, node2, name="name_changed").diff()
NodeDiff(node1, node3, name="input_changed").diff()
NodeDiff(node1, node4, name="output_changed").diff()
NodeDiff(node1, node5, name="tag_changed", verbose_level=2).diff()
NodeDiff(node5, node1, name="tag_dropped", verbose_level=2).diff()
