#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesmini import *
from pyesmini.pyesminiRM import *

pyesmini = PyEsmini("resources/xosc/cut-in.xosc")
rm = PyEsminiRM(pyesmini.getODRManager(), fromFile= False)
print(rm.RM_GetNumberOfRoads())
print(rm.RM_GetRoadLength(0))
rm.RM_Close()
pyesmini.close()
