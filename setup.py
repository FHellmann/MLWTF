#!/usr/bin/python
"""
    Author: Fabio Hellmann <info@fabio-hellmann.de>
"""

from setuptools import setup

with open('requirements.txt') as req:
    required = req.read().splitlines()

setup(
    name='My Smart Home',
    version='0.1.0',
    description='This project is for the use of machine learning with smart home',
    author='Fabio Hellmann',
    author_email='info@fabio-hellmann.de',
    url='http://fabio-hellmann.de/',
    install_requires=required,
)