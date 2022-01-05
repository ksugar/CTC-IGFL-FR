# CTC-IGFL-FR
Source Code used in the Cell Tracking Challenge

## Prerequisites

- Linux OS (64-bit)
  - We tested our scripts on Ubuntu 18.04.
  - Windows and macOS are not supported.
- Commands
  - wget
  - unzip
- Internet connection
  - It is required to install Miniconda and Python modules.
  - Once the environment is set up, the script should work without internet connection.
- GPU
  - GPU should be compatible with `CUDA 10.1.243` (see [details](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn_765/cudnn-support-matrix/index.html))
    - NVIDIA Ampere Architecture (e.g. GeForce RTX 3090, RTX A6000, Nvidia A100) is not supported
  - NVIDIA driver version should be `>= 418.39`
  - If more than one NVIDIA GPU is available, the first device will be used by default. To use another GPU device, set the environment variable `CUDA_VISIBLE_DEVICES`.
- Java
  - Java Runtime Environment 8 or higher (e.g. [AdoptOpenJDK](https://adoptopenjdk.net/)) is required to run the inference program.

## Prepare data

The `Data/` directory should have the same structure as the one provided in the CTC.

```bash
Data/
├── DIC-C2DH-HeLa
│   ├── 01
│   │   ├── t000.tif
│   │   ├── t001.tif
│   │   ...
│   ├── 01_GT
│   │   ├── SEG
│   │   └── TRA
│   ├── 01_ST
│   │   └── SEG
...
```

You can download the training data from the CTC website with the following command.

```bash
# download all datasets
./download_data.sh -a
```

```bash
# download by selection
./download_data.sh DIC-C2DH-HeLa Fluo-C3DL-MDA231
```

## Create a Conda environment

```bash
./create_env.sh
```

## Generate training dataset

```bash
./prep.sh
```

## Run a training script

```bash
./train-DIC-C2DH-HeLa.sh
```

## Train a model with your data

### 1. Prepare data

Place your data under the `Data/` directory. It should have the same structure as the one provided in the CTC.

```bash
Data/
├── YOUR_DATA
│   ├── 01
│   │   ├── t000.tif
│   │   ├── t001.tif
│   │   ...
│   └── 01_GT
│       └── SEG
│           ├── man_seg000.tif
│           ├── man_seg001.tif
│           ...
...
```

### 2. Generate training dataset

(Optional) The following step is required only when your data is 3D.

```bash
../miniconda/bin/python prep/convert_to_2d_labels.py ../../../Data/YOUR_DATA
```

The following step is always required.

```bash
../miniconda/bin/python prep/generate_seg_labels.py ../../../Data/YOUR_DATA ../train_data/YOUR_DATA
```

### 3. Prepare training config files

[base_train_seg.json](src/SW/train_config/base_train_seg.json) can be used as a base configuration.

```
{
    "device": "cuda",
    "patch": [
        128,
        128
    ],
    "lr": 5e-4,
    "n_crops": 1,
    "n_epochs": 500,
    "auto_bg_thresh": 0,
    "aug_scale_factor_base": 0,
    "aug_rotation_angle": 0,
    "aug_contrast": 0,
    "evalinterval": 10,
    "is_3d": false,
    "batch_size": 1,
    "nmodels": 1
}
```

| paramter              | description                                                                                                                            |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| device                | "cuda" or "cpu"                                                                                                                        |
| patch                 | Patch size used for training                                                                                                           |
| lr                    | Learning rate                                                                                                                          |
| n_crops               | Number of crops per training epoch                                                                                                     |
| n_epochs              | Number of training epochs                                                                                                              |
| auto_bg_thresh        | Pixels with the value below `auto_bg_thresh` are recognized as background. The value is based on normalized intensity between 0 and 1. |
| aug_scale_factor_base | Used in data augmentation for scaling ([0, 1]))                                                                                        |
| aug_rotation_angle    | Used in data augmentation for rotation ([0, 180]))                                                                                     |
| aug_contrast          | Used in data augmentation for contrast adjustment ([0, 1]))                                                                            |
| evalinterval          | Every `evalinterval`th data will be used for evaluation (not used for training)                                                        |
| is_3d                 | `true` if data is 3D                                                                                                                   |
| batch_size            | Training batch size                                                                                                                    |
| nmodels               | Number of models to train. If more than 1 models are trained, its outputs are averaged at evaluation phase. size                       |

Dataset-specific parameters can be defined as follows (e.g. `YOUR_DATASET-GT-seg.json`).

```
SW/
├── train_data
│   └── YOUR_DATASET
│       ├── 01-GT-seg
│       │   ├── imgs.zarr
│       │   └── seg_labels.zarr
│       └── 02-GT-seg
│           ├── imgs.zarr
│           └── seg_labels.zarr
├── models
│   ├── YOUR_DATASET-GT-seg.pth (the file will be created if not exists)
│   ...
├── logs
│   ├── YOUR_DATASET-GT-seg (the directory will be created if not exists)
│   ...
...
```

```bash
[
    {
        "dataset_name": "YOUR_DATASET/01-GT-seg",
        "model_name": "YOUR_DATASET-GT-seg.pth",
        "log_dir": "YOUR_DATASET-seg"
    },
    {
        "dataset_name": "YOUR_DATASET/02-GT-seg",
        "model_name": "YOUR_DATASET-GT-seg.pth",
        "log_dir": "YOUR_DATASET-GT-seg"
    }
]
```

