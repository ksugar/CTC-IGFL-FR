#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
miniconda/bin/python train.py --baseconfig train_config/base_train_seg.json seg train_config/PhC-C2DH-U373-GT-seg.json
