#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import re
import os
import sys


def readme():
    with io.open("README.md", "r", encoding="utf-8") as my_file:
        return my_file.read()

setup(
    name='django-trapdoor',
    version='1.0.1',
    url='https://github.com/mikasoftware/django-trapdoor',
    license='BSD 2-Clause License',
    description="Automatically ban IP addresses requesting suspicious URL paths from your Django site",
    long_description=readme(),
    author='Bartlomiej Mika',
    author_email='bart@mikasoftware.com',
    packages=[
        'trapdoor'
    ],
    install_requires=[
        'django',
        'django-ipware'
    ],
    python_requires='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    keywords='ip blocker countermeasure defensive scanning',
)
