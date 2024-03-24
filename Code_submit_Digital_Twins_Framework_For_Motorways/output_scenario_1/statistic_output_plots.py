import xml.etree.ElementTree as et

import matplotlib.pyplot as plt
import numpy as np


def get_statistic_data(xroot):
    vehicles = xroot[0]
    vehicleTripStatistics = xroot[4]

    running_vehicle = int(vehicles.get("running"))
    speed = float(vehicleTripStatistics.get("speed"))

    return running_vehicle, speed

xtree_statistic_pe = et.parse("statistic_physical_entity.xml")
xtree_statistic_1 = et.parse("statistic1.xml")
xtree_statistic_2 = et.parse("statistic2.xml")
xtree_statistic_3 = et.parse("statistic3.xml")
xroot_statistic_pe = xtree_statistic_pe.getroot()
xroot_statistic_1 = xtree_statistic_1.getroot()
xroot_statistic_2 = xtree_statistic_2.getroot()
xroot_statistic_3 = xtree_statistic_3.getroot()

running_vehicle_pe, speed_pe = get_statistic_data(xroot_statistic_pe)
running_vehicle_1, speed_1 = get_statistic_data(xroot_statistic_1)
running_vehicle_2, speed_2 = get_statistic_data(xroot_statistic_2)
running_vehicle_3, speed_3 = get_statistic_data(xroot_statistic_3)

labels = ['Physical entity', 'DT 1st run', 'DT 2nd run', 'DT 3rd run']
running_veh_values = [running_vehicle_pe, running_vehicle_1, running_vehicle_2, running_vehicle_3]

fig, ax = plt.subplots()

bars = ax.bar(labels, running_veh_values,alpha =0.8,  width=0.4)
ax.bar_label(bars, fontsize=6)
ax.set_ylabel("No. of running vehicles", fontsize=10)
ax.set_ylim(0,2000)
ax.set_title("Number of running vehicles in the simulation for Scenario 1", fontsize=12)
plt.savefig('running_veh.png')
plt.show()

#average
running_dt_average = (running_vehicle_1 + running_vehicle_2 + running_vehicle_3 )/3

running_veh_dt_arr = np.array([running_vehicle_1,running_vehicle_2,running_vehicle_3])
running_veh_values_dt_mean = np.mean(running_veh_dt_arr)
running_veh_values_dt_std = np.std(running_veh_dt_arr)

running_veh_arr = np.array([running_vehicle_pe,running_vehicle_pe,running_vehicle_pe])
running_veh_values_mean = np.mean(running_veh_arr)
running_veh_values_std = np.std(running_veh_arr)

CTEs = [ running_veh_values_mean, running_veh_values_dt_mean]
error = [ running_veh_values_std, running_veh_values_dt_std]
x_pos = np.arange(2)

fig, ax = plt.subplots()
bars = ax.bar(x_pos, CTEs, yerr=error, align='center', ecolor='black', alpha =0.8,  capsize=10, width = 0.4)
ax.bar_label(bars, fontsize=6)
ax.set_ylabel("No. of running vehicles", fontsize=10)
ax.set_xticks(x_pos)
ax.set_ylim(0,2000)
ax.set_xticklabels(['Physical entity', 'Digital Twin'])
ax.set_title("Number of running vehicles in the simulation for Scenario 1", fontsize=10)
plt.savefig('running_veh_avg.png',)
plt.show()


#Speed
speed_vehicles = [speed_pe, speed_1, speed_2, speed_3]
# fig = plt.figure(figsize = (7, 4))
fig, ax = plt.subplots()
bars = ax.bar(labels, speed_vehicles, width=0.4, alpha =0.8)
ax.bar_label(bars, fontsize=6)
ax.set_ylabel("Average speed", fontsize=10)
ax.set_ylim(0,30)
ax.set_title("Average speed of vehicles in the simulation for Scenario 1", fontsize=12)
plt.savefig('speed.png')
plt.show()



#average
speed_dt_average = (speed_1 + speed_2 + speed_3)/3

speed_dt_arr = np.array([speed_1,speed_2,speed_3])
speed_dt_mean = np.mean(speed_dt_arr)
speed_dt_std = np.std(speed_dt_arr)

speed_arr = np.array([speed_pe,speed_pe,speed_pe])
speed_values_mean = np.mean(speed_arr)
speed_values_std = np.std(speed_arr)

CTEs = [ speed_values_mean, speed_dt_mean]
error = [ speed_values_std, speed_dt_std]
x_pos = np.arange(2)

fig, ax = plt.subplots()
bars = ax.bar(x_pos, CTEs, yerr=error, align='center', ecolor='black', alpha =0.8,  capsize=10, width = 0.4)
ax.bar_label(bars, fontsize=6)
ax.set_ylabel("Average speed", fontsize=10)
ax.set_xticks(x_pos)
ax.set_ylim(0,30)
ax.set_xticklabels(['Physical entity', 'Digital Twin'])
ax.set_title("Average speed of vehicles in the simulation for Scenario 1", fontsize=12)
plt.savefig('speed_avg.png')
plt.show()
