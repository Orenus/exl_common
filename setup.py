#!/usr/bin/env python

from setuptools import setup

setup(
    name='exl_helpers',
    packages=['exl_helpers'],
    package_dir={'exl_helpers': '.'},
    description='Base package for helper functions and classes for exl_base_apps',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    install_requires=[
        'exl_base',
        'mock==2.0.0',
        'invoke',
        'bumpversion',
    ],
    version='0.0.13',
    url='http://github.com/prodops/package_example',
    author='Oren Sea',
    author_email='oren@prodops.io',
    keywords=['pip', 'prodops', 'example', 'packaging', 'package', 'base']
)
