import json
import numpy as np
import pandas as pd
import random
import math
from math import sin, cos, sqrt, atan2, radians

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from scipy import stats
from scipy.stats import ttest_ind

folder = "2023_YJ_MI_MA/"
user_type_1 = folder + "result_7_returner_explorer/kyoto/return_explorer/return_explorer_129789.json"

user_go_search = folder + "result_7_returner_explorer/kyoto/res_sg/user_sg_sng_nsg_nsng_dict_13w_270days_"

#------------------------------------------------------------------------------
# # 1. Read data
#------------------------------------------------------------------------------

df_user_type = {}
with open(user_type_1, 'r') as f:
    df_user_type_1 = json.load(f)
    for user in df_user_type_1:
        df_user_type[user] = df_user_type_1[user]

print(len(df_user_type))

df_user_go_search_all = {user: [0, 0, 0, 0] for user in df_user_type}

for i in range(269):
    print("i", i)
    with open(user_go_search + str(i) + ".json", 'r') as f:
        df_user_go_search = json.load(f)
        for user in df_user_go_search:
            if user in df_user_go_search_all:
                df_user_go_search_all[user][0] += df_user_go_search[user][0] 
                df_user_go_search_all[user][1] += df_user_go_search[user][1] 
                df_user_go_search_all[user][2] += df_user_go_search[user][2] 
                df_user_go_search_all[user][3] += df_user_go_search[user][3] 


    print(len(df_user_go_search_all))
    print(np.sum([df_user_go_search_all[user][0] for user in df_user_go_search]))
    print(np.sum([df_user_go_search_all[user][1] for user in df_user_go_search]))
    print(np.sum([df_user_go_search_all[user][2] for user in df_user_go_search]))
    print(np.sum([df_user_go_search_all[user][3] for user in df_user_go_search]))
#sg_sng_nsg_nsng

#------------------------------------------------------------------------------
# # 2. Obtain values
#------------------------------------------------------------------------------

x_rg2_in_rg = []
x_rg4_in_rg = []
x_rg8_in_rg = []
y_p_go_search = []
for user in df_user_type:
    if user in df_user_go_search_all:
        rg2, rg4, rg8, rg = df_user_type[user]["rg_2"], df_user_type[user]["rg_4"], df_user_type[user]["rg_8"], df_user_type[user]["rg"]
        rg2_in_rg = rg2 /(rg + 1e-9)
        rg4_in_rg = rg4 /(rg + 1e-9)
        rg8_in_rg = rg8 /(rg + 1e-9)
        x_rg2_in_rg.append(rg2_in_rg)
        x_rg4_in_rg.append(rg4_in_rg)
        x_rg8_in_rg.append(rg8_in_rg)

        sg, sng, nsg, nsng =\
              df_user_go_search_all[user][0],\
                  df_user_go_search_all[user][1],\
                      df_user_go_search_all[user][2],\
                          df_user_go_search_all[user][3]
        if sg + sng <= 0:
            y_p_go_search.append(0.0)
        else:
            y_p_go_search.append((sg)/(sg + sng))

print(np.mean(x_rg2_in_rg))
print(np.max(x_rg2_in_rg))
print(np.min(x_rg2_in_rg))
print("--------------------------------")
print(np.mean(x_rg4_in_rg))
print(np.max(x_rg4_in_rg))
print(np.min(x_rg4_in_rg))
print("--------------------------------")
print(np.mean(x_rg8_in_rg))
print(np.max(x_rg8_in_rg))
print(np.min(x_rg8_in_rg))
print("--------------------------------")
print(np.mean(y_p_go_search))
print(np.max(y_p_go_search))
print(np.min(y_p_go_search))

#------------------------------------------------------------------------------
# # rg2
#------------------------------------------------------------------------------

y_exp_2 = []
y_ret_2 = []
for i in range(len(x_rg2_in_rg)):
    if x_rg2_in_rg[i] > 0.05:
        y_ret_2.append(y_p_go_search[i])
    else:
        y_exp_2.append(y_p_go_search[i])

print(np.mean(y_exp_2))
print(len(y_exp_2))

print(np.mean(y_ret_2))
print(len(y_ret_2))

# Two-sided t-test
t_stat_2, p_value_two_sided_2 = ttest_ind(y_exp_2, y_ret_2, equal_var=False)

