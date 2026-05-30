import os
import json
import numpy as np
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression

key_to_type1_dict = {"0": "amenity", "1": "building", "2": "emergency", "3": "leisure",\
                     "4": "public_transport", "5": "shop", "6": "sport", "7": "tourism"}

#------------------------------------------------------------------------------
# # step 1: read files
#------------------------------------------------------------------------------

day_type_distance = "day_type_distance_sg" + "/"
all_files = os.listdir(day_type_distance)
print(all_files)
print(len(all_files))

all_files.sort()
print(all_files)

count = 0
for file_name in all_files:
    if file_name[-4:] == "json":
        f_path = "day_type_distance_sg/" + file_name
        with open(f_path, 'r') as f:
            df = json.load(f)
            count += 1
print (count)

#------------------------------------------------------------------------------
# # step 2: plot figures
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# # 2.1 plot functions
#------------------------------------------------------------------------------

#idx = "0", "1", ..., "7"
def get_conditional_probability(idx):
    max_distance = 40
    x, p_go_search = [i for i in range(max_distance)], [0.0 for i in range(max_distance)]
    numerator, denominator = [0.0 for i in range(max_distance)], [0.0 for i in range(max_distance)] 

    print(len(all_files))
    for file_name in all_files:
        if file_name[-4:] == "json":

            f_path = "day_type_distance_sg/" + file_name
            with open(f_path, 'r') as f:
                df = json.load(f)
                for i in range(max_distance):
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
    plt.xlabel('Distance (km)',fontsize=ft)

    plt.yticks(fontsize=ft)
    plt.ylabel('P(Go|Search)', fontsize=ft)

    plt.title("Tokyo, Scenario: 4 to 1")
    plt.show()

#------------------------------------------------------------------------------
# # 2.2 data fitting
#------------------------------------------------------------------------------

def generate_points_for_fitting(x, y, y_min=5e-6, y_max=0.01):
    x_for_fit = np.array([np.log(x[i]+1) for i in range(len(x))]).reshape(-1, 1)
    y_for_fit = np.array([np.log(y[i]+0.00000001) for i in range(len(y))])
    x_for_fit_new, y_for_fit_new = [], []

    for i in range(len(x_for_fit)):
        if y_for_fit[i] > np.log(y_min) and y_for_fit[i] < np.log(y_max):
            x_for_fit_new.append(x_for_fit[i][0])
            y_for_fit_new.append(y_for_fit[i])

    x_for_fit_new = np.array(x_for_fit_new).reshape(-1, 1)
    y_for_fit_new = np.array(y_for_fit_new)

    model = LinearRegression()
    model.fit(x_for_fit_new, y_for_fit_new)
    slope = model.coef_[0]
    intercept = model.intercept_
    print("slope:", slope)
    print("intercept:", intercept)
    return slope, intercept

def prepare_x_y_for_fitting_lines(x, slope, intercept):
    len_draw = int(10*np.log(len(x))+2)/10.0
    x_draw_seq = []
    for j in range(1000000):
        if j/10 < len_draw and j/10>0.10:
            x_draw_seq.append(j/10)

    x_draw = [np.exp(x_draw_seq[i]) for i in range(len(x_draw_seq))]
    y_draw = [np.exp(slope*x_draw_seq[i]+intercept) for i in range(len(x_draw_seq))]
    return x_draw, y_draw

def draw_fitting(x, y, x_draw, y_draw, idx, slope):
    ft = 11
    plt.figure(figsize=(3,2.5),dpi=300)
    l1 = plt.loglog(x, y, color="red", linestyle='', marker="o", linewidth=0.4, markersize=2)
    l2 = plt.loglog(x_draw, y_draw, color="black", linestyle='-', linewidth=1, markersize=2)

    my_x_ticks = [1, 10, 100]
    plt.xticks(my_x_ticks, fontsize=ft)
    plt.xlabel('User-POI distance (km)',fontsize=ft)

    plt.ylim(0.00001, 0.02)
    plt.yticks(fontsize=ft)
    plt.ylabel('P(Go|Search)', fontsize=ft)

    plt.title("Tokyo-" + key_to_type1_dict[idx])
    plt.text(15, 0.002, '$r$=' + str(round(slope, 2)), fontsize=12, color='black', ha='center', va='bottom')
    plt.savefig('log-log-figure/20260415/' + idx + '_'  + key_to_type1_dict[idx] + '_' + str(round(slope, 2)) + '.svg',bbox_inches = 'tight')
    plt.show()

#------------------------------------------------------------------------------
# # 1. amenity
#------------------------------------------------------------------------------

idx = "0"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 2. building
#------------------------------------------------------------------------------

idx = "1"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 3. emergency
#------------------------------------------------------------------------------

idx = "2"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 4. leisure
#------------------------------------------------------------------------------

idx = "3"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 5. public transport
#------------------------------------------------------------------------------

idx = "4"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 6. shop
#------------------------------------------------------------------------------

idx = "5"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 7. sport
#------------------------------------------------------------------------------

idx = "6"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)

#------------------------------------------------------------------------------
# # 8. tourism
#------------------------------------------------------------------------------

idx = "7"
x, y = get_conditional_probability(idx)
draw_conditional_probability(x, y)

slope, intercept = generate_points_for_fitting(x, y)
x_draw, y_draw = prepare_x_y_for_fitting_lines(x, slope, intercept)
draw_fitting(x, y, x_draw, y_draw, idx, slope)
