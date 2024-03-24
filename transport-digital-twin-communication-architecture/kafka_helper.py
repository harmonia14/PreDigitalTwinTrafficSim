from sumo_helper import getProbeData, getProbeVehicleIDs, getCamVehicleIDs, getCamData, getTollData, getTollVehicleIDs, getTollData
from constants import CAMERA_LOOKUP, BROKER_EP, ENTERPRISE_EP, ENTERPRISE_TOPICS, KAFKA_VERSION
from kafka import KafkaAdminClient, KafkaConsumer
from kafka.admin import NewPartitions, NewTopic
import traci, time

#----------------------------------------------------------------------------------

#functions for working with kafka topics and partitions

#creates topics from list of topics 'TOPICS' in broker
def createTopics(TOPICS, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker, api_version=KAFKA_VERSION)
    admin_client.create_topics(new_topics=TOPICS, validate_only=False)
  
    print("Created topics in ", broker)
    for topic in TOPICS:
        print(topic.name)
        print("partitions:", get_partitions_number(broker, topic.name))

#creates topic and eppends it to list of to be created topics 
def appendTopics(topics, numPartitions, topic_name):
    topics.append(NewTopic(name=topic_name, num_partitions=numPartitions, replication_factor=1))
    return topics

#deletes topic from a broker
def delete_topics(topics, broker):
    admin_client = KafkaAdminClient(bootstrap_servers=broker, api_version=KAFKA_VERSION)
    admin_client.delete_topics(topics=topics)
    print("deleted topics")

#returns number of partitions in a topic
def get_partitions_number(broker, topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=broker,
        api_version=KAFKA_VERSION
    )
    partitions = consumer.partitions_for_topic(topic)
    return len(partitions)

#init script for consistant simulations, cleans topics on brokers for fresh start
def initTopics():
    for topic in list(KafkaConsumer(bootstrap_servers=BROKER_EP, api_version=KAFKA_VERSION).topics()):
         delete_topics([topic], BROKER_EP)
        
    for topic in list(KafkaConsumer(bootstrap_servers=ENTERPRISE_EP, api_version=KAFKA_VERSION).topics()):
        delete_topics([topic], ENTERPRISE_EP) 
    topics = []
    enterprise_topics = []
    topics = appendTopics(topics, 2, "inductive_loops")
    topics = appendTopics(topics, 8, "motorway_cameras")
    topics = appendTopics(topics, 2, "toll_bridge_cameras")
    topics = appendTopics(topics, 10, "probe_vehicles")  
    for topic in ENTERPRISE_TOPICS:
        enterprise_topics = appendTopics(enterprise_topics, 1, topic)
    createTopics(topics, BROKER_EP)  
    createTopics(enterprise_topics, ENTERPRISE_EP)
   
#gets the specific partition a message came from    
def getPartition(msg):
    if msg.topic == 'enterprise_motorway_cameras':
        return CAMERA_LOOKUP[msg.value['camera_id']]["partition"]
    return None

#creates a specificed number of partitions in a topic on the broker(s)
def createNewPartitions(SERVER, TOPIC, PARTITIONS):
    admin_client = KafkaAdminClient(bootstrap_servers=SERVER, api_version=KAFKA_VERSION)
    topic_partitions = {}
    topic_partitions[TOPIC] = NewPartitions(total_count=PARTITIONS)
    admin_client.create_partitions(topic_partitions)

#--------------------------------------------------------------------------------------

#functions for sending data to kafka brokers

def sendProbeData(vehicleIDs, producer, timestamp, topic):
    probes = getProbeVehicleIDs(vehicleIDs)
    for vehID in probes:
        data = getProbeData(vehID, timestamp)  
        sendData(data, producer, topic, None)

def sendCamData(vehicleIDs, producer, timestamp, topic):
    for cam in CAMERA_LOOKUP:
        camVehicles = getCamVehicleIDs(cam, vehicleIDs)
        for vehID in camVehicles:
            data = getCamData(vehID, cam, timestamp)
            sendData(data, producer, topic, None)

def sendTollData(vehicleIDs, producer, timestamp, topic):
    x, y = traci.simulation.convertGeo(float("-6.3829509"), float("53.3617409"), fromGeo=True)
    p1 = [x, y]
    tollVehicles = getTollVehicleIDs(vehicleIDs, p1)
    for vehID in tollVehicles:
        data = getTollData(vehID, p1, timestamp)
        sendData(data, producer, topic, None)

def sendData(data, producer, topic, partition):
    # data['sent_timestamp'] = time.time() # only used for latency calculations
    producer.send(topic=topic, value=data, partition=partition)