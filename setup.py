#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="David Steinberger",
    author_email='david.steinberger@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Scrap Imdb website to retrieve infdetail informmations from movies or tvshow",
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='scrapimdb',
    name='scrap-imdb',
    packages=find_packages(include=['scrapimdb']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/dsteinberger/scrapimdb',
    version='0.1.6',
    zip_safe=False,
)
