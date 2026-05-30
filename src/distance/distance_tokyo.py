import os
import json
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from sklearn.linear_model import LinearRegression

key_to_type1_dict = {"0": "amenity", "1": "building", "2": "emergency", "3": "leisure",\
                     "4": "public_transport", "5": "shop", "6": "sport", "7": "tourism"}

#------------------------------------------------------------------------------
# # step 1: read files
#------------------------------------------------------------------------------

file_path = "2023_YJ_MI_MA/result_4_1_model_figure_4/tokyo/"

day_type_distance = file_path + "day_type_distance_sg" + "/"
all_files = os.listdir(day_type_distance)
print(all_files)
print(len(all_files))

all_files.sort()
print(all_files)

count = 0
for file_name in all_files:
    if file_name[-4:] == "json":
        f_path = file_path + "day_type_distance_sg/" + file_name
        with open(f_path, 'r') as f:
            df = json.load(f)
            #print(len(df))
            count += 1
print (count)

#------------------------------------------------------------------------------
# # step 2: plot the figures
#------------------------------------------------------------------------------

#idx = "0", "1", ..., "7"
def get_conditional_probability(idx_list):
    max_distance = 40
    x, p_go_search = [i for i in range(max_distance)], [0.0 for i in range(max_distance)]
    numerator, denominator = [0.0 for i in range(max_distance)], [0.0 for i in range(max_distance)] 

    print(len(all_files))
    for file_name in all_files:
        if file_name[-4:] == "json":

            f_path = file_path + "day_type_distance_sg/" + file_name
            with open(f_path, 'r') as f:
                df = json.load(f)
                for i in range(max_distance):
                    for idx in idx_list:
                        numerator[i] += df[idx][i][0]
                        denominator[i] += (0.001+df[idx][i][0]+df[idx][i][1])
                    
    p_go_search = [numerator[i]/denominator[i] for i in range(max_distance)]
    return x, p_go_search

def draw_conditional_probability(x, y):
    ft = 12
    plt.figure(figsize=(3,2),dpi=300)
    l1 = plt.scatter(x, y, color="red", linestyle='-', marker="o", linewidth=0.1, s=4.0, label='X')

    my_x_ticks = [0, 20, 40]
    plt.xticks(my_x_ticks, fontsize=ft)
    plt.xlabel('User-POI distance (km)',fontsize=ft)
    #plt.xlim([0, 42])

    my_y_ticks = np.arange(0.00, 0.016, 0.005)
    plt.yticks([0, 0.005, 0.01], ["0", "0.005", "0.01"], fontsize=ft)
    plt.ylabel('P(Go|Search)', fontsize=ft)
    #plt.ylim([0, 0.01])

    plt.title("Tokyo")
    #plt.legend(loc=1, fontsize=8)
    plt.savefig('p-distance-tokyo-20260504.svg',bbox_inches = 'tight')
    plt.show()

idx_list = [str(i) for i in range(8)]
x, y = get_conditional_probability(idx_list)
draw_conditional_probability(x, y)
