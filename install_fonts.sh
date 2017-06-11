#!/bin/bash
[ $(uname -s) == "Linux" ] &&
    echo "Linux detected, installing fonts to ~/.fonts" &&
    mkdir -p ~/.fonts &&
    cp *.otf ~/.fonts/