# One-sided test: test if mean(array1) > mean(array2)
p_value_one_sided_2 = p_value_two_sided_2 / 2 if t_stat_2 > 0 else 1 - (p_value_two_sided_2 / 2)

print(f"T-statistic: {t_stat_2}")
print(f"One-sided p-value: {p_value_one_sided_2}")

stats.ttest_ind(y_exp_2, y_ret_2, equal_var=False)

print(len(x_rg2_in_rg))
print(len(y_p_go_search))
sampled_x_2 = []
sampled_y_2 = []

for i in range(len(x_rg2_in_rg)):
    if random.random()<1.0:
        sampled_x_2.append((x_rg2_in_rg[i]))
        sampled_y_2.append((y_p_go_search[i]))
sampled_x_2 = np.array(sampled_x_2)
sampled_y_2 = np.array(sampled_y_2)

plt.rcParams['font.sans-serif'] = ['Arial'] 
plt.rcParams['axes.unicode_minus'] = False 

ft = 11
plt.figure(figsize=(3,2.5),dpi=300)
l1 = plt.scatter(sampled_x_2, sampled_y_2, linestyle='-', color="red", marker="o", linewidth=0.1, s=3.0, label='X')

my_x_ticks = [0, 2, 4, 6]
plt.xticks(fontsize=ft)
plt.xlabel('$r_{g}(2)$/$r_{g}$',fontsize=ft)
plt.xlim(0, 3)
plt.xticks([0, 1, 2, 3], ['0', '1', '2', '3'])

my_y_ticks = [0, 0.01, 0.02, 0.03]
plt.yticks(fontsize=ft)
plt.ylabel('$P(Go|Search)$',fontsize=ft)
plt.ylim(0, 0.024)
plt.yticks([0, 0.008, 0.016, 0.024], ['0', '0.008', '0.016', '0.024'])

plt.axvline(x=0.52,color='black', ymin = 0, ymax = 1, linestyle='--', linewidth=1.5)
plt.text(0.38, -0.00180, '0.5', fontsize=10, color="black")
plt.text(0.65, 0.02108, 'Explorer', fontsize=ft, color="black")
plt.text(1.4, 0.014, 'Returner', fontsize=ft, color="black")

plt.title("Kyoto", fontsize=ft)
plt.savefig('20260314_kyoto_p_go_search_2.svg',bbox_inches = 'tight')
plt.savefig('20260314_kyoto_p_go_search_2.png',bbox_inches = 'tight')
#plt.savefig('connection.svg',bbox_inches = 'tight')

plt.show()

#------------------------------------------------------------------------------
# # rg4
#------------------------------------------------------------------------------

y_exp_4 = []
y_ret_4 = []
for i in range(len(x_rg4_in_rg)):
    if x_rg4_in_rg[i] > 0.05:
        y_ret_4.append(y_p_go_search[i])
    else:
        y_exp_4.append(y_p_go_search[i])

print(np.mean(y_exp_4))
print(len(y_exp_4))

print(np.mean(y_ret_4))
print(len(y_ret_4))

# Two-sided t-test
t_stat_4, p_value_two_sided_4 = ttest_ind(y_exp_4, y_ret_4, equal_var=False)

# One-sided test: test if mean(array1) > mean(array2)
p_value_one_sided_4 = p_value_two_sided_4 / 2 if t_stat_4 > 0 else 1 - (p_value_two_sided_4 / 2)

print(f"T-statistic: {t_stat_4}")
print(f"One-sided p-value: {p_value_one_sided_4}")

stats.ttest_ind(y_exp_4, y_ret_4, equal_var=False)

print(len(x_rg4_in_rg))
print(len(y_p_go_search))
sampled_x_4 = []
sampled_y_4 = []

for i in range(len(x_rg2_in_rg)):
    if random.random()<1.0:
        sampled_x_4.append((x_rg4_in_rg[i]))
        sampled_y_4.append((y_p_go_search[i]))
sampled_x_4 = np.array(sampled_x_4)
sampled_y_4 = np.array(sampled_y_4)

plt.rcParams['font.sans-serif'] = ['Arial'] 
plt.rcParams['axes.unicode_minus'] = False 

ft = 11
plt.figure(figsize=(3,2.5),dpi=300)
l1 = plt.scatter(sampled_x_4, sampled_y_4, linestyle='-', color="red", marker="o", linewidth=0.1, s=3.0, label='X')

