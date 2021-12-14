#!/usr/bin/env bash
base_path=$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)
cd "$base_path"
usage="usage: $(basename "$0") [-h]

------- Listing options -------
  -h  show this help text"

mkdir -p lib
echo "Downloading pretrained models"
wget -nc https://github.com/ksugar/CTC-IGFL-FR/releases/download/6th-ctc-primary/pretrained_models.zip
unzip -n pretrained_models.zip
rm pretrained_models.zip
