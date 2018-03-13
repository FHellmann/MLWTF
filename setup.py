#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

with open('requirements.txt') as req:
    required = req.read().splitlines()

setup(
    name='My Smart Home',
    version='0.2.0',
    description='This project is for the use of machine learning with smart home',
    long_description=readme + '\n\n' + changelog,
    author='Fabio Hellmann',
    author_email='info@fabio-hellmann.de',
    url='https://github.com/FHellmann/My-Smart-Home',
    packages=find_packages(exclude=['tests*']),
    install_requires=required,
    test_suite='tests',
)
