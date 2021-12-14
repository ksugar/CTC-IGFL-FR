#/bin/bash
if [ ! -d miniconda ]; then
    wget https://repo.anaconda.com/miniconda/Miniconda3-py38_4.8.3-Linux-x86_64.sh -O miniconda.sh
    chmod +x miniconda.sh
    ./miniconda.sh -b -p miniconda
    miniconda/bin/conda env update -f environment.yml
fi
miniconda/bin/python run_elephant.py "$@"
