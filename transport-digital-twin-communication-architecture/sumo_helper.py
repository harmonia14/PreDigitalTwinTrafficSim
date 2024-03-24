import os, sys, traci, datetime, random, math
import numpy as np
from constants import CAMERA_LOOKUP, TOLL_BRIDGE, autonomousVehicles

def addDistanceNoise(p1, p2):
    d = calcDistance(p1, p2)
    return random.uniform(0.95*d, 1.05*d)

def addGeoDistanceNoise(coordinates):
    lon = coordinates[0]
    lat = coordinates[1]
    r  = 10/111300 #converts 10 metres into degrees
    w = r * math.sqrt(random.uniform(0, 1))
    t = 2 * math.pi * (random.uniform(0, 1))
    x = w * math.cos(t) 
    lon_e = x/math.cos(lat) 
    lat_e = w * math.sin(t)
    return lon+lon_e, lat+lat_e

def getTimeStamp(date, time):
    return str(date)+' '+str(datetime.timedelta(seconds=time))

def mpsToKph(speed):
    return (speed*3600)/1000

def addSpeedNoise(speed):
    return random.uniform(0.95*speed, 1.05*speed)

def SUMO_HOME_TOOLS():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        print("SUMO_HOME environment variable present!")
    else:
        print("please declare environment variable 'SUMO_HOME'")
        sys.exit("please declare environment variable 'SUMO_HOME'")

def getVehicleLocationGeo(vehID):
    x, y = traci.vehicle.getPosition(vehID)
    lat, lon = traci.simulation.convertGeo(float(x), float(y), fromGeo=False)
    return (lon, lat)

def calcDistance(p1, p2):
    return traci.simulation.getDistance2D(x1=float(p1[0]), y1=float(p1[1]), x2=float(p2[0]), y2=float(p2[1]), isGeo=False)

def getDirection(vehID, cam):
    edge = str(traci.vehicle.getRoadID(vehID))
    for i in cam["northEdges"].split(","):
        if i in edge:   
            return 'N'
    for i in cam["southEdges"].split(","):
        if i in edge:       
            return 'S'           
    return False

def getVehiclesInView(vehicleIDs, cam, r, dir):
    lon, lat = cam["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    vehicles = [] 
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if (dir == 'N' and p2[1] > p1[1]) or (dir == 'S' and p2[1] < p1[1]): 
            if calcDistance(p1, p2) < r and getDirection(vehID, cam):   
                vehicles.append(vehID)
    return vehicles

def getCamVehicleIDs(camera_id, vehicleIDs):
    return getVehiclesInView(vehicleIDs, CAMERA_LOOKUP[camera_id], 150, camera_id[4])

def getCamData(vehID, camera_id, timestamp):
    lon, lat = CAMERA_LOOKUP[camera_id]["coordinates"].split(",")
    x, y = traci.simulation.convertGeo(float(lat), float(lon), fromGeo=True)
    p1 = [x, y]
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    data = {
        'camera_id': str(camera_id),
        'lane_id': str(traci.vehicle.getRoadID(vehID)),
        'lane_index': str(traci.vehicle.getLaneIndex(vehID)),
        'direction': str(getDirection(vehID, CAMERA_LOOKUP[camera_id])),
        'distance': str(addDistanceNoise(p1, p2)),
        'speed': str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        'timestamp': str(timestamp)
    }
    return data
 
def getLoopData(loopID, timestamp, counts):
    data = { 
        'loop_id': str(loopID[0][:-2]),
        'lane 1': str(counts[0]),
        'lane 2': str(counts[1]),
        'lane 3': str(counts[2]),
        'lane 4': str(counts[3]),
        'timestamp': str(timestamp)
    }
    return data

def getLoopLaneCounts(loopID):
    counts = []
    for i in range(4):
        counts.append(traci.inductionloop.getLastStepVehicleNumber(loopID[i]))
    return counts

def appendLoopCount(loopID, currentCount):
    return np.add(currentCount, getLoopLaneCounts(loopID))

def getProbeVehicleIDs(IDsOfVehicles):
    probes = []
    for vehID in IDsOfVehicles:      
        if traci.vehicle.getTypeID(vehID) in autonomousVehicles:
            probes.append(vehID)
    return probes

def getProbeData(vehID, timestamp):
    data = {
        'probe_id': str(vehID),
        'location': str(addGeoDistanceNoise(getVehicleLocationGeo(vehID))),
        'speed': str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        'vehicle type': traci.vehicle.getTypeID(vehID),
        'timestamp': str(timestamp)
    }
    return data

def getTollVehicleIDs(vehicleIDs, p1):
    return getVehiclesInViewToll(vehicleIDs, 100, p1)

def getVehiclesInViewToll(vehicleIDs, r, p1):
    vehicles = [] 
    for vehID in vehicleIDs:
        x, y = traci.vehicle.getPosition(vehID)
        p2 = [x, y]
        if calcDistance(p1, p2) < r and getDirection(vehID, TOLL_BRIDGE):   
                vehicles.append(vehID)
    return vehicles

def getTollData(vehID, p1, timestamp):
    x, y = traci.vehicle.getPosition(vehID)
    p2 = [x, y]
    data = {
        'lane_id': str(traci.vehicle.getRoadID(vehID)),
        'lane_index': str(traci.vehicle.getLaneIndex(vehID)),
        'direction': str(getDirection(vehID, TOLL_BRIDGE)),
        'distance': str(addDistanceNoise(p1, p2)),
        'speed': str(round(addSpeedNoise(mpsToKph(traci.vehicle.getSpeed(vehID))), 2)),
        'class': str(traci.vehicle.getVehicleClass(vehID)),
        'timestamp': str(timestamp)
    }
    return data



 