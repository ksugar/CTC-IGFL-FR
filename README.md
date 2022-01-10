[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ksugar/CTC-IGFL-FR/blob/main/CTC_IGFL_FR.ipynb)

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

## Working directory

All the following commands are supposed to be run in the `src/SW` directory. Please change your current directory as below to follow the instructions.

```bash
cd src/SW
```
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
miniconda/bin/python prep/convert_to_2d_labels.py ../../Data/YOUR_DATA
```

The following step is always required.

```bash
miniconda/bin/python prep/generate_seg_labels.py ../../Data/YOUR_DATA train_data/YOUR_DATA
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
| nmodels               | Number of models to train. If more than 1 models are trained, its outputs are averaged at evaluation phase.                            |

Dataset-specific parameters can be defined as follows (e.g. `YOUR_DATASET-GT-seg.json`).

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

In this case, the following file structure is expected.

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

Instead of manually preparing these files, [generate_train_config.py](src/SW/generate_train_config.py) can be used to generate an all-in-one config.

```bash
miniconda/bin/python generate_train_config.py training.json --dataset DIC-C2DH-HeLa/01-GT-seg DIC-C2DH-HeLa/02-GT-seg --model_name DIC-C2DH-HeLa-GT-seg.pth --log_dir DIC-C2DH-HeLa-GT-seg --n_epochs 100
```

<details>
<summary>Usage details</summary>
<pre>
usage: generate_train_config.py [-h] --dataset_name DATASET_NAME
                                [DATASET_NAME ...] --model_name MODEL_NAME
                                --log_dir LOG_DIR [--device DEVICE]
                                [--patch size [size ...]] [--lr LR]
                                [--n_crops N_CROPS] [--n_epochs N_EPOCHS]
                                [--auto_bg_thresh AUTO_BG_THRESH]
                                [--aug_scale_factor_base AUG_SCALE_FACTOR_BASE]
                                [--aug_rotation_angle AUG_ROTATION_ANGLE]
                                [--aug_contrast AUG_CONTRAST]
                                [--evalinterval EVALINTERVAL] [--is_3d]
                                [--batch_size BATCH_SIZE] [--nmodels NMODELS]
                                output<br>
positional arguments:
  output                Output file name<br>
optional arguments:
  -h, --help            show this help message and exit
  --dataset_name DATASET_NAME [DATASET_NAME ...]
                        Dataset path(es) relative to train_data/.
                        Usage: --dataset_name DIC-C2DH-HeLa/01-GT-seg DIC-C2DH-HeLa/02-GT-seg
  --model_name MODEL_NAME
                        Model file path relative to models/.This path is used to save the trained model.
                        Usage: --model_name DIC-C2DH-HeLa-GT-seg.pth
  --log_dir LOG_DIR     Log directory path relative to logs/.This path is used to save the trained model.
                        Usage: --log_dir DIC-C2DH-HeLa-GT-seg
  --device DEVICE       "cpu" or "cuda".
                        default: "cuda"
  --patch size [size ...]
                        Patch size used for training.
                        default: 128 128
  --lr LR               Learning rate.
                        default: 5e-4
  --n_crops N_CROPS     Number of crops per training epoch.
                        default: 1
  --n_epochs N_EPOCHS   Number of training epochs.
                        default: 500
  --auto_bg_thresh AUTO_BG_THRESH
                        Pixels with the value below auto_bg_thresh are recognized as background.
                        The value is based on normalized intensity between 0 and 1.
                        default: 0
  --aug_scale_factor_base AUG_SCALE_FACTOR_BASE
                        Used in data augmentation for scaling in the range [0, 1].
                        default: 0
  --aug_rotation_angle AUG_ROTATION_ANGLE
                        Used in data augmentation for rotation in the range [0, 180].
                        default: 0
  --aug_contrast AUG_CONTRAST
                        Used in data augmentation for contrast adjustment in the range [0, 1].
                        default: 0
  --evalinterval EVALINTERVAL
                        Every `evalinterval`th data will be used for evaluation (not used for training).
                        If -1 is given, all data is used for both training and evaluation.
                        default: 10
  --is_3d               Specify if data is 3D.
  --batch_size BATCH_SIZE
                        Training batch size.
                        default: 1
  --nmodels NMODELS     Number of models to train.
                        If more than 1 models are trained, its outputs are averaged at evaluation phase.
                        default: 1
</pre>
</details>

