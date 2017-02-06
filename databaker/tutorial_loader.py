# Based on altair tutorial loader:
# https://github.com/altair-viz/altair/blob/273a1fcf9cec1956474af755d5fe32f0e3f0aee8/altair/tutorial.py

# Copyright (c) 2015, Brian E. Granger and Jake Vanderplas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of altair nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
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

import os
import shutil

SRC_PATH = os.path.join(
    os.path.split(os.path.abspath(__file__)
)[0], 'tutorial')

DEST_PATH = os.path.relpath('DatabakerTutorial')

def copy_tutorial(overwrite=False):
    """Copy the Databaker tutorial notebooks into ./DatabakerTutorial."""
    if os.path.isdir(DEST_PATH) and overwrite:
        print('Removing old tutorial directory: {}'.format(DEST_PATH))
        shutil.rmtree(DEST_PATH, ignore_errors=True)
    if os.path.isdir(DEST_PATH):
        raise RuntimeError('{} already exists, run with overwrite=True to discard *all* existing files in tutorial directory'.format(DEST_PATH))
    print('Copying notebooks into fresh tutorial directory: {}'.format(DEST_PATH))
    shutil.copytree(SRC_PATH, DEST_PATH)


def tutorial(overwrite=False):
    """Copy the Databaker tutorial notebooks into ./DatabakerTutorial and show a link in the notebook."""
    copy_tutorial(overwrite=overwrite)
    print('Click on the following notebooks to explore the tutorial:')
    from IPython.display import FileLinks, display
    file_links = FileLinks(path=DEST_PATH,
                           included_suffixes=['.ipynb'],
                           recursive=False)
    display(file_links)
