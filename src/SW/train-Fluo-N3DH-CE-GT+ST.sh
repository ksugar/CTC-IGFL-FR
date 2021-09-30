#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
miniconda/bin/python train.py --baseconfig config/base_train_seg.json seg config/Fluo-N3DH-CE-GT+ST-seg.json
