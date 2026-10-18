#!/bin/sh
# Finder launcher; all implementation remains in the Python runtime.
cd -- "$(dirname -- "$0")" || exit 1
if command -v python3 >/dev/null 2>&1; then
    PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python3 core/bootstrap.py "$@"
    result=$?
else
    echo "Setup incomplete. Install company-approved Python 3.12, then run setup again."
    result=1
fi
if [ "$#" -eq 0 ] && [ -t 0 ]; then
    printf '\nPress Enter to close.'
    read -r answer
fi
exit "$result"
