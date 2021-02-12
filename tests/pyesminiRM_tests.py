#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesminiRM import *
import unittest

XODRFILE = "resources/xodr/fabriksgatan.xodr"



class TestPyEsminiRMMethods(unittest.TestCase):

    def test_init_close(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertFalse(rm.close()) # TODO: Why this returns False?

    def test_createPosition(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.createPosition() == 0)
        self.assertTrue(rm.createPosition() == 1)
        self.assertTrue(rm.createPosition() == 2)

    def test_getNrOfPositions(self):
        rm = PyEsminiRM(XODRFILE)
        rm.createPosition()
        rm.createPosition()
        self.assertTrue(rm.getNrOfPositions() == 2)

    def deletePosition(self):
        rm = PyEsminiRM(XODRFILE)
        rm.createPosition()
        rm.createPosition()
        self.assertFalse(rm.deletePosition(10))  # invalid index
        self.assertTrue(rm.deletePosition(1))
        self.assertTrue(rm.getNrOfPositions() == 1)

    def test_getNumberOfRoads(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.getNumberOfRoads() == 16)

    def test_getIdOfRoadFromIndex(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.getIdOfRoadFromIndex(0) == 0 )
        self.assertTrue(rm.getIdOfRoadFromIndex(1) == 1 )
        self.assertTrue(rm.getIdOfRoadFromIndex(2) == 2 )
        self.assertTrue(rm.getIdOfRoadFromIndex(3) == 3 )


    def test_getRoadLength(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.getRoadLength(0) > 10)

    def test_getRoadNumberOfLanes(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.getRoadNumberOfLanes(0, 1) == 2)

    def test_getLaneIdByIndex(self):
        rm = PyEsminiRM(XODRFILE)
        self.assertTrue(rm.getLaneIdByIndex(1, 0, 1) == 1)

    def test_setLanePosition(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.setLanePosition(i, 0, 0, 10, 5, True))

    def test_setS(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.setS(i, 5))

    def test_setWorldPosition(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.setWorldPosition(i, 1, 2, 3, 4, 5, 6))

    def test_setWorldXYHPosition(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.setWorldXYHPosition(i, 1, 2, 3))

    def test_setWorldXYZHPosition(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.setWorldXYZHPosition(i, 1, 2, 3, 4))

    def test_positionMoveForward(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.positionMoveForward(i, 2.5, 1))

    def test_getPositionData(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        rm.setWorldXYZHPosition(i, 1, 2, 9, 4)
        data = rm.getPositionData(i)
        self.assertTrue(data.laneId == 1)
        #for field_name, field_type in data._fields_:
        #    print("   -", field_name, getattr(data, field_name))

    def test_getSpeedLimit(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        self.assertTrue(rm.getSpeedLimit(i))

    def test_getLaneInfo(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        info = rm.getLaneInfo(i, 1, 1)  # TODO: lookAheadMode as a meaningful constant
        #print("LANE_INFO", info.speed_limit, info.pos[0])
        self.assertTrue(info.speed_limit ==0 and info.pos[0]==0 )

    def test_getProbeInfo(self):
        rm = PyEsminiRM(XODRFILE)
        i = rm.createPosition()
        info = rm.getProbeInfo(i, 1, 1)  # TODO: lookAheadMode as a meaningful constant
        #print("PROBE_INFO", info.relative_h, info.relative_pos[1])
        self.assertTrue(info.relative_h ==0 and info.relative_pos[1]==0 )

    def test_subtractAFromB(self):
        rm = PyEsminiRM(XODRFILE)
        i1 = rm.createPosition()
        i2 = rm.createPosition()
        self.assertFalse(rm.subtractAFromB(i1, i2))  # TODO : Better testcase
if __name__ == '__main__':
    unittest.main()
