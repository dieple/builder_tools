#!/bin/bash

export AWS_DEFAULT_REGION=eu-west-1

ROLE_ARN=$1
CI=$2

log() {
  echo "================================================================================"
  echo $@ | sed  -e :a -e 's/^.\{1,77\}$/ & /;ta'
  echo "================================================================================"
}

unset AWS_VAULT
unset AWS_SECURITY_TOKEN
if [[ ! -z "$CI" ]]; then  # if CI is set...
    temp_role=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "CI" $STS_OPTS)
else  # else we are running for the first time locally...
    temp_role=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "${ROLE_ARN}" $STS_OPTS)
fi
export AWS_ACCESS_KEY_ID=$(echo $temp_role | jq .Credentials.AccessKeyId | xargs)
export AWS_SECRET_ACCESS_KEY=$(echo $temp_role | jq .Credentials.SecretAccessKey | xargs)
export AWS_SESSION_TOKEN=$(echo $temp_role | jq .Credentials.SessionToken | xargs)
log "AWS session variables set for role: ${ROLE_ARN}"
