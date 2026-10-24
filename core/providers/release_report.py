"""Release report collection through explicit source grants and retained actions."""

from ..models import Operation
from .common import BuiltinProvider, integer_schema, object_schema, string_schema


class ReleaseReportProvider(BuiltinProvider):
    id = "release.report"
    resource_kind = "release_report"
    operations = {
        "collect": Operation("collect", "Collect a complete release snapshot without rendering or modifying external systems.",
                             object_schema({"release_id": integer_schema(1, 2147483647),
                                            "output_dir": string_schema(), "resume": string_schema()},
                                           ("release_id",)), mutating=True),
    }

    def _invoke(self, operation, resource, arguments, context):
        from ..release_report import _collect
        return _collect(arguments["release_id"], resource, context,
                        output_dir=arguments.get("output_dir"), resume=arguments.get("resume"))
