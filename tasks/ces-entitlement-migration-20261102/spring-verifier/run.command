#!/bin/sh
set -eu
project_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$project_dir"
if ! command -v java >/dev/null 2>&1; then
    echo "Java is unavailable. Install approved JDK 17 and add its bin directory to PATH." >&2
    exit 2
fi
java_major=$(java -version 2>&1 | sed -n 's/.*version "\([0-9][0-9]*\).*/\1/p' | head -n 1)
case "$java_major" in
    ''|*[!0-9]*) echo "Cannot determine Java version. Use approved JDK 17 and run java -version." >&2; exit 2 ;;
esac
if [ "$java_major" -lt 17 ]; then
    echo "Java 17 or later is required. Select the approved JDK and run java -version." >&2
    exit 2
fi
verifier_jar=target/ems2-ces-spring-verifier-1.0.0.jar
if [ ! -f "$verifier_jar" ]; then
    echo "Verifier JAR is missing. Run mvn clean verify from this project directory." >&2
    exit 2
fi
exec java -jar "$verifier_jar" "$@"
