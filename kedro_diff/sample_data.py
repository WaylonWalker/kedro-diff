"""Sample Data.

Module for creating sample pipeline.json data for use in examples and tests.
"""
from typing import Dict


def create_simple_sample(
    num_nodes: int = 1,
    kedro_version: str = "0.17.2",
    tagged: bool = True,
    name_prefix: str = "node",
) -> Dict:
    """Create Sample data for examples and tests.

    Args:
        num_nodes: number of nodes to generate in the pipeline
        kedro_version: kedro version to use in the pipeline.json format
        tagged: to tag the datasets or not
        name_prefix: prefix to add to the name of each node

    Returns:
        kedro pipeline.json sample data as a dictionary

    Example:
        >>> create_simple_sample(1)
        {'kedro_version': '0.17.2', 'pipeline': [{'name': 'node1', 'inputs': ['output0'], 'outputs': ['output1'], 'tags': ['tag1']}]}

        >>> create_simple_sample(1, name_prefix='first')
        {'kedro_version': '0.17.2', 'pipeline': [{'name': 'first1', 'inputs': ['output0'], 'outputs': ['output1'], 'tags': ['tag1']}]}

        >>> create_simple_sample(1, tagged=False)
        {'kedro_version': '0.17.2', 'pipeline': [{'name': 'node1', 'inputs': ['output0'], 'outputs': ['output1'], 'tags': ['']}]}
    """
    # {"name": "node1", "inputs": [], "outputs": ["output1"], "tags": []}
    return {
        "kedro_version": kedro_version,
        "pipeline": [
            {
                "name": f"{name_prefix}{n}",
                "inputs": [f"output{n-1}"],
                "outputs": [f"output{n}"],
                "tags": [f"tag{n}" if tagged else ""],
            }
            for n in range(1, num_nodes + 1)
        ],
    }
