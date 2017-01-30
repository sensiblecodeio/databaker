#!/usr/bin/python
from __future__ import absolute_import, division, print_function

import glob
import os
import subprocess
import sys


def list_tutorials():
    tutorial_glob = 'tutorial*.ipynb'
    tutorial_dir = os.path.dirname(os.path.abspath(__file__))
    tutorial_path = os.path.join(tutorial_dir, tutorial_glob)
    return sorted([os.path.basename(tutorial)
                   for tutorial in glob.glob(tutorial_path)])


def print_available_tutorials():
    """ Print available Databaker tutorials. Based on checking filenames. """
    print("Available tutorials:")
    tutorials = list_tutorials()

    if len(tutorials) == 0:
        print("(none found)")
    else:
        for tutorial in tutorials:
            print(tutorial)


def launch_tutorial(tutorial_name):
    """ Launch a Databaker tutorial specified at command line. """
    if tutorial_name in list_tutorials():
        tutorial_dir = os.path.dirname(os.path.abspath(__file__))
        tutorial_path = os.path.join(tutorial_dir, tutorial_name)

        # shell=True not required for Windows, I don't think, only POSIX.
        cmd = 'jupyter notebook {}'.format(tutorial_path)
        print("Running command:", cmd)
        subprocess.Popen(cmd, shell=True)
    else:
        print("Tutorial not found:", tutorial_name)


def main(argv=None):
    """ Launch a Databaker tutorial in Jupyter, or list those available.

    Usage: tutorial <tutorial_name.ipynb>

    Assumes that tutorials match the name tutorial*.ipynb. """
    if argv is None:
        argv = sys.argv[1:]
    if len(argv) > 0:
        launch_tutorial(argv[0])
    else:
        print_available_tutorials()


if __name__ == '__main__':
    main()
