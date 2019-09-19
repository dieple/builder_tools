#!/bin/bash

AWS_VAULT_PROFILE=$1

if [[ "${AWS_VAULT_PROFILE}" == "" ]]; then
    echo "Supply aws-vault profile name as \$1"
    exit 1
fi

SCRIPT_DIR=`dirname "$0"`
cd "${SCRIPT_DIR}/.."

python3 ./builder.py \
    --githubUsername=dieple \
    --githubEmail=dieple1@gmail.com \
    --shareHostVolume=$HOME/repos \
    --terraformVersion=0.11.13 \
    --installTerraform=true \
    --dockerAppUser=dataops \
    --profile="$AWS_VAULT_PROFILE" \
    --imageName=dataops
