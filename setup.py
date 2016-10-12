from __future__ import absolute_import
from setuptools import setup, find_packages

long_desc = """
Transform Excel spreadsheets
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

conf = dict(
    name='databaker',
    version='1.2.0',
    description="DataBaker, part of QuickCode for ONS",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    keywords='',
    author='The Sensible Code Company Ltd',
    author_email='feedback@sensiblecode.io',
    url='https://github.com/sensiblecodeio/databaker',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=['docopt', 'xypath>=1.1.0', 'xlutils', 'pyhamcrest'],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'bake = databaker.bake:main',
            'sortcsv = databaker.sortcsv:main'
        ]
    })

if __name__ == '__main__':
    setup(**conf)
