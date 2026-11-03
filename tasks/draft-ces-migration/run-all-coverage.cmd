@echo off
setlocal
set "TASK_DIR=%~dp0"
if defined CES_COVERAGE_PYTHON (
  "%CES_COVERAGE_PYTHON%" -m ai_sdlc_workbench.coverage_suite --config "%TASK_DIR%coverage\suite.json" --mode replay --open %*
) else if exist "%TASK_DIR%..\..\.venv\Scripts\python.exe" (
  "%TASK_DIR%..\..\.venv\Scripts\python.exe" -m ai_sdlc_workbench.coverage_suite --config "%TASK_DIR%coverage\suite.json" --mode replay --open %*
) else (
  python -m ai_sdlc_workbench.coverage_suite --config "%TASK_DIR%coverage\suite.json" --mode replay --open %*
)
exit /b %ERRORLEVEL%
