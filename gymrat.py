#!/usr/bin/env python

import os
import sys
import time
import itertools
import numpy as np
import argparse
import logging

import gym
from gym_recording.wrappers import TraceRecordingWrapper

from atari import HumanAtariController

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('env_name', type=str)
    parser.add_argument('--reps', default=1, type=int)
    parser.add_argument('--tracedir', type=str)

    args = parser.parse_args()

    logging.basicConfig(format='%(levelname)s:%(name)s %(message)s',
            level=logging.DEBUG)

    if args.tracedir is None:
        args.tracedir = os.path.join(THIS_DIR, 'traces')
    args.tracedir = os.path.join(args.tracedir, args.env_name)
    os.makedirs(args.tracedir, exist_ok=True)

    controller = HumanAtariController(args.env_name, args.tracedir)

    for epoch_i in range(args.reps):
        controller.play()

    controller.env.close()

