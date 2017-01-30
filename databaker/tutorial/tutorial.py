#!/usr/bin/python
from __future__ import absolute_import, division, print_function

import os
import subprocess


def main():
    tutorial_dir = os.path.dirname(os.path.abspath(__file__))
    tutorial_filename = 'tutorial1.ipynb'
    tutorial_path = os.path.join(tutorial_dir, tutorial_filename)

    # shell=True not required for Windows, I don't think, only POSIX.
    cmd = 'jupyter notebook {}'.format(tutorial_path)
    print("Running command:", cmd)
    subprocess.Popen(cmd, shell=True)


if __name__ == '__main__':
    main()
