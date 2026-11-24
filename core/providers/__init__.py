"""Default providers; projects register resource instances separately."""

from .database import SQLiteDatabaseProvider
from .connectors import ConnectorMcpProvider
from .discovery import EurekaDiscoveryProvider
from .knowledge import LocalKnowledgeProvider
from .graph import GraphSnapshotProvider
from .logs import FileLogsProvider
from .repository import GitRepositoryProvider
from .robot import RobotTestingProvider
from .testing import CommandTestingProvider
from .release_report import ReleaseReportProvider


def builtin_providers(workspace_root=None) -> list:
    return [LocalKnowledgeProvider(), GitRepositoryProvider(), CommandTestingProvider(), RobotTestingProvider(),
            FileLogsProvider(), SQLiteDatabaseProvider(), EurekaDiscoveryProvider(), GraphSnapshotProvider(workspace_root),
            ConnectorMcpProvider(), ReleaseReportProvider()]
