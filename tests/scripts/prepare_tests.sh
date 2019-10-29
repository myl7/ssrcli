#!/bin/bash
set -euo pipefail

SUB_TEST_SERVER_PORT=8001

cd "$(dirname "$0")/../resources/ssr_sub_server"
python3 -m http.server ${SUB_TEST_SERVER_PORT}
