#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
miniconda/bin/python train.py --baseconfig train_config/base_train_seg.json seg train_config/Fluo-N2DL-HeLa-ST-seg.json
