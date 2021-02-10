from ctypes import *
import ctypes
from .shared import *


class ScenarioObjectState(Structure):
    _fields_ = [
        ("id", c_int),  # Automatically generated unique object id
        ("model_id", c_int),
        # Id to control what 3D model to represent the vehicle - see carModelsFiles_[] in scenarioenginedll.cpp
        ("ctrl_type", c_int),  # 0: DefaultController 1: External. Further values see Controller::Type enum
        ("timestamp", c_float),
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("h", c_float),
        ("p", c_float),
        ("r", c_float),
        ("roadId", c_int),
        ("t", c_float),
        ("laneId", c_int),
        ("laneOffset", c_float),
        ("s", c_float),
        ("speed", c_float),
        ("centerOffsetX", c_float),
        ("centerOffsetY", c_float),
        ("centerOffsetZ", c_float),
        ("width", c_float),
        ("length", c_float),
        ("height", c_float)
    ]


class RoadInfo(Structure):
    _fields_ = [
        ("global_pos_x", c_float),  # target position, in global coordinate system
        ("global_pos_y", c_float),  # target position, in global coordinate system
        ("global_pos_z", c_float),  # target position, in global coordinate system
        ("local_pos_x", c_float),  # target position, relative vehicle (pivot position object) coordinate system
        ("local_pos_y", c_float),  # target position, relative vehicle (pivot position object) coordinate system
        ("local_pos_z", c_float),  # target position, relative vehicle (pivot position object) coordinate system
        ("angle", c_float),  # heading angle to target from and relatove to vehicle (pivot position)
        ("road_heading", c_float),  # road heading at steering target point
        ("road_pitch", c_float),  # road pitch (inclination) at steering target point
        ("road_roll", c_float),  # road roll (camber) at target point
        ("trail_heading", c_float),  # trail heading (only when used for trail lookups, else equals road_heading)
        ("curvature", c_float),  # road curvature at steering target point
        ("speed_limit", c_float)  # speed limit given by OpenDRIVE type entry
    ]


class LaneBoundaryId(Structure):
    _fields_ = [
        ("far_left_lb_id", c_int),
        ("left_lb_id", c_int),
        ("right_lb_id", c_int),
        ("far_right_lb_id", c_int)
    ]


class SimpleVehicleState(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("h", c_float),
        ("p", c_float),
        ("speed", c_float),
    ]


class Parameter(Structure):
    _fields_ = [
        ("name", String),  # Name of the parameter as defined in the OpenSCENARIO file
        ("value", POINTER(None))
        # Pointer to value which can be an integer, double or string (const char*) as defined in the OpenSCENARIO file
    ]


