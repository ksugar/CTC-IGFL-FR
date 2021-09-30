#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
../create_env.sh
../miniconda/bin/python convert_to_2d_labels.py --gt ../../../Data/Fluo-C3DH-A549
../miniconda/bin/python convert_to_2d_labels.py ../../../Data/Fluo-C3DH-H157
../miniconda/bin/python convert_to_2d_labels.py ../../../Data/Fluo-C3DL-MDA231
../miniconda/bin/python convert_to_2d_labels.py ../../../Data/Fluo-N3DH-CE
../miniconda/bin/python convert_to_2d_labels.py ../../../Data/Fluo-N3DH-CHO
