#!/bin/bash

USER_NAME=$1
VERSION=0.0.1

if [ -z ${USER_NAME} ]; then
	echo "Please specify docker hub user name"
    exit 1
fi

docker build -t ${USER_NAME}/bridge_bidding_env:v${VERSION} .
