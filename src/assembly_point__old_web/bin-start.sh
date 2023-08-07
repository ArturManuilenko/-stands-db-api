#!/bin/bash

echo ">>> $(basename ${BASH_SOURCE[0]})"
set -o errexit
set -o pipefail
set -o nounset
cd "$(dirname "${BASH_SOURCE[0]}")"
THIS_DIR=$(pwd)
cd ../../
CWD="$(pwd)"
export PYTHONUNBUFFERED=1
export PYTHONPATH="${CWD}"


# RUN
# ======================================================================================================
cd ${THIS_DIR}
#python3 "./server/server_start.py"
python3 "main.py" --port=${APPLICATION_PORT}
