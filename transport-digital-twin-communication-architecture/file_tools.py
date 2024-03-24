import os, errno

def writeMessageToFile(partition, topic, data):
    path = './consumed_topics/'+str(topic)+'/'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(path+str(partition)+'.txt', "a") as f:
        f.write(str(data)+'\n')
    

def writeLatencyToFile(topic, latency):
    path = './test_results/latency_results/'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(path+str(topic)+'.txt', "a") as f:
        f.write(str(latency)+',')


def writeTestInfoToFile(end_time, real_duration_s, sim_duration_s, broker, enterprise):
    path = './test_results/'
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(path+'test_info.txt', "a") as f:
        f.write('Simulation end time:'+str(end_time)+'\n')
        f.write('Simulation time duration (seconds):'+str(real_duration_s)+'\n')
        f.write('Simulation time duration (simulated seconds):'+str(sim_duration_s)+'\n')
        f.write('Broker EP:'+str(broker)+'\n')
        f.write('Enterprise EP:'+str(enterprise)+'\n')