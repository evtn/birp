#!/usr/bin/env python3

import os
from setuptools import setup


# get key package details from birp/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'birp', '__version__.py')) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open('README.md', 'r') as f:
    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=['birp', 'birp.reverse', 'birp.translate'],
    install_requires=["lark"],
    package_data={"": ["*.lark", "*.birp"]},
    include_package_data=True,
    python_requires=">=3.6.*",
    license=about['__license__'],
    download_url=f"https://github.com/evtn/birp/archive/v{about['__version__']}.tar.gz",
    zip_safe=False,
    # https://pypi.org/classifiers/
    classifiers=[ 
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'   
    ],
    keywords='python russian translation'
)
