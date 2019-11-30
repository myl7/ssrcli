#!/bin/bash

SSR_SUB_SERVER_PORT=8001

python3 proxy_server.py &
cd ssr_sub_server
python3 -m http.server ${SSR_SUB_SERVER_PORT} &
cd ..
# WARNING: When switch between comments, remember to move the line up
env XDG_DATA_HOME=$(pwd) XDG_CONFIG_HOME=$(pwd) XDG_DATA_DIRS=$(pwd) \
  XDG_CONFIG_DIRS=$(pwd) XDG_CACHE_HOME=$(pwd) XDG_RUNTIME_DIR=$(pwd) \
  python3 -m pytest --cov=../ssrcli
#  python3 -m pytest --cov=../ssrcli -k 'not test_install_and_test_ssr and not test_remove_ssr'  --ignore=shadowsocksr/
kill %1
kill %2