<details>
<summary>Output (<code>training.json</code>)</summary>
<pre>
[
    {
        "dataset_name": "DIC-C2DH-HeLa/01-GT-seg",
        "model_name": "DIC-C2DH-HeLa-GT-seg.pth",
        "log_dir": "DIC-C2DH-HeLa-GT-seg",
        "device": "cuda",
        "patch": [
            128,
            128
        ],
        "lr": 0.0005,
        "n_crops": 1,
        "n_epochs": 100,
        "auto_bg_thresh": 0.0,
        "aug_scale_factor_base": 0.0,
        "aug_rotation_angle": 0.0,
        "aug_contrast": 0.0,
        "evalinterval": 10,
        "is_3d": false,
        "batch_size": 1,
        "nmodels": 1
    },
    {
        "dataset_name": "DIC-C2DH-HeLa/02-GT-seg",
        "model_name": "DIC-C2DH-HeLa-GT-seg.pth",
        "log_dir": "DIC-C2DH-HeLa-GT-seg",
        "device": "cuda",
        "patch": [
            128,
            128
        ],
        "lr": 0.0005,
        "n_crops": 1,
        "n_epochs": 100,
        "auto_bg_thresh": 0.0,
        "aug_scale_factor_base": 0.0,
        "aug_rotation_angle": 0.0,
        "aug_contrast": 0.0,
        "evalinterval": 10,
        "is_3d": false,
        "batch_size": 1,
        "nmodels": 1
    }
]
</pre>
</details>

### 4. Run a training script

1. Using a `base` config and a dataset-specific config.

```bash
miniconda/bin/python train.py --baseconfig train_config/base_train_seg.json seg train_config/YOUR_DATASET_SPECIFIC_CONFIG.json
```

2. Using an all-in-one config.

