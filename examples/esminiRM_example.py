#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesminiRM import *

rm = PyEsminiRM("resources/xodr/fabriksgatan.xodr")
print(rm)
print(rm.RM_GetNumberOfRoads())
print(rm.RM_GetRoadLength(0))