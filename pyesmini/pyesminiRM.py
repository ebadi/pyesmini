from ctypes import *
import ctypes
from .shared import *


# /home/wave/repositories/QtEsmini/pyesmini/pyesmini/esminiRMLib.hpp: 34
class PositionData(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('h', c_float),
        ('p', c_float),
        ('r', c_float),
        ('hRelative', c_float),
        ('roadId', c_int),
        ('laneId', c_int),
        ('laneOffset', c_float),
        ('s', c_float),
    ]


# /home/wave/repositories/QtEsmini/pyesmini/pyesmini/esminiRMLib.hpp: 45
class RoadLaneInfo(Structure):
    _fields_ = [
        ('pos', c_float * int(3)),
        ('heading', c_float),
        ('pitch', c_float),
        ('roll', c_float),
        ('width', c_float),
        ('curvature', c_float),
        ('speed_limit', c_float),
    ]


# /home/wave/repositories/QtEsmini/pyesmini/pyesmini/esminiRMLib.hpp: 52
class RoadProbeInfo(Structure):
    _fields_ = [
        ('road_lane_info', RoadLaneInfo),
        ('relative_pos', c_float * int(3)),
        ('relative_h', c_float),
    ]


# /home/wave/repositories/QtEsmini/pyesmini/pyesmini/esminiRMLib.hpp: 59
class PositionDiff(Structure):
    _fields_ = [
        ('ds', c_float),
        ('dt', c_float),
        ('dLaneId', c_int),
    ]


