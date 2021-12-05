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

## Prepare training data

```bash
./prep.sh
```

## Run a training script

```bash
./train-DIC-C2DH-HeLa.sh
```