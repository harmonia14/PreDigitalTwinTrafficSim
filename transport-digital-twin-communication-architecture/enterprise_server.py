#!/usr/bin/env python3.11

from kafka import KafkaConsumer, KafkaProducer
from constants import DECODING, BROKER_EP, ENTERPRISE_EP, ENCODING, TOPIC_LOOKUP
from kafka_helper import getPartition
from multiprocessing import Process

def consume(producerEP, consumerEP, topic):
     producer = KafkaProducer(bootstrap_servers=producerEP, value_serializer=ENCODING, compression_type='gzip')
     consumer = KafkaConsumer(bootstrap_servers=consumerEP, value_deserializer=DECODING)
     consumer.subscribe(topics=topic)
     for msg in consumer:  
          producer.send(TOPIC_LOOKUP[msg.topic], msg.value, partition=getPartition(msg))

if __name__ == '__main__':
     print("Enterprise consumer is running...")
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_motorway_cameras"])).start() 
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_toll_bridge_cameras"])).start()
     Process(target=consume, args=(BROKER_EP, ENTERPRISE_EP, ["enterprise_probe_vehicles"])).start()