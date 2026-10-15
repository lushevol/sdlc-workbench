"""Expose the dependency skill through Workbench operation grants and action records."""

from __future__ import annotations

from ..models import Context, Operation, Resource
from ..relationships.skill import load_graph_tool
from .common import BuiltinProvider, ProviderError, configured_path


def _operations(workspace_root=None):
    helper = load_graph_tool("snapshot", workspace_root)
    return {name: Operation(name, item["description"], item["input_schema"])
            for name, item in helper.OPERATIONS.items()}


class GraphSnapshotProvider(BuiltinProvider):
    id = "graph.snapshot"
    resource_kind = "dependency_graph"
    def __init__(self, workspace_root=None):
        self.operations = _operations(workspace_root)

    def _invoke(self, operation: str, resource: Resource, arguments: dict, context: Context) -> dict:
        helper = load_graph_tool("snapshot", context.workspace_root)
        try:
            return helper.query(configured_path(resource, context), operation, arguments, context.workspace_root)
        except helper.SnapshotError as error:
            raise ProviderError(error.code, error.message) from error
