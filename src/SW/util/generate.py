#! /usr/bin/env python
# ==============================================================================
# Copyright (c) 2021, Ko Sugawara
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1.  Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
# 2.  Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ==============================================================================
"""Generate config files for the CTC 6th challenge (ISBI2021)."""
import argparse
from string import Template
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', help='template bash script')
    args = parser.parse_args()
    datasets = [
        'BF-C2DL-HSC',
        'BF-C2DL-MuSC',
        'DIC-C2DH-HeLa',
        'Fluo-C2DL-MSC',
        'Fluo-N2DH-GOWT1',
        'Fluo-N2DL-HeLa',
        'PhC-C2DH-U373',
        'PhC-C2DL-PSC',
        'Fluo-C3DH-A549',
        'Fluo-C3DH-H157',
        'Fluo-C3DL-MDA231',
        'Fluo-N3DH-CE',
        'Fluo-N3DH-CHO',
    ]
    p = Path(__file__).parent.parent
    with open(args.template, 'r') as f:
        src = Template(f.read())
    for dataset in datasets:
        for cfg in ('GT', 'ST', 'GT+ST'):
            name = f'{dataset}-{cfg}'
            result = src.substitute({
                'name': name,
            })
            with open(str(p / f'train-{dataset}-{cfg}.sh'), 'w') as f:
                f.write(result)
    for name in ('allGT', 'allST', 'allGT+allST'):
        result = src.substitute({
            'name': name,
        })
        with open(str(p / f'train-{name}.sh'), 'w') as f:
            f.write(result)


if __name__ == '__main__':
    main()
