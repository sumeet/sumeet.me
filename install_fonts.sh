#!/bin/bash
set -e
[ $(uname -s) == "Linux" ] &&
    echo "Linux detected, installing fonts to ~/.fonts" &&
    mkdir -p ~/.fonts &&
    cp *.otf *.ttc ~/.fonts/
exit 0
