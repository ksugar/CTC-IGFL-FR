#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
if [ ! -d miniconda ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh -O miniconda.sh
    chmod +x miniconda.sh
    ./miniconda.sh -b -p miniconda
    miniconda/bin/conda env update -f environment.yml
    miniconda/bin/conda env update -f environment-train.yml
fi
