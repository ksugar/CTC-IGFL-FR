#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
prep/convert_to_2d_labels.sh
prep/generate_seg_labels.sh
