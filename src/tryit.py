#!/usr/bin/env python
# encoding: utf-8

from airfoilprep import Polar, Airfoil
import numpy as np

airfoil1 = Airfoil.initFromGeometry('s828.txt', Res=[7e6, 9e6])
