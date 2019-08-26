#!/usr/bin/env bash

set -euo pipefail

SUB_SERVER_PORT=8001

cd "$(dirname "$0")/../config/ssr_sub_server"

python3 -m http.server ${SUB_SERVER_PORT}
