#!/bin/bash

set -x
set -e

if [[ $SYSTEM =~ nacl* ]]; then
  export NACL_SDK_ROOT=$PWD/nacl_sdk/pepper_45
fi

make -j4

make test
