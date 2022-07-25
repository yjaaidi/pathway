#!/usr/bin/env sh

conda install -c conda-forge $@
conda env export -n pathway > environment.yml
