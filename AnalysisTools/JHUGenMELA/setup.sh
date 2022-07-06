#!/bin/sh

(
cd $(dirname ${BASH_SOURCE[0]})
pushd MELA &> /dev/null
./setup.sh "$@" || exit 1
popd &> /dev/null
)
