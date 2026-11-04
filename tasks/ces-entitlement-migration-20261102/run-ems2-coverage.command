#!/bin/sh
set -eu
TASK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
WORKSPACE_DIR=$(CDPATH= cd -- "$TASK_DIR/../.." && pwd)
PYTHON_BIN=${CES_COVERAGE_PYTHON:-"$WORKSPACE_DIR/.venv/bin/python"}
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN=python3
fi
exec "$PYTHON_BIN" -m ai_sdlc_workbench.ems2_coverage --config "$TASK_DIR/coverage/ems2-config.json" --mode replay --open "$@"
