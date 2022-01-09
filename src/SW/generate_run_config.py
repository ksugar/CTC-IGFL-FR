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
"""Commandline interface for generating a config file for inference."""

import argparse
from argparse import RawTextHelpFormatter
import json


def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('output',
                        type=str,
                        help='Output file name')
    parser.add_argument('--seg_model',
                        type=str,
                        help='Path to a model parameter file (.pth).',
                        required=True)
    parser.add_argument('--device',
                        type=str,
                        help='\"cpu\" or \"cuda\".\ndefault: \"cuda\"',
                        default='cuda')
    parser.add_argument('--scales',
                        metavar='size',
                        type=float,
                        nargs='+',
                        help=(
                            'Pixel/voxels sizes in physical scale in the ' +
                            'order of [X, Y(, Z)].'),
                        required=True)
    parser.add_argument('--c_ratio',
                        type=float,
                        help=(
                            'Center ratio used to recover ellipses/ellipsoids' +
                            ' from center prediction (generally it should be ' +
                            'the same value as used in ' +
                            'prep/generate_generate_seg_labels.py.\n' +
                            'default: 0.3'
                        ),
                        default=0.3)
    parser.add_argument('--p_thresh',
                        type=float,
                        help=(
                            'Probability threshold for prediction. Pixels with ' +
                            'a central probability higher than this value are ' +
                            'subject to further processing.\ndefault: 0.5'
                        ),
                        default=0.5)
    parser.add_argument('--r_min',
                        type=float,
                        help=(
                            'Minimum threshold of radii of detections in ' +
                            'physical scale. If at least one of the radii of' +
                            'a detection is smaller than this value, the ' +
                            'detection is discarded.\ndefault: 0'
                        ),
                        default=0)
    parser.add_argument('--r_max',
                        type=float,
                        help=(
                            'Maximum threshold of radii of detections in ' +
                            'physical scale. The radii of a detection larger ' +
                            'than r_max become r_max.\ndefault: 1e6'
                        ),
                        default=1e6)
    parser.add_argument('--is_3d',
                        help=('Specify if data is 3D.'),
                        action='store_true')
    parser.add_argument('--use_interpolation',
                        help=(
                            'Specify if interpolation of missing spots is ' +
                            'turned on.'
                        ),
                        action='store_true')
    parser.add_argument('--linking_threshold',
                        type=float,
                        help=(
                            'Threshold value for linking in physical scale.\n' +
                            'Links with smaller values than this value are ' +
                            'accepted.\ndefault: 5.0'
                        ),
                        default=5.0)
    parser.add_argument('--search_depth',
                        type=int,
                        help=(
                            'The linking algorithm tries to find the parent ' +
                            'spot up to the current timepoint - search_depth.' +
                            '\ndefault: 3'
                        ),
                        default=3)
    parser.add_argument('--search_neighbors',
                        type=int,
                        help=(
                            'The linking algorithm tries to find the parent ' +
                            'spot up to search_neighbors in the target ' +
                            'timepoint.\ndefault: 3'
                        ),
                        default=3)
    parser.add_argument('--max_edges',
                        type=int,
                        help=(
                            'The linking algorithm accepts max_edges links ' +
                            'at maximum for each parent spot.\ndefault: 1'
                        ),
                        default=1)
    parser.add_argument('--division_min_displacement',
                        type=float,
                        help=(
                            'This value is combined with ' +
                            'division_acceptable_distance to determin if a ' +
                            'spot is dividing.\ndefault: 1.0'
                        ),
                        default=1.0)
    parser.add_argument('--division_acceptable_distance',
                        type=float,
                        help=(
                            'This value is combined with ' +
                            'division_min_displacement to determin if a ' +
                            'spot is dividing.\ndefault: 1.0'
                        ),
                        default=1.0)
    parser.add_argument('--dryrun',
                        help=('Print output to the console instead of a file.'),
                        action='store_true')
    args = parser.parse_args()
    if args.device not in ('cpu', 'cuda'):
        raise ValueError('--device should be \"cpu\" or \"cuda\"')
    if len(args.scales) != 2 + args.is_3d:
        raise ValueError(f'--scales should have the length {2 + args.is_3d}')
    if not 0 <= args.c_ratio <= 1:
        raise ValueError('--c_ratio should be in the range [0, 1]')
    if not 0 <= args.p_thresh <= 1:
        raise ValueError('--p_thresh should be in the range [0, 1]')
    if args.r_min < 0:
        raise ValueError('--r_min should not be a negative value')
    if args.r_max < 0:
        raise ValueError('--r_max should not be a negative value')
    if args.r_max < args.r_min:
        raise ValueError('--r_max should be equal or greater than r_min')
    if args.linking_threshold < 0:
        raise ValueError('--linking_threshold should not be a negative value')
    if args.search_depth < 1:
        raise ValueError('--search_depth should be a positive value')
    if args.search_neighbors < 1:
        raise ValueError('--search_neighbors should be a positive value')
    if args.max_edges < 1:
        raise ValueError('--max_edges should be a positive value')
    if args.division_min_displacement < 0:
        raise ValueError(
            '--division_min_displacement should not be a negative value'
        )
    if args.division_acceptable_distance < 0:
        raise ValueError(
            '--division_acceptable_distance should not be a negative value'
        )
    config_dict = vars(args).copy()
    config_dict.pop('output')
    config_dict.pop('dryrun')
    config_dict['use_2d'] = True
    config_dict['is_pad'] = True
    config_dict['use_opticalflow'] = False
    if args.dryrun:
        print(json.dumps(config_dict, indent=4))
    else:
        with open(args.output, "w") as outfile:
            json.dump(config_dict, outfile, indent=4)


if __name__ == '__main__':
    main()
