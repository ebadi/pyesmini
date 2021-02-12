#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from pyesmini.pyesminiRM import *
from pyesmini.pyesmini import *
import unittest

XOSCFILE = "resources/xosc/cut-in.xosc"


class TestStringMethods(unittest.TestCase):
    def test_initWithPointer(self):
        pyesmini = PyEsmini("resources/xosc/cut-in.xosc", use_viewer=False)
        rm = PyEsminiRM(pyesmini.getODRManager(), fromFile=False)
        self.assertTrue(rm.getNumberOfRoads() == 1)
        self.assertTrue(rm.getRoadLength(0) == 1464.434326171875)


if __name__ == '__main__':
    unittest.main()
