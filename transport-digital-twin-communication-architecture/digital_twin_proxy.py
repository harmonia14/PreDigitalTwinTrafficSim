from kafka import KafkaConsumer
from constants import DECODING, BROKER_EP
import file_tools as file
from multiprocessing import Process
import time

def consume(EP, TOPIC):
     consumer = KafkaConsumer(bootstrap_servers=EP, value_deserializer=DECODING)
     consumer.subscribe(topics=TOPIC)
     print(TOPIC[0], "consumer is running...")
     for msg in consumer:  
          # Used for latency calculations 
          # latency = (time.time() - float(msg.value['sent_timestamp']))*1000    
          # file.writeLatencyToFile(msg.topic, latency)
          file.writeMessageToFile(msg.partition, msg.topic, msg.value)

if __name__ == '__main__':
     print("Starting consumers...") 
     Process(target=consume, args=(BROKER_EP, ["inductive_loops"])).start()
     Process(target=consume, args=(BROKER_EP, ["probe_vehicles"])).start()
     Process(target=consume, args=(BROKER_EP, ["motorway_cameras"])).start()
     Process(target=consume, args=(BROKER_EP, ["toll_bridge_cameras"])).start()
     

    

     