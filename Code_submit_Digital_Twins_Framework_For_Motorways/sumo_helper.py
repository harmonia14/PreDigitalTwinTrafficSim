import math
import os
import sys

import sumolib

from constants import CAMERA_LOOKUP, TOLL_BRIDGE, EARTH_EQUATORIAL_METERS_PER_DEGREE


def SUMO_HOME_TOOLS():
    if 'SUMO_HOME' in os.environ:
        tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
        sys.path.append(tools)
        print("SUMO_HOME environment variable present!")
    else:
        print("please declare environment variable 'SUMO_HOME'")
        sys.exit("please declare environment variable 'SUMO_HOME'")


def approximate_destination(point, distance, theta):
    lon, lat = point
    radians_theta = math.radians(theta)
    dx = distance * math.cos(radians_theta)
    dy = distance * math.sin(radians_theta)

    dlon = dx / (EARTH_EQUATORIAL_METERS_PER_DEGREE * math.cos(math.radians(lat)))
    dlat = dy / EARTH_EQUATORIAL_METERS_PER_DEGREE

    return (lon + dlon, lat + dlat)



def mpsToKph(speed):
    return (speed * 3600) / 1000


def kphToMps(speed):
    return (speed * 1000) / 3600

def calculate_points_and_angle(x, y, edges, direction):
    min_dist = sys.maxsize

    for edge in edges:
        distance = ((((edge[0] - x) ** 2) + ((edge[1] - y) ** 2)) ** 0.5)
        if min_dist > distance:
            min_dist = distance
            min_points = edge

    point_1 = edges[0]
    point_2 = edges[-1]

    angle = math.atan2(point_1[1] - point_2[1], point_1[0] - point_2[0])
    angle = math.degrees(angle)
    if direction == 'N':
        angle = 360 + angle

    return min_points, angle


net = sumolib.net.readNet("ITSC2020_CAV_impact/workspace/M50network.net.xml")


def calculate_camera_values():
    for key, value in CAMERA_LOOKUP.items():
        lon_lat = value['coordinates']
        lon_lat_arr = lon_lat.split(',')
        lon = lon_lat_arr[0]
        lat = lon_lat_arr[1]
        x, y = net.convertLonLat2XY(lon, lat)
        north_edges = net.getEdge(value['northEdges'].split(',')[0]).getShape()
        south_edges = net.getEdge(value['southEdges'].split(',')[0]).getShape()

        north_start_edges, north_angle = calculate_points_and_angle(x, y, north_edges, 'N')
        south_start_edges, south_angle = calculate_points_and_angle(x, y, south_edges, 'S')
        value['north_start_edges'] = north_start_edges
        value['north_angle'] = north_angle
        value['south_start_edges'] = south_start_edges
        value['south_angle'] = south_angle


def calculate_toll_bridge_values():
        lon_lat = TOLL_BRIDGE['coordinates']
        lon_lat_arr = lon_lat.split(',')
        lon = lon_lat_arr[0]
        lat = lon_lat_arr[1]
        x, y = net.convertLonLat2XY(lon, lat)
        north_edges = net.getEdge(TOLL_BRIDGE['northEdges'].split(',')[0]).getShape()
        south_edges = net.getEdge(TOLL_BRIDGE['southEdges'].split(',')[0]).getShape()

        north_start_edges, north_angle = calculate_points_and_angle(x, y, north_edges, 'N')
        south_start_edges, south_angle = calculate_points_and_angle(x, y, south_edges, 'S')
        TOLL_BRIDGE['north_start_edges'] = north_start_edges
        TOLL_BRIDGE['north_angle'] = north_angle
        TOLL_BRIDGE['south_start_edges'] = south_start_edges
        TOLL_BRIDGE['south_angle'] = south_angle
