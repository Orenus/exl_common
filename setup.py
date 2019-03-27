#!/usr/bin/env python

from setuptools import setup

setup(
    name='exl_common',
    packages=['exl_common'],
    package_dir={'exl_common': '.'},
    description='Base package for helper functions and classes for exl_base_apps',
    classifiers=[
        'Private :: Do Not Upload to pypi server',
    ],
    install_requires=[
        'exl_base',
        'invoke',
        'bumpversion',
        'paramiko',
    ],
    version='0.0.1',
    url='http://github.com/prodops/package_example',
    author='Oren Sea',
    author_email='oren@prodops.io',
    keywords=['pip', 'prodops', 'example', 'packaging', 'package', 'base']
)

