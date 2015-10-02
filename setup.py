from setuptools import setup, find_packages

long_desc = """
Transform Excel spreadsheets
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

conf = dict(
    name='databaker',
    version='1.0.4',
    description="Excel Output Transformation",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    keywords='',
    author='ScraperWiki Ltd',
    author_email='feedback@scraperwiki.com',
    url='http://github.com/scraperwiki/databaker',
    license='AGPL',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=['docopt', 'xypath>=1.0.12', 'xlutils', 'pyhamcrest'],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'bake = databaker.bake:main',
            'sortcsv = databaker.sortcsv:main'
        ]
    })

if __name__ == '__main__':
    setup(**conf)
