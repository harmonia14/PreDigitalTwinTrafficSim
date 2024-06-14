#!/usr/bin/env python3.11

from kafka import KafkaProducer
from constants import BROKER_EP, ENTERPRISE_EP, ENCODING, SUMO_CMD, M50_Northbound, M50_Southbound, NB_PARTITION, SB_PARTITION, SIMULATION_DURATION, KAFKA_VERSION, SUMO_CFG
from kafka_helper import sendCamData, sendProbeData, sendTollData, sendData, initTopics
from sumo_helper import SUMO_HOME_TOOLS, getTimeStamp, appendLoopCount, getLoopData
from datetime import date, datetime
import file_tools as file
import traci, time

def getSimulationTimeCfg(filepath: str) -> dict:
    from xml.etree import ElementTree as ET

    result = {'begin': 0.0, 'end': 0.0, 'step_len': 0.0}
    xmltree = ET.parse(filepath)
    xmlroot = xmltree.getroot()
    timecfg = xmlroot.find('./time')
    if not timecfg:
        return result

    result['begin'] = float(timecfg.find('begin').get('value'))
    result['end'] = float(timecfg.find('end').get('value'))
    result['step_len'] = float(timecfg.find('step-length').get('value'))
    return result

SUMO_HOME_TOOLS() #checks for sumo dependancy

comp = 'gzip'
print("Starting producers...")
print("Connecting to cluster at:", BROKER_EP)

north_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION, compression_type=comp)
south_loop_producer = KafkaProducer(bootstrap_servers=BROKER_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION, compression_type=comp)


print("Starting enterprise producers...")

toll_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
camera_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)
probe_producer = KafkaProducer(bootstrap_servers=ENTERPRISE_EP, value_serializer=ENCODING, api_version=KAFKA_VERSION)

print("Connected to enterprise cluster at:", ENTERPRISE_EP)

date = date.today()
initTopics()

simu_end_time = getSimulationTimeCfg(SUMO_CFG)['end']
if simu_end_time:
     SIMULATION_DURATION = simu_end_time

while True:
        print("Waiting to start simulation...")
        traci.start(SUMO_CMD)
        print("Simulation started...")
        start_t = time.time()
        t = 0
        loopData = []
        sCount = [0,0,0,0]
        nCount = [0,0,0,0]
        while t<SIMULATION_DURATION:
            traci.simulationStep()
            vehIDs = traci.vehicle.getIDList()
            t = traci.simulation.getTime()
            timestamp = getTimeStamp(date, t)
            
            has_inductive_loops = True
            try:
                nCount = appendLoopCount(M50_Northbound, nCount)
                sCount = appendLoopCount(M50_Southbound, sCount)
            
            except traci.TraCIException as traci_except:
                print("Traffic Control Exception:", traci_except)
                has_inductive_loops = False

            if t%1 == 0:
                sendProbeData(vehIDs, probe_producer, timestamp, "enterprise_probe_vehicles") 
                sendCamData(vehIDs, camera_producer, timestamp, "enterprise_motorway_cameras")
                sendTollData(vehIDs, toll_producer, timestamp, "enterprise_toll_bridge_cameras") 

                if has_inductive_loops:
                    sendData(getLoopData(M50_Northbound, timestamp, nCount), north_loop_producer, "inductive_loops", NB_PARTITION)
                    sendData(getLoopData(M50_Southbound, timestamp, sCount), south_loop_producer, "inductive_loops", SB_PARTITION)
                sCount = [0,0,0,0]
                nCount = [0,0,0,0]

        end_time = datetime.now()
        real_duration_s = time.time()-start_t
        print('Simulation finished at', end_time)
        print('Total sim time in seconds: ', real_duration_s)
        file.writeTestInfoToFile(end_time, real_duration_s, SIMULATION_DURATION, BROKER_EP, ENTERPRISE_EP)
        
        traci.close()
        break

