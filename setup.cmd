@echo off
setlocal DisableDelayedExpansion
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 "%~dp0core\bootstrap.py" %*
goto finished
:use_python
where python >nul 2>nul
if errorlevel 1 goto missing_python
python "%~dp0core\bootstrap.py" %*
goto finished
:missing_python
echo Setup incomplete. Install company-approved Python 3.12, then run setup again.
set "setup_result=1"
goto close
:finished
set "setup_result=%errorlevel%"
:close
if "%~1"=="" pause
exit /b %setup_result%
