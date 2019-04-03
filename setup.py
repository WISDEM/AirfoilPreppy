#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup  # , find_packages


setup(
    name='AirfoilPrep',
    version='0.1.0',
    description='Airfoil preprocessing for wind turbine applications',
    author='NREL WISDEM Team',
    author_email='systems.engineering@nrel.gov',
    package_dir={'': 'src'},
    packages=['airfoilprep'],
    license='Apache License, Version 2.0',
    zip_safe=False
)