my_x_ticks = [0, 2, 4, 6]
plt.xticks(fontsize=ft)
plt.xlabel('$r_{g}(4)$/$r_{g}$',fontsize=ft)
plt.xlim(0, 3)
plt.xticks([0, 1, 2, 3], ['0', '1', '2', '3'])

my_y_ticks = [0, 0.01, 0.02, 0.03]
plt.yticks(fontsize=ft)
plt.ylabel('$P(Go|Search)$',fontsize=ft)
plt.ylim(0, 0.024)
plt.yticks([0, 0.008, 0.016, 0.024], ['0', '0.008', '0.016', '0.024'])

plt.axvline(x=0.52,color='black', ymin = 0, ymax = 1, linestyle='--', linewidth=1.5)

plt.text(0.38, -0.00180, '0.5', fontsize=10, color="black")
plt.text(0.65, 0.02108, 'Explorer', fontsize=ft, color="black")
plt.text(1.4, 0.014, 'Returner', fontsize=ft, color="black")

plt.title("Kyoto", fontsize=ft)
plt.savefig('20260314_kyoto_p_go_search_4.svg',bbox_inches = 'tight')
plt.savefig('20260314_kyoto_p_go_search_4.png',bbox_inches = 'tight')
#plt.savefig('connection.svg',bbox_inches = 'tight')

plt.show()

#------------------------------------------------------------------------------
# # rg8
#------------------------------------------------------------------------------

y_exp_8 = []
y_ret_8 = []
for i in range(len(x_rg8_in_rg)):
    if x_rg8_in_rg[i] > 0.05:
        y_ret_8.append(y_p_go_search[i])
    else:
        y_exp_8.append(y_p_go_search[i])

print(np.mean(y_exp_8))
print(len(y_exp_8))

print(np.mean(y_ret_8))
print(len(y_ret_8))

# Two-sided t-test
t_stat_8, p_value_two_sided_8 = ttest_ind(y_exp_8, y_ret_8, equal_var=False)

# One-sided test: test if mean(array1) > mean(array2)
p_value_one_sided_8 = p_value_two_sided_8 / 2 if t_stat_8 > 0 else 1 - (p_value_two_sided_8 / 2)

print(f"T-statistic: {t_stat_8}")
print(f"One-sided p-value: {p_value_one_sided_8}")

print(len(x_rg8_in_rg))
print(len(y_p_go_search))
sampled_x_8 = []
sampled_y_8 = []

for i in range(len(x_rg8_in_rg)):
    if random.random()<1.0:
        sampled_x_8.append((x_rg8_in_rg[i]))
        sampled_y_8.append((y_p_go_search[i]))
sampled_x_8 = np.array(sampled_x_8)
sampled_y_8 = np.array(sampled_y_8)

plt.rcParams['font.sans-serif'] = ['Arial'] 
plt.rcParams['axes.unicode_minus'] = False 

ft = 11
plt.figure(figsize=(3,2.5),dpi=300)
l1 = plt.scatter(sampled_x_8, sampled_y_8, linestyle='-', color="red", marker="o", linewidth=0.1, s=3.0, label='X')

my_x_ticks = [0, 2, 4, 6]
plt.xticks(fontsize=ft)
plt.xlabel('$r_{g}(8)$/$r_{g}$',fontsize=ft)
plt.xlim(0, 3)
plt.xticks([0, 1, 2, 3], ['0', '1', '2', '3'])

my_y_ticks = [0, 0.01, 0.02, 0.03]
plt.yticks(fontsize=ft)
plt.ylabel('$P(Go|Search)$',fontsize=ft)
plt.ylim(0, 0.024)
plt.yticks([0, 0.008, 0.016, 0.024], ['0', '0.008', '0.016', '0.024'])

plt.axvline(x=0.52,color='black', ymin = 0, ymax = 1, linestyle='--', linewidth=1.5)
plt.text(0.38, -0.00180, '0.5', fontsize=10, color="black")
plt.text(0.65, 0.02108, 'Explorer', fontsize=ft, color="black")
plt.text(1.4, 0.014, 'Returner', fontsize=ft, color="black")

plt.title("Kyoto", fontsize=ft)
plt.savefig('20260314_kyoto_p_go_search_8.svg',bbox_inches = 'tight')
plt.savefig('20260314_kyoto_p_go_search_8.png',bbox_inches = 'tight')
#plt.savefig('connection.svg',bbox_inches = 'tight')

plt.show()