```bash
miniconda/bin/python train.py seg train_config/YOUR_ALL_IN_ONE_CONFIG.json
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

| paramter                     | description                                                                                                                                                          |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| seg_model                    | Path to a model parameter file (<code>.pth</code>).                                                                                                                  |
| device                       | "cuda" or "cpu"                                                                                                                                                      |
| scales                       | Pixel/voxels sizes in physical scale in the order of [<code>X</code>, <code>Y</code>, <code>Z</code>].                                                               |
| c_ratio                      | Center ratio used to recover ellipses/ellipsoids from center prediction (generally it should be the same value as used in <code>prep/generate_generate_seg_labels.py |
| p_thresh                     | Probability threshold for prediction. Pixels with a central probability higher than this value are subject to further processing.                                    |
| r_min                        | Minimum threshold of radii of detections in physical scale. If at least one of the radii of a detection is smaller than this value, the detection is discarded.      |
| r_max                        | Maximum threshold of radii of detections in physical scale. The radii of a detection larger than <code>r_max</code> become <code>r_max</code>.                       |
| is_3d                        | `true` if data is 3D)                                                                                                                                                |
| use_2d                       | `true` should be specified always                                                                                                                                    |
| is_pad                       | `true` should be specified always                                                                                                                                    |
| use_opticalflow              | `false` should be specified always                                                                                                                                   |
| use_interpolation            | `true` if interpolation of missing spots is turned on                                                                                                                |
| linking_threshold            | Threshold value for linking in physical scale. Links with smaller values than this value are accepted.                                                               |
| search_depth                 | The linking algorithm tries to find the parent spot up to the current timepoint - <code>search_depth</code>.                                                         |
| search_neighbors             | The linking algorithm tries to find the parent spot up to <code>search_neighbors</code> in the target timepoint.                                                     |
| max_edges                    | The linking algorithm accepts <code>max_edges</code> links at maximum for each parent spot.                                                                          |
| division_min_displacement    | This value is combined with <code>division_acceptable_distance</code> to determin if a spot is dividing.                                                             |
| division_acceptable_distance | This value is combined with <code>division_min_displacement</code> to determin if a spot is dividing.                                                                |

<details>
<summary>Linking algorithm</summary>
Tracking is performed by looking up the parent spots in the previous timepoint by nearest-neighbour algorithm. The links with a distance smaller than <code>linking_threshold</code> are considered as link candidates. Each spot accepts <code>max_edges</code> links. If there are competing links, the link with a smaller displacement is adopted and the remaining spots look for the next closest spot up to <code>search_neighbors</code> neighbors. If no candidates are found in the current timepoint, the algorithm looks for the previous timepoints up to <code>search_depth</code> timepoints. This procedure was repeated up to five times to generate the links. In addition to this criteria, if two links from a parent spot are both smaller than <code>division_acceptable_distance</code>, the parent spot is also recognized as a dividing spot. The dividing spot would have larger displacement than <code>division_min_displacement</code> between two timepoints. If the spot is recognized as dividing, the spot accepts <code>max_edges</code> links at maximum, otherwise it accepts only one link regardless of <code>max_edges</code>.
</details>

Instead of manually preparing these files, [generate_run_config.py](src/SW/generate_run_config.py) can be used to generate a config file for inference.

```bash
miniconda/bin/python generate_run_config.py run.json --seg_model pretrained_models/allGT-seg.pth --scales 0.645 0.645 --c_ratio 0.5 --p_thresh 0.8 --r_min 1 --r_max 50 --use_interpolation
```

<details>
<summary>Usage details</summary>
<pre>
usage: generate_run_config.py [-h] --seg_model SEG_MODEL [--device DEVICE]
                              --scales size [size ...] [--c_ratio C_RATIO]
                              [--p_thresh P_THRESH] [--r_min R_MIN]
                              [--r_max R_MAX] [--is_3d] [--use_interpolation]
                              [--linking_threshold LINKING_THRESHOLD]
                              [--search_depth SEARCH_DEPTH]
                              [--search_neighbors SEARCH_NEIGHBORS]
                              [--max_edges MAX_EDGES]
                              [--division_min_displacement DIVISION_MIN_DISPLACEMENT]
                              [--division_acceptable_distance DIVISION_ACCEPTABLE_DISTANCE]
                              [--dryrun]
                              output<br>
positional arguments:
  output                Output file name<br>
optional arguments:
  -h, --help            show this help message and exit
  --seg_model SEG_MODEL
                        Path to a model parameter file (.pth).
  --device DEVICE       "cpu" or "cuda".
                        default: "cuda"
  --scales size [size ...]
                        Pixel/voxels sizes in physical scale in the order of [X, Y(, Z)].
  --c_ratio C_RATIO     Center ratio used to recover ellipses/ellipsoids from center prediction (generally it should be the same value as used in prep/generate_generate_seg_labels.py.
                        default: 0.3
  --p_thresh P_THRESH   Probability threshold for prediction. Pixels with a central probability higher than this value are subject to further processing.
                        default: 0.5
  --r_min R_MIN         Minimum threshold of radii of detections in physical scale. If at least one of the radii ofa detection is smaller than this value, the detection is discarded.
                        default: 0
  --r_max R_MAX         Maximum threshold of radii of detections in physical scale. The radii of a detection larger than r_max become r_max.
                        default: 1e6
  --is_3d               Specify if data is 3D.
  --use_interpolation   Specify if interpolation of missing spots is turned on.
  --linking_threshold LINKING_THRESHOLD
                        Threshold value for linking in physical scale.
                        Links with smaller values than this value are accepted.
                        default: 5.0
  --search_depth SEARCH_DEPTH
                        The linking algorithm tries to find the parent spot up to the current timepoint - search_depth.
                        default: 3
  --search_neighbors SEARCH_NEIGHBORS
                        The linking algorithm tries to find the parent spot up to search_neighbors in the target timepoint.
                        default: 3
  --max_edges MAX_EDGES
                        The linking algorithm accepts max_edges links at maximum for each parent spot.
                        default: 1
  --division_min_displacement DIVISION_MIN_DISPLACEMENT
                        This value is combined with division_acceptable_distance to determin if a spot is dividing.
                        default: 1.0
  --division_acceptable_distance DIVISION_ACCEPTABLE_DISTANCE
                        This value is combined with division_min_displacement to determin if a spot is dividing.
                        default: 1.0
  --dryrun              Print output to the console instead of a file.
</pre>
</details>

<details>
<summary>Output (<code>run.json</code>)</summary>
<pre>
{
    "seg_model": "pretrained_models/allGT-seg.pth",
    "device": "cuda",
    "scales": [
        0.645,
        0.645
    ],
    "c_ratio": 0.5,
    "p_thresh": 0.8,
    "r_min": 1.0,
    "r_max": 50.0,
    "is_3d": false,
    "use_interpolation": true,
    "linking_threshold": 5.0,
    "search_depth": 3,
    "search_neighbors": 3,
    "max_edges": 1,
    "division_min_displacement": 1.0,
    "division_acceptable_distance": 1.0,
    "use_2d": true,
    "is_pad": true,
    "use_opticalflow": false
}
</pre>
</details>

### 3. Run a Java program for inference

Run the executable `.jar` with three input parameters:

```bash
# usage: java -jar elephant-ctc-0.1.0.jar INPUT_SEQUENCE OUTPUT_SEQUENCE CONFIG_FILE
java -jar elephant-ctc-0.1.0.jar "../../Data/DIC-C2DH-HeLa/01" "../../Data/DIC-C2DH-HeLa/01_RES-allGT" "run_configs/DIC-C2DH-HeLa-01-allGT.json"
```

Details of the parameters are shown below:

- `INPUT_SEQUENCE`: A directory that includes images to analyze. The directory should contain .tif files for each timepoint.

```bash
Data/
├── DIC-C2DH-HeLa
│   ├── 01
│   │   ├── t000.tif
│   │   ├── t001.tif
│   │   ...
```

- `OUTPUT_SEQUENCE`: A directory that stores the results in the following structure. The results are stored in .tif format for each timepoint.

```bash
Data/
├── DIC-C2DH-HeLa
│   ├── 01_RES-allGT
│   │   ├── mask000.tif
│   │   ├── mask001.tif
│   │   ...
```

- `CONFIG_FILE`: The config file for inferece, as explained in the previous section.

The source code for the java program can be found [here](https://github.com/ksugar/elephant-ctc).