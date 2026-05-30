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

folder = "2023_YJ_MI_MA/result_5_temporal_model_figure_5/kyoto/20260411/"

mob_file = folder + "all_mob_seq/until_20230930.json"
web_file = folder + "all_web_seq/until_20230930.json"

with open(mob_file, 'r') as file:
    all_mob_seq = json.load(file)

with open(web_file, 'r') as file:
    all_web_seq = json.load(file)

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
#plt.savefig('from_intention_to_action_kyoto.svg',bbox_inches = 'tight')
plt.show()

print(len(data))
print(data.count(1)/len(data))
print(data.count(2)/len(data))
print(data.count(3)/len(data))

num_ones = sum(1 for x in data if x == 1 or x == 2 or x == 3)
print(num_ones/len(data))

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
plt.savefig('from_action_to_action_kyoto.svg',bbox_inches = 'tight')
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
plt.savefig('from_intention_to_intention_kyoto.svg',bbox_inches = 'tight')
plt.show()
