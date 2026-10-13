"""Default providers; projects register resource instances separately."""

from .database import SQLiteDatabaseProvider
from .discovery import EurekaDiscoveryProvider
from .knowledge import LocalKnowledgeProvider
from .logs import FileLogsProvider
from .repository import GitRepositoryProvider
from .testing import CommandTestingProvider


def builtin_providers() -> list:
    return [LocalKnowledgeProvider(), GitRepositoryProvider(), CommandTestingProvider(),
            FileLogsProvider(), SQLiteDatabaseProvider(), EurekaDiscoveryProvider()]