class PyEsminiRM:
    # def RM_Init(const char *odrFilename); ### TODO: What is the return value?
    def __init__(self, odrFilename):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        if platform == "linux" or platform == "linux2":
            self.se = CDLL(dir_path + "/libesminiRMLib.so")
        elif platform == "darwin":
            self.se = CDLL(dir_path + "/libesminiRMLib.dylib")
        elif platform == "win32":
            self.se = CDLL(dir_path + "\libesminiRMLib.dll")
        else:
            print("Unsupported platform: {}".format(platform))
            raise Exception("Loading shared library: shared library not found")

        self.se.RM_CreatePosition.argtypes = []
        self.se.RM_CreatePosition.restype = c_int

        self.se.RM_GetNrOfPositions.argtypes = []
        self.se.RM_GetNrOfPositions.restype = c_int

        self.se.RM_DeletePosition.argtypes = [c_int]
        self.se.RM_DeletePosition.restype = c_int

        self.se.RM_GetNumberOfRoads.argtypes = []
        self.se.RM_GetNumberOfRoads.restype = c_int

        self.se.RM_GetIdOfRoadFromIndex.argtypes = [c_int]
        self.se.RM_GetIdOfRoadFromIndex.restype = c_int

        self.se.RM_GetRoadLength.argtypes = [c_int]
        self.se.RM_GetRoadLength.restype = c_float

        self.se.RM_GetRoadNumberOfLanes.argtypes = [c_int, c_float]
        self.se.RM_GetRoadNumberOfLanes.restype = c_int

        self.se.RM_GetLaneIdByIndex.argtypes = [c_int, c_int, c_float]
        self.se.RM_GetLaneIdByIndex.restype = c_int

        self.se.RM_GetLaneIdByIndex.argtypes = [c_int, c_int, c_float, c_float, c_bool]
        self.se.RM_GetLaneIdByIndex.restype = c_int

        self.se.RM_SetS.argtypes = [c_int, c_float]
        self.se.RM_SetS.restype = c_int

        self.se.RM_SetWorldPosition.argtypes = [c_int, c_float, c_float, c_float, c_float, c_float, c_float]
        self.se.RM_SetWorldPosition.restype = c_int

        self.se.RM_SetWorldXYHPosition.argtypes = [c_int, c_float, c_float, c_float]
        self.se.RM_SetWorldXYHPosition.restype = c_int

        self.se.RM_SetWorldXYHPosition.argtypes = [c_int, c_float, c_float, c_float]
        self.se.RM_SetWorldXYHPosition.restype = c_int

        self.se.RM_PositionMoveForward.argtypes = [c_int, c_float, c_int]
        self.se.RM_PositionMoveForward.restype = c_int

        self.se.RM_GetPositionData.argtypes = [c_int, POINTER(PositionData)]
        self.se.RM_GetPositionData.restype = c_int

        self.se.RM_GetSpeedLimit.argtypes = [c_int]
        self.se.RM_GetSpeedLimit.restype = c_float

        self.se.RM_GetLaneInfo.argtypes = [c_int, c_float, POINTER(RoadLaneInfo), c_int]
        self.se.RM_GetLaneInfo.restype = c_int

        self.se.RM_GetProbeInfo.argtypes = [c_int, c_float, POINTER(RoadProbeInfo), c_int]
        self.se.RM_GetProbeInfo.restype = c_int

        self.se.RM_SubtractAFromB.argtypes = [c_int, c_int, POINTER(PositionDiff)]
        self.se.RM_SubtractAFromB.restype = c_int

        self.se.RM_Init.argtypes = [String]
        self.se.RM_Init.restype = c_int
        self.se.RM_Init(odrFilename)

    def RM_Close(self):
        self.se.RM_Close.argtypes = []
        self.se.RM_Close.restype = c_int
        return self.se.RM_Close()

    '''
    Create a position object
    @return Handle to the position object, to use for operations
    '''

    def RM_CreatePosition(self):
        return self.se.RM_CreatePosition()

    '''
    Get the number of created position objects
    @return Number of created position objects
    '''

    def RM_GetNrOfPositions(self):
        return self.se.RM_GetNrOfPositions()

    '''
    Delete one or all position object(s)
    @param hande Handle to the position object. Set -1 to delete all.
    @return 0 if succesful, -1 if specified position(s) could not be deleted
    '''

    def RM_DeletePosition(self, handle):
        if self.se.RM_DeletePosition() < 0:
            return False
        else:
            return True

    '''
    Get the total number fo roads in the road network of the currently loaded OpenDRIVE file.
    @return Number of roads
    '''

    def RM_GetNumberOfRoads(self):
        return self.se.RM_GetNumberOfRoads()

    '''
    Get the Road ID of the road with specified index. E.g. if there are 4 roads, index 3 means the last one.
    @param index The index of the road
    @return The ID of the road
    '''

    def RM_GetIdOfRoadFromIndex(self, index):
        return self.se.RM_GetIdOfRoadFromIndex()

    '''
    Get the lenght of road with specified ID
    @param id The road ID 
    @return The length of the road if ID exists, else 0.0
    '''

    def RM_GetRoadLength(self, id):
        return self.se.RM_GetRoadLength()

    '''
    Get the number of drivable lanes of specified road
    @param roadId The road ID
    @param s The distance along the road at what poto check number of lanes (which can vary along the road)
    @return The number of drivable lanes
    '''

    def RM_GetRoadNumberOfLanes(self, roadId, s):
        return self.se.RM_GetRoadNumberOfLanes()

    '''
    Get the ID of the lane given by index
    @param roadId The road ID
    @param laneIndex The index of the lane 
    @param s The distance along the road at what poto look up the lane ID
    @return The lane ID
    '''

    def RM_GetLaneIdByIndex(self, roadId, laneIndex, s):
        return self.se.RM_GetLaneIdByIndex()

    '''
    Set position from road coordinates, world coordinates being calculated
    @param handle Handle to the position object
    @param roadId Road specifier
    @param laneId Lane specifier
    @param laneOffset Offset from lane center
    @param s Distance along the specified road
    @param align If true the heading will be reset to the lane driving direction (typically only at initialization)
    @return 0 if successful, -1 if not
    '''

    def RM_SetLanePosition(self, handle, roadId, laneId, laneOffset, s, align=True):
        if self.se.RM_GetLaneIdByIndex(handle, roadId, laneId, laneOffset, s, align) < 0:
            return False
        else:
            return True

    '''
    Set s (distance) part of a lane position, world coordinates being calculated
    @param handle Handle to the position object
    @param s Distance along the specified road
    @return 0 if successful, -1 if not
    '''

    def RM_SetS(self, handle, s):
        if self.se.RM_SetS(handle, s) < 0:
            return False
        else:
            return True

    '''
    Set position from world coordinates, road coordinates being calculated
    @param handle Handle to the position object
    @param x cartesian coordinate x value
    @param y cartesian coordinate y value
    @param z cartesian coordinate z value
    @param h rotation heading value
    @param p rotation pitch value
    @param r rotation roll value
    @return 0 if successful, -1 if not
    '''

    def RM_SetWorldPosition(self, handle, x, y, z, h, p, r):
        if self.se.RM_SetWorldPosition(handle, x, y, z, h, p, r) < 0:
            return False
        else:
            return True

    '''
    Set position from world X, Y and heading coordinates; Z, pitch and road coordinates being calculated
    @param handle Handle to the position object
    @param x cartesian coordinate x value
    @param y cartesian coordinate y value
    @param h rotation heading value
    @return 0 if successful, -1 if not
    '''

    def RM_SetWorldXYHPosition(self, handle, x, y, h):
        if self.se.RM_SetWorldXYHPosition(handle, x, y, h) < 0:
            return False
        else:
            return True

    '''
    Set position from world X, Y, Z and heading coordinates; pitch and road coordinates being calculated
    Setting a Z value may have effect in mapping the position to the closest road, e.g. overpass
    @param handle Handle to the position object
    @param x cartesian coordinate x value
    @param y cartesian coordinate y value
    @param h rotation heading value
    @return 0 if successful, -1 if not
    '''

    def RM_SetWorldXYHPosition(self, handle, x, y, h):
        if self.se.RM_SetWorldXYHPosition(handle, x, y, h) < 0:
            return False
        else:
            return True

    '''
    Move position forward along the road. Choose way randomly though any junctions.
    @param handle Handle to the position object
    @param dist Distance (meter) to move
    @param strategy How to move in a junction where multiple route options appear, see Junction::JunctionStrategyType
    @return 0 if successful, -1 if not
    '''

    def RM_PositionMoveForward(self, handle, dist, strategy):
        if self.se.RM_PositionMoveForward(handle, dist, strategy) < 0:
            return False
        else:
            return True

    '''
    Get the fields of the position of specified index
    @param handle Handle to the position object
    @param data Struct to fill in the values
    @return 0 if successful, -1 if not
    '''

    def RM_GetPositionData(self, handle):
        # PositionData *data
        positionData = PositionData()
        if self.se.RM_GetPositionData(handle, positionData) < 0:
            return None
        else:
            return positionData

    '''
    Retrieve current speed limit (at current road, s-value and lane) based on ODR type elements or nr of lanes
    @param handle Handle to the position object
    @return 0 if successful, -1 if not
    '''

    def RM_GetSpeedLimit(self, handle):
        if self.se.RM_GetSpeedLimit(handle) < 0:
            return False
        else:
            return True

    '''
    Retrieve lane information from the position object (at current road, s-value and lane)
    @param handle Handle to the position object
    @param lookahead_distance The distance, along the road, to the poof interest
    @param data Struct including all result values, see RoadLaneInfo typedef
    @param lookAheadMode Measurement strategy: Along reference lane, lane center or current lane offset. See roadmanager::Position::LookAheadMode enum
    @return 0 if successful, -1 if not
    '''

    def RM_GetLaneInfo(self, handle, lookahead_distance, lookAheadMode):
        # RoadLaneInfo *data
        roadLaneInfo = RoadLaneInfo()
        if self.se.RM_GetLaneInfo(handle, lookahead_distance, roadLaneInfo, lookAheadMode) < 0:
            return None
        else:
            return roadLaneInfo

    '''
    As RM_GetLaneInfo plus relative location of poof interest (probe) from current position
    @param handle Handle to the position object from which to measure
    @param lookahead_distance The distance, along the road to the probe (poof interest)
    @param data Struct including all result values, see RoadProbeInfo typedef
    @param lookAheadMode Measurement strategy: Along reference lane, lane center or current lane offset. See roadmanager::Position::LookAheadMode enum
    @return 0 if successful, -1 if not
    '''

    def RM_GetProbeInfo(handle, lookahead_distance, lookAheadMode):
        # RoadProbeInfo *data
        roadProbeInfo = RoadProbeInfo()
        if self.se.RM_GetProbeInfo(handle, lookahead_distance, roadProbeInfo, lookAheadMode) < 0:
            return None
        else:
            return roadProbeInfo

    '''
    Find out the difference between two position objects, i.e. delta distance (long and lat) and delta laneId
    @param handleA Handle to the position object from which to measure
    @param handleB Handle to the position object to which the distance is measured
    @param pos_diff Struct including all result values, see PositionDiff typedef
    @return true if a valid path between the road positions was found and calculations could be performed
    '''

    def RM_SubtractAFromB(handleA, handleB):
        # PositionDiff *pos_diff
        positionDiff = PositionDiff()
        return self.se.RM_SubtractAFromB(handleA, handleB, positionDiff)
