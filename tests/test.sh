#!/bin/bash

SSR_SUB_SERVER_PORT=8001

python3 proxy_server.py &
cd ssr_sub_server
python3 -m http.server ${SSR_SUB_SERVER_PORT} &
cd ..
env XDG_DATA_HOME=$(pwd) XDG_CONFIG_HOME=$(pwd) XDG_DATA_DIRS=$(pwd) \
  XDG_CONFIG_DIRS=$(pwd) XDG_CACHE_HOME=$(pwd) XDG_RUNTIME_DIR=$(pwd) \
  python3 -m pytest --cov=../ssrcli
kill %1
kill %2
