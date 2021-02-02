#!/usr/bin/env python3
import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from pyesmini.pyesmini import *

XOSCFILE = "resources/xosc/follow_ghost.xosc"
pyesmini = PyEsmini(XOSCFILE)

pyesmini.stepDT(0.001)
print(pyesmini.getODRManager())

pyesmini.addObjectSensor(0, 2.0, 1.0, 0.5, 1.57, 1.0, 50.0, 1.57, 10)
pyesmini.addObjectSensor(0, 3.0, 4.0, 1.5, 2.57, 2.0, 51.0, 2.57, 10)

print("getObjectGhostState::::", pyesmini.getObjectGhostState(0)._fields_)
print("getObjectState::::", pyesmini.getObjectState(0)._fields_)
print("getRoadInfoAlongGhostTrail::::", pyesmini.getRoadInfoAlongGhostTrail(0, 100)._fields_)
print("clearPaths::::", pyesmini.clearPaths())
xml = open(XOSCFILE, 'r').read()
# print(xml)
# print(pyesmini.loadOSCstring(xml))
pyesmini.stepDT(0.001)
pyesmini.updateOSIGroundTruth()
print("getOSIRoadLane::::::", pyesmini.getOSIRoadLane(0))
print("getOSILaneBoundary::::::", pyesmini.getOSILaneBoundary(0))
print("getOSIGroundTruthRaw::::", pyesmini.getOSIGroundTruthRaw())
print("getOSIGroundTruth::::", pyesmini.getOSIGroundTruth(1))
print("OSIFileOpen::::", pyesmini.OSIFileOpen("testX.txt"))
print("OSIFileWrite::::", pyesmini.OSIFileWrite())


# Define callback for scenario object enabling manipulating the state AFTER scenario step but BEFORE OSI output
# Use in combination with ExternalController in mode=additive in order for scenario actions to be applied first
def mycallback(state_ptr, b):
    state = state_ptr.contents
    print("CALLBAK for obj {}: x={} y={}".format(state.id, state.x, state.y))


pyesmini.registerObjectCallback(0, mycallback)
pyesmini.step()
print("fetchSensorObjectList:::::::", pyesmini.fetchSensorObjectList(0, 10))
print("LEN-fetchSensorObjectList:::::::", len(pyesmini.fetchSensorObjectList(0, 10)))

x = pyesmini.fetchSensorObjectList(0, 10)
for i in x:
    print(i)

### TODO: BUG The result is all -1 !!!!
# print("getOSILaneBoundaryIds::::", pyesmini.getOSILaneBoundaryIds(1))   ### TODO : SEGFAULT


for i in range(10000):
    pyesmini.step()
    triggered = False

    if pyesmini.getSimulationTime() > 2.5 and triggered == False:
        triggered = True;
    # val = pyesmini.getParameter("DummyParameter")
    # if val != None:
    #    print("Found")
    #    print(val)

    print("Simulation time: ", pyesmini.getSimulationTime())
pyesmini.close()
