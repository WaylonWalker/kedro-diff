from typing import Dict

empty = {"kedro_version": "0.17.2", "pipeline": []}
two_nodes = {
    "kedro_version": "0.17.2",
    "pipeline": [
        {"name": "node1", "inputs": [], "outputs": ["output1"], "tags": []},
        {"name": "node2", "inputs": ["output1"], "outputs": ["output2"], "tags": []},
    ],
}

one_node_one_tag = {
    "kedro_version": "0.17.2",
    "pipeline": [
        {"name": "node1", "inputs": [], "outputs": ["output1"], "tags": ["onetag"]}
    ],
}

one_node = {
    "kedro_version": "0.17.2",
    "pipeline": [{"name": "node1", "inputs": [], "outputs": ["output1"], "tags": []}],
}

two_nodes_two_tags = {
    "kedro_version": "0.17.2",
    "pipeline": [
        {"name": "node1", "inputs": [], "outputs": ["output1"], "tags": ["tag1"]},
        {
            "name": "node2",
            "inputs": ["output1"],
            "outputs": ["output2"],
            "tags": ["tag2"],
        },
    ],
}


def create_simple_sample(
    num_nodes: int = 1,
    kedro_version: str = "0.17.2",
    tagged: bool = True,
    name_prefix: str = "node",
) -> Dict:
    # {"name": "node1", "inputs": [], "outputs": ["output1"], "tags": []}
    return {
        "kedro_version": kedro_version,
        "pipeline": [
            {
                "name": f"{name_prefix}{n}",
                "inputs": [f"output{n-1}"],
                "outputs": [f"output{n}"],
                "tags": [f"tag{n}"],
            }
            for n in range(1, num_nodes + 1)
        ],
    }
