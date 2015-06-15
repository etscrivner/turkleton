#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'boto',
    'six'
]

test_requirements = [
    'mock'
]

setup(
    name='turkleton',
    version='1.2.1',
    description="Simplified interfaces for assignments on Mechanical Turk.",
    long_description=readme + '\n\n' + history,
    author="Eric Scrivner",
    author_email='eric.t.scrivner@gmail.com',
    url='https://github.com/etscrivner/turkleton',
    packages=[
        'turkleton',
        'turkleton.assignment'
    ],
    package_dir={
        'turkleton': 'turkleton'
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='turkleton',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
