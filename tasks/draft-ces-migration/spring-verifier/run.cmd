@echo off
setlocal
cd /d "%~dp0"
where java >nul 2>&1
if errorlevel 1 (
    echo Java is unavailable. Install approved JDK 17 and add its bin directory to PATH. 1>&2
    exit /b 2
)
set "verifier_java_version="
for /f "tokens=3" %%v in ('java -version 2^>^&1 ^| findstr /i "version"') do set "verifier_java_version=%%~v"
set "verifier_java_major="
for /f "tokens=1 delims=.-+" %%m in ("%verifier_java_version%") do set "verifier_java_major=%%m"
if not defined verifier_java_major (
    echo Cannot determine Java version. Select approved JDK 17 and run java -version. 1>&2
    exit /b 2
)
if %verifier_java_major% LSS 17 (
    echo Java 17 or later is required. Select the approved JDK and run java -version. 1>&2
    exit /b 2
)
if not exist "target\ems2-ces-spring-verifier-1.0.0.jar" (
    echo Verifier JAR is missing. Run mvn clean verify from this project directory. 1>&2
    exit /b 2
)
java -jar "target\ems2-ces-spring-verifier-1.0.0.jar" %*
exit /b %errorlevel%
