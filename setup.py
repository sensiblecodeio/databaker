from setuptools import setup, find_packages

long_desc = """
Transform Excel spreadsheets
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

conf = dict(
    name='databaker',
    version='0.0.0',
    description="Excel Output Transformation",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ScraperWiki Ltd',
    author_email='feedback@scraperwiki.com',
    url='http://github.com/scraperwiki/databaker',
    #license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': [
            'bake = databaker.bake:main',
        ]
    })

if __name__ == '__main__':
    setup(**conf)
