# CTC-IGFL-FR
Source Code used in the Cell Tracking Challenge

## Prerequisites

- Linux OS (64-bit)
  - We tested our scripts on Ubuntu 18.04.
  - Windows and macOS are not supported.
- Internet connection
  - It is required to install Miniconda and Python modules.
  - Once the environment is set up, the script should work without internet connection.

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