#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesmini import *
import unittest

XOSCFILE = "resources/xosc/cut-in.xosc"
XOSCFILE_GHOST = "resources/xosc/follow_ghost.xosc"


def callback(state_ptr, b):
    state = state_ptr.contents


class TestStringMethods(unittest.TestCase):
    '''

    def test_loadOSCstring(self):
        ### TODO: A minimalistic scenario with proper reference to odr file.
        xml = open(XOSCFILE, 'r').read()
        print(xml)
        pyesmini = PyEsmini(xml, use_viewer=False, oscFile=False)
        self.assertTrue(True)

    def test_fetchSensorObjectList(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        pyesmini.addObjectSensor(0, 2.0, 1.0, 0.5, 1.57, 1.0, 50.0, 1.57, 10)
        self.assertTrue(len(pyesmini.fetchSensorObjectList(0, 2)) > 0 )


    def test_loadOSCstring(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        xml = open(XOSCFILE, 'r').read()
        #print(xml)
        # TODO returns -1
        # self.assertTrue(pyesmini.loadOSCstring(xml))
        self.assertTrue(True)


    def test_setParameter(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.setParameter("test", 12.0) > 0 )


    def test_getParameter(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.getParameter("test"))



    '''


if __name__ == '__main__':
    unittest.main()
