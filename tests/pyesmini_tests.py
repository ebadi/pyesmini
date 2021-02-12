#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesmini import *
import unittest

XOSCFILE = "resources/xosc/cut-in.xosc"
XOSCFILE_GHOST = "resources/xosc/follow_ghost.xosc"

x = False


# Define callback for scenario object enabling manipulating the state AFTER scenario step but BEFORE OSI output
# Use in combination with ExternalController in mode=additive in order for scenario actions to be applied first
def mycallback(state_ptr, b):
    global x
    x = True
    state = state_ptr.contents
    print("Callback for obj {}: x={} y={}".format(state.id, state.x, state.y))


class TestPyEsminiMethods(unittest.TestCase):

    def test_registerObjectCallback(self):
        global x
        x = False
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        pyesmini.registerObjectCallback(0, mycallback)
        pyesmini.step()
        self.assertTrue(x)

    def test_getOSILaneBoundary(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        pyesmini.stepDT(0.001)
        pyesmini.updateOSIGroundTruth()
        self.assertTrue(len(pyesmini.getOSILaneBoundary(10)) > 0)

    def test_getOSILaneBoundaryIds(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        pyesmini.stepDT(0.001)
        pyesmini.updateOSIGroundTruth()
        self.assertTrue(len(pyesmini.getOSILaneBoundaryIds(10)) > 0)

    def test_getOSIRoadLane(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getOSIRoadLane(0)) > 0)

    def test_clearPaths(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.clearPaths())

    def test_addPath(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.addPath("."))

    def test_step(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.step())

    def test_close(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.close())

    def test_simulationTime(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        pyesmini.step()
        self.assertTrue(pyesmini.getSimulationTime() > 0)

    def test_simulationTime(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertFalse(pyesmini.getQuitFlag())

    def test_getODRFilename(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue("xodr" in pyesmini.getODRFilename())

    def test_getSceneGraphFilename(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue("osg" in pyesmini.getSceneGraphFilename())

    def test_getODRManager(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        print(pyesmini.getODRManager() != None)

    def test_reportObjectPos(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.reportObjectPos(0, 0.2, 1, 2, 3, 0.5, 0.6, 0.4, 1))

    def test_reportObjectRoadPos(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.reportObjectRoadPos(0, 0.2, 1, 1, 1, 1, 1))

    def test_reportObjectSpeed(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.reportObjectSpeed(0, 1))

    def test_reportObjectLateralLanePosition(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.reportObjectLateralLanePosition(0, 1, 2))

    def test_getNumberOfObjects(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.getNumberOfObjects() > 0)

    def test_getObjectState(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getObjectState(0)._fields_) > 0)

    def test_getObjectName(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getObjectName(0)) > 0)

    def test_getRoadInfoAtDistance(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getRoadInfoAtDistance(0, 100, 1)._fields_) > 0)

    def test_getObjectGhostState(self):
        pyesmini = PyEsmini(XOSCFILE_GHOST, use_viewer=False)
        pyesmini.step()
        self.assertTrue(len(pyesmini.getObjectGhostState(0)._fields_) > 0)

    def test_addObjectSensor(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.addObjectSensor(1, 1.1, 2.2, 3.3, 4.4, 0.1, 10.9, 2, 10))

    def test_openOSISocket(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.openOSISocket("127.0.0.1"))

    def test_enableOSIFile(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.enableOSIFile("test"))

    def test_enableOSIFile(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.updateOSIGroundTruth())

    def test_getOSIGroundTruth(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getOSIGroundTruth([1, 2, 3])) > 0)

    def test_getOSIGroundTruthRaw(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getOSIGroundTruthRaw()) > 0)

    def test_getOSISensorDataRaw(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.getOSISensorDataRaw()) > 0)

    def test_OSIFileOpen(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.OSIFileOpen("test.txt"))
        self.assertTrue(pyesmini.OSIFileWrite())

    def test_viewerShowFeature(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.viewerShowFeature(1, True))

    def test_simpleVehicleCreate(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.simpleVehicleCreate(1, 2, 3, 4) != 0)

    def test_simpleVehicleDelete(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.simpleVehicleDelete(pyesmini.simpleVehicleCreate(1, 2, 3, 4)))

    def test_simpleVehicleControlBinary(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.simpleVehicleControlBinary(pyesmini.simpleVehicleCreate(1, 2, 3, 4), 2.5, 1, 1))

    def test_simpleVehicleControlAnalog(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.simpleVehicleControlAnalog(pyesmini.simpleVehicleCreate(1, 2, 3, 4), 2, 1, 1))

    def test_simpleVehicleSetMaxSpeed(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(pyesmini.simpleVehicleSetMaxSpeed(pyesmini.simpleVehicleCreate(1, 2, 3, 4), 2))

    def test_simpleVehicleGetState(self):
        pyesmini = PyEsmini(XOSCFILE, use_viewer=False)
        self.assertTrue(len(pyesmini.simpleVehicleGetState(pyesmini.simpleVehicleCreate(1, 2, 3, 4))._fields_) > 0)


if __name__ == '__main__':
    unittest.main()
