#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesmini import *

pyesmini = PyEsmini("resources/xosc/cut-in.xosc", h = 400)

print("Number of objects:", pyesmini.getNumberOfObjects())
print("Open Drive file: ", pyesmini.getODRFilename())
print("Open Scene Graph file: ", pyesmini.getSceneGraphFilename())
print("Pointer to ODR MANAGER", pyesmini.getODRManager())

for i in range(10000):
    pyesmini.step()
    pyesmini.reportObjectPos(0, 0, 8, i, 0, 1.57, 0.0, 0.0, 15.0);
    print("simpleVehicleCreate", pyesmini.simpleVehicleCreate(1, 2, 3, 4))
    state = pyesmini.getRoadInfoAtDistance(0, 10, 0)
    for field_name, field_type in state._fields_:
        print("   -", field_name, getattr(state, field_name))

    statev = pyesmini.simpleVehicleGetState
    for j in range(pyesmini.getNumberOfObjects()):
        print("set speed of object ", j, " = ", pyesmini.reportObjectSpeed(j, i))
        print("set lateral position ", j, " = ", pyesmini.reportObjectLateralPosition(j, i))
        print("set lateral position ", 0, " = ", pyesmini.reportObjectLateralLanePosition(j, 0, j))
        print("State for object: ", j)
        print("Object name: ", pyesmini.getObjectName(j))
        print("Has shadow object: ", pyesmini.objectHasGhost(j))

        state = pyesmini.getObjectState(j)
        for field_name, field_type in state._fields_:
            print("   ", field_name, getattr(state, field_name))
        if i == 100:
            pyesmini.stepDT(1)
        print("Simulation time: ", pyesmini.getSimulationTime())
    if pyesmini.getQuitFlag():
        print("Exit by getting quit flag")
        break

pyesmini.close()
