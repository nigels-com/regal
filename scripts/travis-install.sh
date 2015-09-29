#!/bin/bash

set -x
set -e

if [[ $SYSTEM =~ nacl* ]]; then
  wget http://storage.googleapis.com/nativeclient-mirror/nacl/nacl_sdk/nacl_sdk.zip
  unzip nacl_sdk.zip
  nacl_sdk/naclsdk update --force pepper_45
fi
