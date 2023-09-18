from __future__ import annotations


def flatten_node_lists(obj):  # noqa: ANN001, ANN201
    """Flatten nodes lists."""
    if isinstance(obj, dict) and obj.keys() == {"nodes"}:
        return [flatten_node_lists(item) for item in obj["nodes"]]

    if isinstance(obj, dict):
        return {key: flatten_node_lists(value) for key, value in obj.items()}

    return obj
