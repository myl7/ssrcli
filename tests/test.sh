#!/bin/bash

SUB_TEST_SERVER_PORT=8001

python3 proxy_server.py &
cd ssr_sub_server
python3 -m http.server ${SUB_TEST_SERVER_PORT} &
cd ..
env XDG_DATA_HOME=. XDG_CONFIG_HOME=. XDG_DATA_DIRS=. XDG_CONFIG_DIRS=. XDG_CACHE_HOME=. XDG_RUNTIME_DIR=. \
  python3 -m pytest --ignore=ssrcli
kill %1
kill %2
