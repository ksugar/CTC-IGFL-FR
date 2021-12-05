#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
usage="usage: $(basename "$0") [-h] [-a] DATASET_NAME1 DATASET_NAME2 ...

------- Listing options -------
  -h  show this help text
  -a  download all datasets"

function download_and_extract {
    wget -O ../../Data/$1.zip http://data.celltrackingchallenge.net/training-datasets/$1.zip
    unzip -d ../../Data/ -qo ../../Data/$1.zip
    chmod -R 775 ../../Data/$1
    rm ../../Data/$1.zip
}

while [[ $# -gt 0 ]]; do
    case "$1" in
    -a | --all)
        download_and_extract "BF-C2DL-HSC"
        download_and_extract "BF-C2DL-MuSC"
        download_and_extract "DIC-C2DH-HeLa"
        download_and_extract "Fluo-C2DL-MSC"
        download_and_extract "Fluo-C3DH-A549"
        download_and_extract "Fluo-C3DH-H157"
        download_and_extract "Fluo-C3DL-MDA231"
        download_and_extract "Fluo-N2DH-GOWT1"
        download_and_extract "Fluo-N2DL-HeLa"
        download_and_extract "Fluo-N3DH-CE"
        download_and_extract "Fluo-N3DH-CHO"
        download_and_extract "PhC-C2DH-U373"
        download_and_extract "PhC-C2DL-PSC"
        exit 0
        ;;
    -h | --help)
        echo "$usage"
        exit 0
        ;;
    *)
        download_and_extract "$1"
        shift
        ;;
    esac
done