class PyEsmini:
    '''
    Initialize the scenario engine
    @param disable_ctrls 1=Any controller will be disabled 0=Controllers applied according to OSC file
    @param use_viewer 0=no viewer, 1=use viewer
    @param threads 0=single thread, 1=viewer in a separate thread, parallel to scenario engine
    @param record Create recording for later playback 0=no recording 1=recording
    @return 0 if successful, -1 if not


    Initialize the scenario engine
    @param oscFilename Path to the OpenSCEANRIO file

    Initialize the scenario engine
    @param oscAsXMLString OpenSCENARIO XML as string
    '''

    def __init__(self, osc, disable_ctrls=False, use_viewer=True, threads=False, recordFile="", oscFile=True, x=60,
                 y=60, w=800, h=400):

        dir_path = os.path.dirname(os.path.realpath(__file__))

        if platform == "linux" or platform == "linux2":
            self.se = CDLL(dir_path + "/libesminiLib.so")
        elif platform == "darwin":
            self.se = CDLL(dir_path + "/libesminiLib.dylib")
        elif platform == "win32":
            self.se = CDLL(dir_path + "\esminiLib.dll")
        else:
            print("Unsupported platform: {}".format(platform))
            raise Exception("Loading shared library: shared library not found")

        self.se.SE_InitWithArgs.argtypes = c_int, POINTER(c_char_p)
        self.se.SE_InitWithArgs.restype = c_int

        self.disable_ctrls = disable_ctrls
        self.use_viewer = use_viewer

        ArgumentList = ["OpenScenarioEditor"]
        if threads:
            ArgumentList.append("--threads")

        if len(recordFile) > 0:
            ArgumentList.append("--record")
            ArgumentList.append(recordFile)

        if oscFile:
            ArgumentList.append("--osc")
            ArgumentList.append(osc)
        else:
            ArgumentList.append("--osc_str")
            ArgumentList.append(osc)
        if disable_ctrls:
            ArgumentList.append("--disable_controllers")

        if use_viewer:
            ArgumentList.append("--window")
            ArgumentList.append(str(x) + " " + str(y) + " " + str(w) + " " + str(h))
        else:
            ArgumentList.append("--headless")
        arr = (ctypes.c_char_p * len(ArgumentList))()
        arr[:] = [s.encode('utf-8') for s in ArgumentList]

        if self.se.SE_InitWithArgs(len(ArgumentList), arr) < 0:
            raise Exception("Init failed")

        '''
        if oscFile:
            if self.se.SE_Init(osc, self.disable_ctrls, self.use_viewer, self.threads, self.record) < 0:
                raise Exception("loadOSCfile Error: Make sure that the OSC file is not corrupted.")
        else:
            if self.se.SE_InitWithString(osc, self.disable_ctrls, self.use_viewer, self.threads, self.record) < 0:
                raise Exception("loadOSC Error: Make sure that the OSC XML string is not corrupted.")
        '''
        self.se.SE_Init.argtypes = [String, c_int, c_int, c_int, c_int]
        self.se.SE_Init.restype = c_int

        self.se.SE_InitWithString.argtypes = [String, c_int, c_int, c_int, c_int]
        self.se.SE_InitWithString.restype = c_int

        self.se.SE_AddPath.argtypes = [String]
        self.se.SE_AddPath.restype = c_int

        self.se.SE_ClearPaths.argtypes = []
        self.se.SE_ClearPaths.restype = None

        self.se.SE_StepDT.argtypes = [c_float]
        self.se.SE_StepDT.restype = c_int

        self.se.SE_Step.argtypes = []
        self.se.SE_Step.restype = c_int

        self.se.SE_Close.argtypes = []

        self.se.SE_GetSimulationTime.argtypes = []
        self.se.SE_GetSimulationTime.restype = c_float

        self.se.SE_GetQuitFlag.argtypes = []
        self.se.SE_GetQuitFlag.restype = c_int

        self.se.SE_GetODRFilename.argtypes = []
        self.se.SE_GetODRFilename.restype = c_char_p

        self.se.SE_SetParameter.argtypes = [Parameter]
        self.se.SE_SetParameter.restype = c_int

        self.se.SE_GetSceneGraphFilename.argtypes = []
        self.se.SE_GetSceneGraphFilename.restype = c_char_p

        self.se.SE_GetParameter.argtypes = [POINTER(Parameter)]
        self.se.SE_GetParameter.restype = c_int

        self.se.SE_GetODRManager.argtypes = []
        self.se.SE_GetODRManager.restype = POINTER(c_ubyte)
        self.se.SE_GetODRManager.errcheck = lambda v, *a: cast(v, c_void_p)

        self.se.SE_ReportObjectPos.argtypes = [c_int, c_float, c_float, c_float, c_float, c_float, c_float, c_float,
                                               c_float]
        self.se.SE_ReportObjectPos.restype = c_int

        self.se.SE_ReportObjectRoadPos.argtypes = [c_int, c_float, c_int, c_int, c_float, c_float, c_float]
        self.se.SE_ReportObjectRoadPos.restype = c_int

        self.se.SE_ReportObjectSpeed.argtypes = [c_int, c_float]
        self.se.SE_ReportObjectSpeed.restype = c_int

        self.se.SE_ReportObjectLateralPosition.argtypes = [c_int, c_float]
        self.se.SE_ReportObjectLateralPosition.restype = c_int

        self.se.SE_ReportObjectLateralLanePosition.argtypes = [c_int, c_int, c_float]
        self.se.SE_ReportObjectLateralLanePosition.restype = c_int

        self.se.SE_GetNumberOfObjects.argtypes = []
        self.se.SE_GetNumberOfObjects.restype = c_int

        self.se.SE_GetObjectState.argtypes = [c_int, POINTER(ScenarioObjectState)]
        self.se.SE_GetObjectState.restype = c_int

        self.se.SE_GetObjectName.argtypes = [c_int]
        self.se.SE_GetObjectName.restype = c_char_p

        self.se.SE_ObjectHasGhost.argtypes = [c_int]
        self.se.SE_ObjectHasGhost.restype = c_int

        self.se.SE_GetObjectGhostState.argtypes = [c_int, POINTER(ScenarioObjectState)]
        self.se.SE_GetObjectGhostState.restype = c_int

        self.se.SE_GetRoadInfoAtDistance.argtypes = [c_int, c_float, POINTER(RoadInfo), c_int]
        self.se.SE_GetRoadInfoAtDistance.restype = c_int

        self.se.SE_GetRoadInfoAlongGhostTrail.argtypes = [c_int, c_float, POINTER(RoadInfo), POINTER(c_float)]
        self.se.SE_GetRoadInfoAlongGhostTrail.restype = c_int

        self.se.SE_AddObjectSensor.argtypes = [c_int, c_float, c_float, c_float, c_float, c_float, c_float, c_float,
                                               c_int]
        self.se.SE_AddObjectSensor.restype = c_int

        self.se.SE_FetchSensorObjectList.argtypes = [c_int, POINTER(c_int)]
        self.se.SE_FetchSensorObjectList.restype = c_int

        # self.se.SE_RegisterObjectCallback.argtypes = [c_int, CFUNCTYPE(UNCHECKED(None), POINTER(ScenarioObjectState), POINTER(None)), POINTER(None)]
        self.se.SE_RegisterObjectCallback.restype = None

        self.se.SE_OpenOSISocket.argtypes = [String]
        self.se.SE_OpenOSISocket.restype = c_int

        self.se.SE_DisableOSIFile.argtypes = []
        self.se.SE_DisableOSIFile.restype = None

        self.se.SE_EnableOSIFile.argtypes = [String]
        self.se.SE_EnableOSIFile.restype = None

        self.se.SE_UpdateOSIGroundTruth.argtypes = []
        self.se.SE_UpdateOSIGroundTruth.restype = c_int

        self.se.SE_GetOSIGroundTruth.argtypes = [POINTER(c_int)]
        self.se.SE_GetOSIGroundTruth.restype = c_char_p

        self.se.SE_GetOSIGroundTruthRaw.argtypes = []
        self.se.SE_GetOSIGroundTruthRaw.restype = c_char_p

        self.se.SE_GetOSIRoadLane.argtypes = [POINTER(c_int), c_int]
        self.se.SE_GetOSIRoadLane.restype = c_char_p

        self.se.SE_GetOSILaneBoundary.argtypes = [POINTER(c_int), c_int]
        self.se.SE_GetOSILaneBoundary.restype = c_char_p

        self.se.SE_GetOSILaneBoundaryIds.argtypes = [c_int, POINTER(LaneBoundaryId)]
        self.se.SE_GetOSILaneBoundaryIds.restype = None

        self.se.SE_GetOSISensorDataRaw.argtypes = []
        self.se.SE_GetOSISensorDataRaw.restype = c_char_p

        self.se.SE_OSIFileOpen.argtypes = [c_char_p]
        self.se.SE_OSIFileOpen.restype = c_bool

        self.se.SE_OSIFileWrite.argtypes = [c_bool]
        self.se.SE_OSIFileWrite.restype = c_bool

        self.se.SE_ViewerShowFeature.argtypes = [c_int, c_bool]
        self.se.SE_ViewerShowFeature.restype = None

        self.se.SE_SimpleVehicleCreate.argtypes = [c_float, c_float, c_float, c_float]
        self.se.SE_SimpleVehicleCreate.restype = POINTER(c_ubyte)

        self.se.SE_SimpleVehicleDelete.argtypes = [POINTER(None)]
        self.se.SE_SimpleVehicleDelete.restype = None

        self.se.SE_SimpleVehicleControlBinary.argtypes = [POINTER(None), c_double, c_int, c_int]
        self.se.SE_SimpleVehicleControlBinary.restype = None

        self.se.SE_SimpleVehicleControlAnalog.argtypes = [POINTER(None), c_double, c_double, c_double]
        self.se.SE_SimpleVehicleControlAnalog.restype = None

        self.se.SE_SimpleVehicleSetMaxSpeed.argtypes = [POINTER(None), c_float]
        self.se.SE_SimpleVehicleSetMaxSpeed.restype = None

        self.se.SE_SimpleVehicleGetState.argtypes = [POINTER(None), POINTER(SimpleVehicleState)]
        self.se.SE_SimpleVehicleGetState.restype = None

    '''
    Add a search path for OpenDRIVE and 3D model files
    @param path Path to a directory
    @return 0 if successful, -1 if not
    '''

    def addPath(self, path):
        if self.se.SE_AddPath(path) < 0:
            raise Exception("SE_AddPath Error: path is incorrect")
        return True

    '''
    Clear all search paths for OpenDRIVE and 3D model files
    '''

    def clearPaths(self):
        self.se.SE_ClearPaths()
        return True

    '''
    Step the simulation forward with specified timestep
    @param dt time step in seconds
    @return 0 if successful, -1 if not
    '''

    def stepDT(self, timestamp):
        return self.se.SE_StepDT(timestamp)

    '''
    Step the simulation forward. Time step will be elapsed system (world) time since last step. Useful for interactive/realtime use cases.
    @return 0 if successful, -1 if not
    '''

    def step(self):
        if self.se.SE_Step() < 0:
            return False
        else:
            return True

    '''
    Stop simulation gracefully. Two purposes: 1. Release memory and 2. Prepare for next simulation, e.g. reset object lists.
    '''

    def close(self):
        self.se.SE_Close()
        return True

    '''
    Get simulation time in seconds
    '''

    def getSimulationTime(self):
        return self.se.SE_GetSimulationTime()

    '''
    Get the bool value of the end of the scenario 
    '''

    def getQuitFlag(self):
        return bool(self.se.SE_GetQuitFlag())

    '''
    Get name of currently referred and loaded OpenDRIVE file 
    @return filename as string (const, since it's allocated and handled by esmini)
    '''

    def getODRFilename(self):
        return self.se.SE_GetODRFilename().decode()

    '''
    Get name of currently referred and loaded SceneGraph file 
    @return filename as string (const, since it's allocated and handled by esmini)
    '''

    def getSceneGraphFilename(self):
        return self.se.SE_GetSceneGraphFilename().decode()

    '''
    Set value of named parameter
    @param parameter Struct object including name of parameter and pointer to value, see SE_Parameter declaration
    @return 0 if successful, -1 if not
    '''

    def setParameter(self, pname, pvalue):
        param = Parameter()
        param.name = String(pname.encode())
        obj = c_double(pvalue)
        param.value = cast(byref(obj), c_void_p)
        if self.se.SE_SetParameter(param) < 0:
            return False
        else:
            return True

    '''
    Get value of named parameter. The value within the parameter struct will be filled in.
    @param parameter Pointer to parameter struct object, see SE_Parameter declaration.
    @return 0 if successful, -1 if not
    SE_DLL_API int SE_GetParameter(SE_Parameter* parameter);
    '''

    def getParameter(self, pname):
        param = Parameter()
        param.name = String(pname.encode())
        obj = c_double(0)
        param.value = cast(byref(obj), c_void_p)
        if self.se.SE_GetParameter(byref(param)) < 0:
            raise Exception("SE_GetParameter Error: Unknown error")
        else:
            return True
            data = cast(param.value, POINTER(c_double)).contents
            return data.value

    def getODRManager(
            self):
        ### TODO : c_ubyte
        try:
            return self.se.SE_GetODRManager()
        except:
            return None

    '''
    Report object position in cartesian coordinates
    @param id Id of the object
    @param timestamp Timestamp (not really used yet, OK to set 0)
    @param x X coordinate
    @param y Y coordinate
    @param z Z coordinate
    @param h Heading / yaw
    @param p Pitch
    @param r Roll
    @param speed Speed in forward direction of the enitity
    @return 0 if successful, -1 if not
    '''

    def reportObjectPos(self, id, timestamp, x, y, z, h, p, r, speed):
        if self.se.SE_ReportObjectPos(id, timestamp, x, y, z, h, p, r, speed) < 0:
            return False
        else:
            return True

    '''
    Report object position in road coordinates
    @param id Id of the object
    @param timestamp Timestamp (not really used yet, OK to set 0)
    @param roadId Id of the road 
    @param laneId Id of the lane 
    @param laneOffset Lateral offset from center of specified lane
    @param s Longitudinal distance of the position along the specified road
    @param speed Speed in forward direction (s axis) of the enitity
    @return 0 if successful, -1 if not
    '''

    def reportObjectRoadPos(self, id, timestamp, roadId, laneId, laneOffset, s, speed):
        if self.se.SE_ReportObjectRoadPos(id, timestamp, roadId, laneId, laneOffset, s, speed) < 0:
            return False
        else:
            return True

    '''
    Report object longitudinal speed. Useful for an external longitudinal controller.
    @param id Id of the object
    @param speed Speed in forward direction of the enitity
    @return 0 if successful, -1 if not
    '''

    def reportObjectSpeed(self, id,
                          speed):  # Question: How is it reporting the speed? I think this has to be renamed to setObjectSpeed
        if self.se.SE_ReportObjectSpeed(id, speed) < 0:
            return False
        else:
            return True

    '''
    Report object lateral position relative road centerline. Useful for an external lateral controller.
    @param id Id of the object
    @param t Lateral position
    @return 0 if successful, -1 if not
    '''

    def reportObjectLateralPosition(self, id, t):
        if self.se.SE_ReportObjectLateralPosition(id, t) < 0:
            return False
        else:
            return True

    '''
    Report object lateral position by lane id and lane offset. Useful for an external lateral controller.
    @param id Id of the object
    @param laneId Id of the lane
    @param laneOffset Lateral offset from center of specified lane
    @return 0 if successful, -1 if not
    '''

    def reportObjectLateralLanePosition(self, id, laneId, laneOffset):
        if self.se.SE_ReportObjectLateralLanePosition(id, laneId, laneOffset) < 0:
            return False
        else:
            return True

    '''
    Get the number of entities in the current scenario
    @return Number of entities
    '''

    def getNumberOfObjects(self):
        return self.se.SE_GetNumberOfObjects()

    '''
    Get the state of specified object
    @param index Index of the object. Note: not ID
    @param state Pointer/reference to a SE_ScenarioObjectState struct to be filled in
    @return 0 if successful, -1 if not
    '''

    def getObjectState(self, objectId):
        state = ScenarioObjectState()
        if self.se.SE_GetObjectState(objectId, byref(state)) < 0:
            raise Exception("SE_GetObjectState Error: Unknow error")
        else:
            return state

    '''
    Get the name of specified object
    @param index Index of the object. Note: not ID
    @return Name
    '''

    def getObjectName(self, index):
        return self.se.SE_GetObjectName(c_int(index)).decode()

    '''
    Check whether an object has a ghost (special purpose lead vehicle) 
    @param index Index of the object. Note: not ID
    @return 1 if ghost, 0 if not
    '''

    def objectHasGhost(self, index):
        return self.se.SE_ObjectHasGhost(index)

    '''
    Get the state of specified object's ghost (special purpose lead vehicle)
    @param index Index of the object. Note: not ID
    @param state Pointer/reference to a SE_ScenarioObjectState struct to be filled in
    @return 0 if successful, -1 if not
    '''

    def getObjectGhostState(self, index):
        state = ScenarioObjectState()
        if self.se.SE_GetObjectGhostState(index, byref(state)) < 0:
            raise Exception("SE_GetObjectGhostState Error: Unknow error")
        else:
            return state

    '''
    Get information suitable for driver modeling of a point at a specified distance from object along the road ahead
    @param object_id Handle to the position object from which to measure
    @param lookahead_distance The distance, along the road, to the point
    @param data Struct including all result values, see typedef for details
    @param lookAheadMode Measurement strategy: Along 0=lane center, 1=road center (ref line) or 2=current lane offset. See roadmanager::Position::LookAheadMode enum
    @return 0 if successful, -1 if not
    '''

    # Question: Is there a method like getNumberOfRoads and getRoadState to extract road information?
    def getRoadInfoAtDistance(self, object_id, lookahead_distance, lookAheadMode):
        roadinfo = RoadInfo()
        if self.se.SE_GetRoadInfoAtDistance(object_id, lookahead_distance, byref(roadinfo), lookAheadMode) < 0:
            raise Exception("SE_GetRoadInfoAtDistance Error: Unknow error")
        else:
            return roadinfo

    '''
    Get information suitable for driver modeling of a ghost vehicle driving ahead of the ego vehicle
    @param object_id Handle to the position object from which to measure (the actual externally controlled Ego vehicle, not ghost)
    @param lookahead_distance The distance, along the ghost trail, to the point from the current Ego vehicle location
    @param data Struct including all result values, see typedef for details
    @param speed_ghost reference to a variable returning the speed that the ghost had at this point along trail
    @return 0 if successful, -1 if not
    '''

    def getRoadInfoAlongGhostTrail(self, object_id, lookahead_distance):
        speed_ghost = c_float(1)
        roadinfo = RoadInfo()
        if self.se.SE_GetRoadInfoAlongGhostTrail(object_id, lookahead_distance, byref(roadinfo),
                                                 byref(speed_ghost)) < 0:
            raise Exception("SE_GetRoadInfoAtDistance Error: Unknow error")
        else:
            return roadinfo

    '''
    Create an ideal object sensor and attach to specified vehicle
    @param object_id Handle to the object to which the sensor should be attached
    @param x Position x coordinate of the sensor in vehicle local coordinates
    @param y Position y coordinate of the sensor in vehicle local coordinates
    @param z Position z coordinate of the sensor in vehicle local coordinates
    @param h heading of the sensor in vehicle local coordinates
    @param fovH Horizontal field of view, in degrees
    @param rangeNear Near value of the sensor depth range
    @param rangeFar Far value of the sensor depth range
    @param maxObj Maximum number of objects theat the sensor can track
    @return Sensor ID (Global index of sensor), -1 if unsucessful
    '''

    def addObjectSensor(self, object_id, x, y, z, h, rangeNear, rangeFar, fovH, maxObj):
        if self.se.SE_AddObjectSensor(object_id, x, y, z, h, rangeNear, rangeFar, fovH, maxObj) < 0:
            raise Exception("SE_AddObjectSensor Error: Are you sure the sensor you are referring exists?")
        else:
            return True

    '''
    Fetch list of identified objects from a sensor
    @param sensor_id Handle (index) to the sensor
    @param list Array of object indices
    @return Number of identified objects, i.e. length of list. -1 if unsuccesful.
    '''

    def fetchSensorObjectList(self, sensor_id, max_num_obj):
        pyarr = [-1] * max_num_obj
        carr = (ctypes.c_int * max_num_obj)(*pyarr)
        slen = self.se.SE_FetchSensorObjectList(sensor_id, carr) < 0
        if slen < 0:
            raise Exception("SE_AddObjectSensor Error: Unknow error")
        else:
            return carr  ### TODO convert to python list

    '''
    Register a function and optional parameter (ref) to be called back from esmini after each frame (update of scenario)
    The current state of specified entity will be returned.
    Complete or part of the state can then be overridden by calling the SE_ReportObjectPos/SE_ReportObjectRoadPos functions.
    @param object_id Handle to the position object (entity)
    @param SE_ScenarioObjectState A pointer to the function to be invoked
    @param user_data Optional pointer to a local data object that will be passed as argument in the callback. Set 0/NULL if not needed.
    '''

    def registerObjectCallback(self, object_id, f):
        user_data = ScenarioObjectState()
        callback_type = CFUNCTYPE(None, POINTER(ScenarioObjectState), c_void_p)
        callback_func = callback_type(f)
        print("callback_func:::::", callback_func)
        print("callback_type:::::", callback_type)

        self.se.SE_RegisterObjectCallback(object_id, callback_func, 0)

    ################# OSI interface #################

    '''
    Send OSI packages over UDP to specified IP address
    '''

    def openOSISocket(self, ipaddr):
        if self.se.SE_OpenOSISocket(ipaddr) < 0:
            raise Exception("SE_OpenOSISocket Error: path is incorrect")
        else:
            return True

    '''
    Switch off logging to OSI file(s)
    '''

    def disableOSIFile(self):
        self.se.SE_DisableOSIFile()
        return True

    '''
    Switch on logging to OSI file(s)
    @param filename Optional filename, including path. Set to 0 or "" to use default.
    '''

    def enableOSIFile(self, filename):
        self.se.SE_EnableOSIFile(filename)
        return True

    # Question: The description is not compatible with the function signature
    '''
    The SE_UpdateOSIGroundTruth function returns a char array containing the osi GroundTruth serialized to a string
    '''

    def updateOSIGroundTruth(self):
        self.se.SE_UpdateOSIGroundTruth()
        return True

    '''
    The SE_GetOSIGroundTruth function returns a char array containing the osi GroundTruth serialized to a string
    '''

    def getOSIGroundTruth(self, sizelist):
        cint = c_int(0)
        strc = self.se.SE_GetOSIGroundTruth(byref(cint))
        return (cint, strc)

    '''
    The SE_GetOSIGroundTruthRaw function returns a char array containing the OSI GroundTruth information
    @return osi3::GroundTruth*   % QUESTION : IS this correct or its a char array ?
    '''

    def getOSIGroundTruthRaw(self):
        return self.se.SE_GetOSIGroundTruthRaw()

    '''
    The SE_GetOSIRoadLane function returns a char array containing the osi Lane information/message of the lane where the object with object_id is, serialized to a string
    '''

    ### TODO: Detect right encoding and convert return value
    def getOSIRoadLane(self, object_id):
        cint = c_int(0)
        strc = self.se.SE_GetOSIRoadLane(byref(cint), object_id)
        return (cint, strc)

    '''
    The SE_GetOSIRoadLane function returns a char array containing the osi Lane Boundary information/message with the specified GLOBAL id
    '''

    ### TODO: Detect right encoding and convert return value
    def getOSILaneBoundary(self, global_id):
        cint = c_int(0)
        strc = self.se.SE_GetOSILaneBoundary(byref(cint), global_id)
        return (cint, strc)

    '''
    The SE_GetOSILaneBoundaryIds function the global ids for left, far elft, right and far right lane boundaries
    @param object_id Handle to the object to which the sensor should be attached
    @param ids Reference to a struct which will be filled with the Ids
    '''

    def getOSILaneBoundaryIds(self, object_id):
        state = LaneBoundaryId()
        self.se.SE_GetOSILaneBoundaryIds(object_id, byref(state))
        return state._fields_

    '''
    The SE_GetOSISensorDataRaw function returns a char array containing the OSI SensorData information
    @return osi3::SensorData*
    '''

    def getOSISensorDataRaw(self):
        return self.se.SE_GetOSISensorDataRaw()  # TODO encode or decode?

    '''
    Create and open osi file
    '''

    def OSIFileOpen(self, filename):
        return self.se.SE_OSIFileOpen(filename.encode())

    '''
    Create and open osi file
    '''

    def OSIFileWrite(self, flush=False):
        return self.se.SE_OSIFileWrite(flush)

    ################### Viewer settings

    '''
    The SE_GetOSILaneBoundaryIds function the global ids for left, far elft, right and far right lane boundaries 
    @param featureType Type of the features, see viewer::NodeMask typedef
    @param enable Set true to show features, false to hide
    '''

    def viewerShowFeature(self, featureType, enable):
        self.se.SE_ViewerShowFeature(featureType, enable)
        return True

    #################### Simple vehicle
    '''
    Create an instance of a simplistic vehicle based on a 2D bicycle kincematic model
    @param x Initial position X world coordinate
    @param y Initial position Y world coordinate
    @param h Initial heading
    @param length Length of the vehicle
    @return Handle to the created object
    '''

    def simpleVehicleCreate(self, x, y, h, length):
        self.se.SE_SimpleVehicleCreate.errcheck = lambda v, *a: cast(v, c_void_p)  ### TODO ?
        return self.se.SE_SimpleVehicleCreate(x, y, h, length)

    '''
    Delete an instance of the simplistic vehicle model
    '''

    def simpleVehicleDelete(self, handleSimpleVehicle):
        self.se.SE_SimpleVehicleDelete(handleSimpleVehicle)
        return True

    '''
    Control the speed and steering with discreet [-1, 0, 1] values, suitable for keyboard control (e.g. up/none/down).
    The function also steps the vehicle model, updating its position according to motion state and timestep.
    @param dt timesStep (s)
    @param throttle Longitudinal control, -1: brake, 0: none, +1: accelerate
    @param steering Lateral control, -1: left, 0: straight, 1: right
    '''

    def simpleVehicleControlBinary(self, handleSimpleVehicle, dt, throttle,
                                   steering):  # throttle and steering [-1, 0 or 1]
        self.se.SE_SimpleVehicleControlBinary(handleSimpleVehicle, dt, throttle, steering)
        return True

    '''
    Control the speed and steering with floaing values in the range [-1, 1], suitable for driver models.
    The function also steps the vehicle model, updating its position according to motion state and timestep.
    @param dt timesStep (s)
    @param throttle Longitudinal control, -1: maximum brake, 0: no acceleration, +1: maximum acceleration
    @param steering Lateral control, -1: max left, 0: straight, 1: max right
    '''

    def simpleVehicleControlAnalog(self, handleSimpleVehicle, dt, throttle,
                                   steering):  # throttle and steering [-1, 0 or 1]
        self.se.SE_SimpleVehicleControlAnalog(handleSimpleVehicle, dt, throttle, steering);
        return True

    '''
    Set maximum vehicle speed.
    @param speed Maximum speed (m/s)
    '''

    def simpleVehicleSetMaxSpeed(self, handleSimpleVehicle, speed):
        self.se.SE_SimpleVehicleSetMaxSpeed(handleSimpleVehicle, speed)
        return True

    '''
    Get current state of the vehicle. Typically called after Control has been applied.
    @param state Pointer/reference to a SE_SimpleVehicleState struct to be filled in
    '''

    def simpleVehicleGetState(self, handleSimpleVehicle):
        state = SimpleVehicleState()
        self.se.SE_SimpleVehicleGetState(handleSimpleVehicle, byref(state))
        return state
