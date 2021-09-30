#!/usr/bin/env bash
base_path=$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)
cd "$base_path"
../create_env.sh
# ../miniconda/bin/python generate_seg_labels.py --cr 0.3 ../../../Data/BF-C2DL-HSC ../train_data/BF-C2DL-HSC
# ../miniconda/bin/python generate_seg_labels.py --cr 0.5 ../../../Data/BF-C2DL-MuSC ../train_data/BF-C2DL-MuSC
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/DIC-C2DH-HeLa_sparse.json --cr 0.5 ../../../Data/DIC-C2DH-HeLa ../train_data/DIC-C2DH-HeLa
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-C2DL-MSC_sparse.json --cr 0.5 ../../../Data/Fluo-C2DL-MSC ../train_data/Fluo-C2DL-MSC
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-N2DH-GOWT1_sparse.json --cr 0.5 ../../../Data/Fluo-N2DH-GOWT1 ../train_data/Fluo-N2DH-GOWT1
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-N2DL-HeLa_sparse.json --cr 0.5 ../../../Data/Fluo-N2DL-HeLa ../train_data/Fluo-N2DL-HeLa
# ../miniconda/bin/python generate_seg_labels.py --cr 0.5 ../../../Data/PhC-C2DH-U373 ../train_data/PhC-C2DH-U373
# ../miniconda/bin/python generate_seg_labels.py --cr 0.5 ../../../Data/PhC-C2DL-PSC ../train_data/PhC-C2DL-PSC
# ../miniconda/bin/python generate_seg_labels.py --cr 0.3 ../../../Data/Fluo-C3DH-A549 ../train_data/Fluo-C3DH-A549
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-C3DH-H157_sparse.json --cr 0.3 ../../../Data/Fluo-C3DH-H157 ../train_data/Fluo-C3DH-H157
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-C3DL-MDA231_sparse.json --cr 0.3 ../../../Data/Fluo-C3DL-MDA231 ../train_data/Fluo-C3DL-MDA231
# ../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-N3DH-CE_sparse.json --cr 0.3 ../../../Data/Fluo-N3DH-CE ../train_data/Fluo-N3DH-CE
../miniconda/bin/python generate_seg_labels.py --sparse sparse_list/Fluo-N3DH-CHO_sparse.json --cr 0.3 ../../../Data/Fluo-N3DH-CHO ../train_data/Fluo-N3DH-CHO
