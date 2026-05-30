import os
import time
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------
# # 1. Read files
#------------------------------------------------------------------------------

folder = "/home/umni2/a/umnilab/users/xue120/umni4/2023_YJ_MI_MA/result_1/"
root_path = folder + "2_show_cond_prob_Tokyo/4_1/count_save/"

n_search_go_all = [[], [], [], []]

for index in range(18):
    with open(root_path + "tokyo_half_" + str(index) + ".json", 'r') as file:
        df = json.load(file)

    n_search_go_all[0] = n_search_go_all[0] + df["search_go"]
    n_search_go_all[1] = n_search_go_all[1] + df["search_notgo"]
    n_search_go_all[2] = n_search_go_all[2] + df["notsearch_go"]
    n_search_go_all[3] = n_search_go_all[3] + df["notsearch_notgo"]

#------------------------------------------------------------------------------
# # 2. Plot
#------------------------------------------------------------------------------

def generate_condition_probability(n_search_go_all):
    p_search_then_go = list()
    p_notsearch_then_go = list()
    for i in range(len(n_search_go_all[0])):
        n0, n1, n2, n3 = n_search_go_all[0][i], n_search_go_all[1][i], n_search_go_all[2][i], n_search_go_all[3][i]
        p_search_then_go.append((n0+1)/(n0+n1+1))
        p_notsearch_then_go.append((n2+1)/(n2+n3+1))
    return p_search_then_go, p_notsearch_then_go

p_search_then_go_tok, p_notsearch_then_go_tok = generate_condition_probability(n_search_go_all)

fig= plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(2, 1, 1)
x = range(len(p_search_then_go_tok))
plt.plot(x, p_search_then_go_tok, linewidth=1, label="P(Go|Search)", color="orangered")
plt.plot(x, p_notsearch_then_go_tok, linewidth=1, label="P(Go|NotSearch)", color="deepskyblue")

plt.title('Regular, Tokyo, 2023', fontsize=12)

plt.xticks(fontsize=12)
plt.xlabel('Day', fontsize=12)

#ax.set_yscale('log')
my_y_ticks = [0, 0.002, 0.004]
plt.yticks(my_y_ticks, fontsize=12)
plt.ylim(bottom=0)
#plt.ylabel('Probability', fontsize=12)

#plt.legend(loc=2, fontsize=7)
plt.savefig(folder + "2_show_cond_prob_Tokyo/4_1/con_prob_save/" + "tok.svg",\
            bbox_inches = 'tight')

#------------------------------------------------------------------------------
# # 3. Ratio
#------------------------------------------------------------------------------

print (np.mean(p_search_then_go_tok))
print (np.mean(p_notsearch_then_go_tok))
print ("ratio = ", np.mean(p_search_then_go_tok)/np.mean(p_notsearch_then_go_tok))

#------------------------------------------------------------------------------
# # 4. P-test
#------------------------------------------------------------------------------

print (stats.ttest_ind(p_search_then_go_tok,\
                       p_notsearch_then_go_tok, alternative="greater"))
