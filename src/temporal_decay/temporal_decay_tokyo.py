import os
import time
import json
import numpy as np
import pandas as pd
import random
import geopandas as gpd

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
#  # 1. Read files
#------------------------------------------------------------------------------

folder = "2023_YJ_MI_MA/"
mob_file = folder + "result_5_temporal_model_figure_5/tokyo/all_mob_seq/"
web_file = folder + "result_5_temporal_model_figure_5/tokyo/all_web_seq/"

folder_index = ["01", "02", "03", "04", "05", "06", "07", "08", "09"]
all_mob_seq = dict()

for i in range(len(folder_index)):
    mob_seq = dict()

    folder_name = mob_file + "/" + folder_index[i]
    all_files = os.listdir(folder_name)

    for a_file in all_files:
        print(a_file)
        if a_file[-4:] == "json":
            with open(folder_name+"/"+a_file, 'r') as file:
                mob_seq = json.load(file)

                for user in mob_seq:
                    if int(user) < 100000:
                        if user not in all_mob_seq:
                            all_mob_seq[user] = mob_seq[user]
                        else:
                            for poi_type in mob_seq[user]:
                                if poi_type not in all_mob_seq[user]:
                                    all_mob_seq[user][poi_type] = mob_seq[user][poi_type]
                                else:
                                    all_mob_seq[user][poi_type] += mob_seq[user][poi_type]

folder_index = ["010203", "040506", "070809"]
all_web_seq = dict()
for i in range(len(folder_index)):
    web_seq = dict()

    folder_name = web_file + "/" + folder_index[i]
    all_files = os.listdir(folder_name)

    for a_file in all_files:
        print(a_file)
        if a_file[-4:] == "json":
            with open(folder_name+"/"+a_file, 'r') as file:
                web_seq = json.load(file)

                for user in web_seq:
                    if int(user) < 100000:
                        if user not in all_web_seq:
                            all_web_seq[user] = web_seq[user]
                        else:
                            for poi_type in web_seq[user]:
                                if poi_type not in all_web_seq[user]:
                                    all_web_seq[user][poi_type] = web_seq[user][poi_type]
                                else:
                                    all_web_seq[user][poi_type] += web_seq[user][poi_type]

#------------------------------------------------------------------------------
# # 2. Plot distirbution
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# # 2.1 Compute gaps
#------------------------------------------------------------------------------

#Web search: POI type: [Day1, Day2, ..., Dayk]
#Mobility: POI type: [Day1, Day2, ..., Dayk]

def obtain_three_gaps(mob_seq, web_seq):
    three_gaps = {"gap_mob_mob":[], "gap_web_mob":[], "gap_web_web":[]}

    mob_day_int = [int(day[-2:]) for day in mob_seq]
    mob_day_int.sort()
    if len(mob_day_int) > 1:
        gap_mob_mob = [mob_day_int[i+1]-mob_day_int[i] for i in range(len(mob_day_int)-1)]
    else:
        gap_mob_mob = []

    web_day_int = [int(day[-2:]) for day in web_seq]
    web_day_int.sort()
    if len(web_day_int) > 1:
        gap_web_web = [web_day_int[i+1]-web_day_int[i] for i in range(len(web_day_int)-1)]
    else:
        gap_web_web = []

    three_gaps["gap_mob_mob"] = gap_mob_mob
    three_gaps["gap_web_web"] = gap_web_web

    gap_web_mob = []
    for web_day in web_day_int:
        for mob_day in mob_day_int:
            if mob_day > web_day:                
                gap_web_mob.append(mob_day - web_day)
                break
    three_gaps["gap_web_mob"] = gap_web_mob
    return three_gaps

mob_seq = ["01", "03", "12", "22"]
web_seq = ["03", "06", "21"]
print(obtain_three_gaps(mob_seq, web_seq))

#------------------------------------------------------------------------------
# # 2.2 Compute gap distributions
#------------------------------------------------------------------------------

mob_seq = ["01", "12", "03", "22"]
web_seq = ["03", "06", "21"]
print(obtain_three_gaps(mob_seq, web_seq))

time1 = time.time()
all_gap_mob_mob = list()
all_gap_web_mob = list()
all_gap_web_web = list()

count = 0
for user in all_mob_seq:
    count += 1
    if count % 10000 == 0:
        print("count", count)
        time2 = time.time()
        print("time until now", time2-time1)
    
    if user in all_web_seq:
        for poi_type in all_mob_seq[user]:
            if poi_type in all_web_seq[user]:
                mob_seq = all_mob_seq[user][poi_type]
                web_seq = all_web_seq[user][poi_type]
                res = obtain_three_gaps(mob_seq, web_seq)
                all_gap_mob_mob += res["gap_mob_mob"]
                all_gap_web_mob += res["gap_web_mob"]
                all_gap_web_web += res["gap_web_web"]

print(len(all_gap_mob_mob))
print(len(all_gap_web_mob))
print(len(all_gap_web_web))

#------------------------------------------------------------------------------
# # Search to Go
#------------------------------------------------------------------------------

plt.figure(figsize=(3,2.5),dpi=300)

data = [all_gap_web_mob[i]*1.0 for i in range(len(all_gap_web_mob))]

plt.hist(data, bins=13, range=[1, 14], edgecolor='black', align='left', linewidth=0.6, 
         density=True, color=(230/255, 51/255, 13/255))

plt.xlabel("Gap (day)")
plt.ylabel("Probability")

plt.xticks([2*i+1 for i in range(7)],[str(2*i+1) for i in range(7)])
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],["0", "0.2", "0.4", "0.6", "0.8", "1.0"])

plt.title("From intention to action")
plt.savefig('from_intention_to_action_tokyo.svg',bbox_inches = 'tight')
plt.show()

#------------------------------------------------------------------------------
# # Go to Go
#------------------------------------------------------------------------------

plt.figure(figsize=(3,2.5),dpi=300)
data = random.sample(all_gap_mob_mob, 1000*1000)

plt.hist(data, bins=13, range=[1, 14], edgecolor='black', align='left', linewidth=0.6, 
         density=True,  color=(40.0/255, 180.0/255, 230.0/255))

plt.xlabel("Gap (day)")
plt.ylabel("Probability")

plt.xticks([2*i+1 for i in range(7)],[str(2*i+1) for i in range(7)])
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],["0", "0.2", "0.4", "0.6", "0.8", "1.0"])

plt.title("From action to action")
plt.savefig('from_action_to_action_tokyo.svg',bbox_inches = 'tight')
plt.show()

#------------------------------------------------------------------------------
# # Search to Search
#------------------------------------------------------------------------------

plt.figure(figsize=(3,2.5),dpi=300)
data = all_gap_web_web

plt.hist(data, bins=13, range=[1, 14], edgecolor='black', align='left', linewidth=0.6, 
         density=True, color=(230/255, 149/255, 34/255))

plt.xlabel("Gap (day)")
plt.ylabel("Probability")
plt.xticks([2*i+1 for i in range(7)],[str(2*i+1) for i in range(7)])
plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0],["0", "0.2", "0.4", "0.6", "0.8", "1.0"])

plt.title("From intention to intention")
plt.savefig('from_intention_to_intention_tokyo.svg',bbox_inches = 'tight')
plt.show()
