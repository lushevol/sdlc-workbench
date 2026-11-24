@echo off
setlocal
set "TASK_DIR=%~dp0"
if defined CES_COVERAGE_PYTHON (
  "%CES_COVERAGE_PYTHON%" -m ai_sdlc_workbench.ems2_coverage --config "%TASK_DIR%coverage\ems2-config.json" --mode replay --open %*
) else if exist "%TASK_DIR%..\..\.venv\Scripts\python.exe" (
  "%TASK_DIR%..\..\.venv\Scripts\python.exe" -m ai_sdlc_workbench.ems2_coverage --config "%TASK_DIR%coverage\ems2-config.json" --mode replay --open %*
) else (
  python -m ai_sdlc_workbench.ems2_coverage --config "%TASK_DIR%coverage\ems2-config.json" --mode replay --open %*
)
exit /b %ERRORLEVEL%
