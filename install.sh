#!/bin/bash
set -euo pipefail

INSTALL_DIR="$HOME/.local/share/ssrcli"
SCRIPT_PATH="$HOME/.local/bin/ssrcli"

git clone https://github.com/myl7/ssrcli --depth=1 ${INSTALL_DIR}
cd ${INSTALL_DIR}
python3 -c 'import sys,venv;assert sys.version_info[1]>=6'
python3 -m venv venv
source venv/bin/activate
pip install $(sed '2,/# test_reqs/!d' "${INSTALL_DIR}/requirements.txt" | sed '/^#/d')
cat > ${SCRIPT_PATH} << EOF
#!/bin/bash
set -euo pipefail

cd ~/.local/share/ssrcli
source venv/bin/activate
python -m ssrcli "\$@"
EOF
chmod +x ${SCRIPT_PATH}
