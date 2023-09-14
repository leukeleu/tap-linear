from __future__ import annotations

from tap_linear.utils import flatten_node_lists


def test_flatten_node_lists():
    assert flatten_node_lists(
        {
            "things": {
                "nodes": [{"id": 1}, {"id": 2}],
            },
            "object": {
                "id": 3,
            },
            "scalar": "value",
            "list": [1, 2, 3],
            "nested": {
                "things": {
                    "nodes": [{"id": 4}, {"id": 5}],
                },
            },
        },
    ) == {
        "things": [{"id": 1}, {"id": 2}],
        "object": {
            "id": 3,
        },
        "scalar": "value",
        "list": [1, 2, 3],
        "nested": {
            "things": [{"id": 4}, {"id": 5}],
        },
    }
