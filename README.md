# CTC-IGFL-FR
Source Code used in the Cell Tracking Challenge

## Prerequisites

- Linux OS (64-bit)
  - We tested our scripts on Ubuntu 18.04.
  - Windows and macOS are not supported.
- Internet connection
  - It is required to install Miniconda and Python modules.
  - Once the environment is set up, the script should work without internet connection.

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
./train-BF-C2DL-HSC-GT.sh
```