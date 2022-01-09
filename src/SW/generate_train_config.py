#! /usr/bin/env python
# ==============================================================================
# Copyright (c) 2022, Ko Sugawara
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
"""Commandline interface for generating a config file for training."""

import argparse
from argparse import RawTextHelpFormatter
import json


def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('output',
                        type=str,
                        help='Output file name')
    parser.add_argument('--dataset_name',
                        type=str,
                        nargs='+',
                        help=(
                            'Dataset path(es) relative to train_data/.\n' +
                            'Usage: --dataset_name DIC-C2DH-HeLa/01-GT-seg ' +
                            'DIC-C2DH-HeLa/02-GT-seg'
                        ),
                        required=True
                        )
    parser.add_argument('--model_name',
                        type=str,
                        help=(
                            'Model file path relative to models/.' +
                            'This path is used to save the trained model.\n' +
                            'Usage: --model_name DIC-C2DH-HeLa-GT-seg.pth'
                        ),
                        required=True
                        )
    parser.add_argument('--log_dir',
                        type=str,
                        help=(
                            'Log directory path relative to logs/.' +
                            'This path is used to save the trained model.\n' +
                            'Usage: --log_dir DIC-C2DH-HeLa-GT-seg'
                        ),
                        required=True
                        )
    parser.add_argument('--device',
                        type=str,
                        help='\"cpu\" or \"cuda\".\ndefault: \"cuda\"',
                        default='cuda')
    parser.add_argument('--patch',
                        metavar='size',
                        type=int,
                        nargs='+',
                        help='Patch size used for training.\ndefault: 128 128',
                        default=[128, 128])
    parser.add_argument('--lr',
                        type=float,
                        help='Learning rate.\ndefault: 5e-4',
                        default=5e-4)
    parser.add_argument('--n_crops',
                        type=int,
                        help='Number of crops per training epoch.\ndefault: 1',
                        default=1)
    parser.add_argument('--n_epochs',
                        type=int,
                        help='Number of training epochs.\ndefault: 500',
                        default=500)
    parser.add_argument('--auto_bg_thresh',
                        type=float,
                        help=(
                            'Pixels with the value below auto_bg_thresh are ' +
                            'recognized as background.\nThe value is based on ' +
                            'normalized intensity between 0 and 1.\ndefault: 0'
                        ),
                        default=0.0)
    parser.add_argument('--aug_scale_factor_base',
                        type=float,
                        help=(
                            'Used in data augmentation for scaling in the ' +
                            'range [0, 1].\ndefault: 0'
                        ),
                        default=0.0)
    parser.add_argument('--aug_rotation_angle',
                        type=float,
                        help=(
                            'Used in data augmentation for rotation in the ' +
                            'range [0, 180].\ndefault: 0'
                        ),
                        default=0.0)
    parser.add_argument('--aug_contrast',
                        type=float,
                        help=(
                            'Used in data augmentation for contrast ' +
                            'adjustment in the range [0, 1].\ndefault: 0'
                        ),
                        default=0.0)
    parser.add_argument('--evalinterval',
                        type=int,
                        help=(
                            'Every `evalinterval`th data will be used for ' +
                            'evaluation (not used for training).\n' +
                            'If -1 is given, all data is used for both ' +
                            'training and evaluation.\ndefault: 10'
                        ),
                        default=10)
    parser.add_argument('--is_3d',
                        help=('Specify if data is 3D.'),
                        action='store_true')
    parser.add_argument('--batch_size',
                        type=int,
                        help=('Training batch size.\ndefault: 1'),
                        default=1)
    parser.add_argument('--nmodels',
                        type=int,
                        help=(
                            'Number of models to train.\nIf more than 1 ' +
                            'models are trained, its outputs are averaged at ' +
                            'evaluation phase.\ndefault: 1'),
                        default=1)
    parser.add_argument('--dryrun',
                        help=('Print output to the console instead of a file.'),
                        action='store_true')
    args = parser.parse_args()
    if args.device not in ('cpu', 'cuda'):
        raise ValueError('--device should be \"cpu\" or \"cuda\"')
    if len(args.patch) != 2 + args.is_3d:
        raise ValueError(f'--patch should have the length {2 + args.is_3d}')
    if args.n_crops < 1:
        raise ValueError('--n_crops should be a positive value')
    if args.n_epochs < 0:
        raise ValueError('--n_epochs should be a positive value')
    if not 0 <= args.auto_bg_thresh <= 1:
        raise ValueError('--auto_bg_thresh should be in the range [0, 1]')
    if not 0 <= args.aug_scale_factor_base <= 1:
        raise ValueError(
            '--aug_scale_factor_base should be in the range [0, 1]'
        )
    if not 0 <= args.aug_rotation_angle <= 180:
        raise ValueError(
            '--aug_rotation_angle should be in the range [0, 180]'
        )
    if not 0 <= args.aug_contrast <= 1:
        raise ValueError('--aug_contrast should be in the range [0, 1]')
    if args.evalinterval < -1:
        raise ValueError('--evalinterval should be greater than -1')
    if args.batch_size < 1:
        raise ValueError('--batch_size should be a positive value')
    if args.nmodels < 1:
        raise ValueError('--nmodels should be a positive value')
    config_dict = vars(args).copy()
    config_dicts = []
    config_dict.pop('output')
    config_dict.pop('dryrun')
    for dataset in args.dataset_name:
        config_dict['dataset_name'] = dataset
        config_dicts.append(config_dict.copy())
    if args.dryrun:
        print(json.dumps(config_dicts, indent=4))
    else:
        with open(args.output, "w") as outfile:
            json.dump(config_dicts, outfile, indent=4)


if __name__ == '__main__':
    main()
