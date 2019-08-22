#!/usr/bin/env bash

PROFILE=$1

usage(){
cat <<!
$(basename $0) - check to see if a column exists in an object

Usage: $(basename $0) <Profile>
!
}

check_params(){

if [ $# -ne 1 ]
then
    echo "Error: Incorrect number of arguments" >&2
    usage >&2
    exit 1
fi
}


####
# Main
####

check_params $PROFILE

# Modify to meet your env!
#	--shareHostVolume=$HOME/repos Directory on your host which contains your git repos

python ./builder.py --githubUsername=dieple \
	--githubEmail=dieple1@gmail.com \
	--terraformVersion=0.11.13 \
	--installTerraform=true \
	--dockerAppUser=dataops \
	--profile=$PROFILE \
	--shareHostVolume=$HOME/repos \
	--imageName=$PROFILE



