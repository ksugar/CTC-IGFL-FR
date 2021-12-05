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

## Prepare data

The `Data/` directory should have the same structure as the one provided in the CTC.

```bash
Data/
├── DIC-C2DH-HeLa
│   ├── 01
│   │   ├── t000.tif
│   │   ├── t001.tif
│   │   ...
│   ├── 01_GT
│   │   ├── SEG
│   │   └── TRA
│   ├── 01_ST
│   │   └── SEG
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
│   │   ├── t000.tif
│   │   ├── t001.tif
│   │   ...
│   └── 01_GT
│       └── SEG
│           ├── man_seg000.tif
│           ├── man_seg001.tif
│           ...
...
```

### 2. Generate training dataset

(Optional) The following step is required only when your data is 3D.

```bash
../miniconda/bin/python convert_to_2d_labels.py ../../../Data/YOUR_DATA
```

The following step is always required.

```bash
../miniconda/bin/python generate_seg_labels.py ../../../Data/YOUR_DATA ../train_data/YOUR_DATA
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