### 4. Run a training script

```bash
miniconda/bin/python train.py --baseconfig train_config/base_train_seg.json seg train_config/YOUR_DATASET-GT-seg.json
```

## Run inference with a trained model

You need Java Runtime Environment 8 or higher (e.g. [AdoptOpenJDK](https://adoptopenjdk.net/)) to run the inference program.

### 0. (Optional) Download pretrained models

The following command will download pretrained modesl in the `pretrained_models/` directory.

```bash
./download_pretrained_models.sh
```

### 1. Download required libraries

```bash
./download_libraries.sh
```

### 2. Prepare inference config files

A config file for inferece looks like the following example.
More example config files can be found at the [run_configs](src/SW/run_configs/) directory.

```json
{
    "seg_model": "pretrained_models/allGT-seg.pth",
    "device": "cuda",
    "scales": [
        0.645, 0.645
    ],
    "c_ratio": 0.5,
    "p_thresh": 0.8,
    "r_min": 1,
    "r_max": 50,
    "is_3d": false,
    "use_2d": true,
    "is_pad": true,
    "use_opticalflow": false,
    "use_interpolation": true,
    "linking_threshold": 5.0,
    "search_depth": 3,
    "search_neighbors": 3,
    "max_edges": 1,
    "division_min_displacement": 1.0,
    "division_acceptable_distance": 1.0
}
```

| paramter                     | description                                                                                                                                                                                             |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| seg_model                    | Path to a model parameter file (<code>.pth</code>)                                                                                                                                                      |
| device                       | "cuda" or "cpu"                                                                                                                                                                                         |
| scales                       | Pixel/voxels sizes in physical scale in the order of [<code>X</code>, <code>Y</code>, <code>Z</code>].                                                                                                  |
| c_ratio                      | Center ratio used to recover ellipses/ellipsoids from center prediction (generally it should be the same value as used in <code>prep/generate_generate_seg_labels.py</code> (default: <code>0.3</code>) |
| p_thresh                     | Probability threshold for prediction. Pixels with a central probability higher than this value are subject to further processing.                                                                       |
| r_min                        | Minimum threshold of radii of detections in physical scale. If at least one of the radii of a detection is smaller than this value, the detection is discarded.                                         |
| r_max                        | Maximum threshold of radii of detections in physical scale. The radii of a detection larger than <code>r_max</code> become <code>r_max</code>.                                                          |
| is_3d                        | `true` if data is 3D)                                                                                                                                                                                   |
| use_2d                       | `true` should be specified always                                                                                                                                                                       |
| is_pad                       | `true` should be specified always                                                                                                                                                                       |
| use_opticalflow              | `false` should be specified always                                                                                                                                                                      |
| use_interpolation            | `true` if interpolation of missing spots is turned on                                                                                                                                                   |
| linking_threshold            | Threshold value for linking in physical scale. Links with smaller values than this value are accepted.                                                                                                  |
| search_depth                 | The linking algorithm tries to find the parent spot up to the current timepoint - <code>search_depth</code>.                                                                                            |
| search_neighbors             | The linking algorithm tries to find the parent spot up to <code>search_neighbors</code> in the target timepoint.                                                                                        |
| max_edges                    | The linking algorithm accepts <code>max_edges</code> links at maximum for each parent spot.                                                                                                             |
| division_min_displacement    | This value is combined with <code>division_acceptable_distance</code> to determin if a spot is dividing.                                                                                                |
| division_acceptable_distance | This value is combined with <code>division_min_displacement</code> to determin if a spot is dividing                                                                                                    |

<details>
<summary>Linking algorithm</summary>
Tracking is performed by looking up the parent spots in the previous timepoint by nearest-neighbour algorithm. The links with a distance smaller than <code>linking_threshold</code> are considered as link candidates. Each spot accepts <code>max_edges</code> links. If there are competing links, the link with a smaller displacement is adopted and the remaining spots look for the next closest spot up to <code>search_neighbors</code> neighbors. If no candidates are found in the current timepoint, the algorithm looks for the previous timepoints up to <code>search_depth</code> timepoints. This procedure was repeated up to five times to generate the links. In addition to this criteria, if two links from a parent spot are both smaller than <code>division_acceptable_distance</code>, the parent spot is also recognized as a dividing spot. The dividing spot would have larger displacement than <code>division_min_displacement</code> between two timepoints. If the spot is recognized as dividing, the spot accepts <code>max_edges</code> links at maximum, otherwise it accepts only one link regardless of <code>max_edges</code>.
</details>

### 3. Run a Java program for inference

Run the executable `.jar` with three input parameters:

```bash
# usage: java -jar elephant-ctc-0.1.0.jar INPUT_SEQUENCE OUTPUT_SEQUENCE CONFIG_FILE
java -jar elephant-ctc-0.1.0.jar "../../Data/DIC-C2DH-HeLa/01" "../../Data/DIC-C2DH-HeLa/01_RES-allGT" "run_configs/DIC-C2DH-HeLa-01-allGT.json"
```

The source code for the java program can be found [here](https://github.com/ksugar/elephant-ctc).