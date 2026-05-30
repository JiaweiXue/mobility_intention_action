import os
import time
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt

#------------------------------------------------------------------------------
# # 1. read data
#------------------------------------------------------------------------------

n_user_dict = {"fuk":314408, "kum":89182, "kag":47594}
n_poi_dict = {"fuk":3, "kum":269, "kag":250}
n_texttype_dict = {"fuk":9, "kum":15, "kag":16}

folder = "/home/umni2/a/umnilab/users/xue120/umni4/2023_YJ_MI_MA/"
root_path = folder + "0_data/"
mob_path = root_path + "mob/"
text_type_path = root_path + "text_type/"
loc_name_list = ["fukuoka", "kagoshima_2", "kumamoto_2"]

#input: loc: "fukuoka", "kagoshima_2", "kumamoto_2"
#output: {'20220902': {'0': {'0':{'2': {'45577': 1}}}}}
#date: "20220902"; 
#hour: "0", ..., "23";
#min: "0", ..., "3";
#loc: "0", ..., "n-1";
#user: "45777"
def read_mob(loc):
    dict_mob = dict()
    all_files = os.listdir(mob_path + loc + "/")
    print ("# files: ", len(all_files))
    for files in all_files:
        if len(files) > 18:
            file_path = mob_path + loc + "/" + files
            with open(file_path, 'r') as f:
                df = json.load(f)
            date = files.split("_")[0]
            dict_mob[date] = df
    return dict_mob

#input: loc: "fukuoka", "kagoshima_2", "kumamoto_2"
#outpot: {'20220902': {'0': {'0':{'2': {'45577': 1}}}}}
#date: "20220902"; 
#hour: "0", ..., "23";
#min: "0", ..., "3";
#loc: "0", ..., "n-1";
#user: "45777"
def read_texttype(loc):
    dict_texttype = dict()
    all_files = os.listdir(text_type_path + loc + "/")
    print ("# files: ", len(all_files))
    for files in all_files:
        if files[0:2] == "20":
            file_path = text_type_path + loc + "/" + files
            with open(file_path, 'r') as f:
                df = json.load(f)
            date = files.split("_")[0]
            dict_texttype[date] = df
    return dict_texttype

mob_fuk = read_mob("fukuoka")
mob_kum_2 = read_mob("kumamoto_2")
mob_kag_2 = read_mob("kagoshima_2")

texttype_fuk = read_texttype("fukuoka")
texttype_kum_2 = read_texttype("kumamoto_2")
texttype_kag_2 = read_texttype("kagoshima_2")

#------------------------------------------------------------------------------
# # 2. prepare graphs
#------------------------------------------------------------------------------

#count the number of edges in the graph
#input: {'20220902': {'0': {'0':{'123': {'4567': 2}}}}}
#output 1: loc_dict = {"123": 2}
#output 2: user_dict = {"4567": 2}
#output 3: loc_list = ["123"]
#output 4: user_list = ["4567"]
#card: {'20220902': {'123': {'4567': 1}}}  without repeat
def get_n_user_poi_without_repeat(d):  #d: dict_mob; dict_texttype
    loc_dict = {str(i):0 for i in range(270)}
    user_dict = {str(j):0 for j in range(320000)}
    loc_list, user_list = list(), list()
    card = dict()
    
    for day in d:
        loc_dict_day = {str(i):{} for i in range(270)}
        user_dict_day = {str(j):{} for j in range(320000)}
        for hour in d[day]:
            for interval in d[day][hour]:
                for loc in d[day][hour][interval]:
                    for user in d[day][hour][interval][loc]:
                        loc_dict_day[loc][user] = 1
                        user_dict_day[user][loc] = 1
          
        card[day] = user_dict_day   #{"20220902": {"123":{"4567":1}}}
        
        for loc in loc_dict_day:
            loc_dict[loc] += len(loc_dict_day[loc])
        for user in user_dict_day:
            user_dict[user] += len(user_dict_day[user])   
                
    for loc in loc_dict:
        if loc_dict[loc] > 0:
            loc_list.append(loc)
            
    for user in user_dict:
        if user_dict[user] > 0:
            user_list.append(user)
            
    return loc_dict, user_dict, loc_list, user_list, card

print ("Fukuoka")
m_loc_dict_fuk, m_user_dict_fuk, m_loc_list_fuk, m_user_list_fuk, m_fuk_card = get_n_user_poi_without_repeat(mob_fuk)
print(len(m_user_list_fuk), len(m_loc_list_fuk))
print ("total edge: ", np.sum(list(m_loc_dict_fuk.values())))
print ("total edge: ", np.sum(list(m_user_dict_fuk.values())))

print("-------------------------------")
print ("Kumamoto")
m_loc_dict_kum_2, m_user_dict_kum_2, m_loc_list_kum_2, m_user_list_kum_2, m_kum_2_card = get_n_user_poi_without_repeat(mob_kum_2)
print(len(m_user_list_kum_2), len(m_loc_list_kum_2))
print ("total edge: ", np.sum(list(m_loc_dict_kum_2.values())))
print ("total edge: ", np.sum(list(m_user_dict_kum_2.values())))

print("-------------------------------")
print ("Kagoshima")
m_loc_dict_kag_2, m_user_dict_kag_2, m_loc_list_kag_2, m_user_list_kag_2, m_kag_2_card = get_n_user_poi_without_repeat(mob_kag_2)
print(len(m_user_list_kag_2), len(m_loc_list_kag_2))
print ("total edge: ", np.sum(list(m_loc_dict_kag_2.values())))
print ("total edge: ", np.sum(list(m_user_dict_kag_2.values())))

print ("Fukuoka")
t_loc_dict_fuk, t_user_dict_fuk, t_loc_list_fuk, t_user_list_fuk, t_fuk_card = get_n_user_poi_without_repeat(texttype_fuk)
print(len(t_user_list_fuk), len(t_loc_list_fuk))
print ("total edge: ", np.sum(list(t_loc_dict_fuk.values())))
print ("total edge: ", np.sum(list(t_user_dict_fuk.values())))

print("-------------------------------")
print ("Kumamoto")
t_loc_dict_kum_2, t_user_dict_kum_2, t_loc_list_kum_2, t_user_list_kum_2, t_kum_2_card = get_n_user_poi_without_repeat(texttype_kum_2)
print(len(t_user_list_kum_2), len(t_loc_list_kum_2))
print ("total edge: ", np.sum(list(t_loc_dict_kum_2.values())))
print ("total edge: ", np.sum(list(t_user_dict_kum_2.values())))
       
print("-------------------------------")
print ("Kagoshima")
t_loc_dict_kag_2, t_user_dict_kag_2, t_loc_list_kag_2, t_user_list_kag_2, t_kag_2_card = get_n_user_poi_without_repeat(texttype_kag_2)
print(len(t_user_list_kag_2), len(t_loc_list_kag_2))
print ("total edge: ", np.sum(list(t_loc_dict_kag_2.values())))
print ("total edge: ", np.sum(list(t_user_dict_kag_2.values())))

#------------------------------------------------------------------------------
# # 3. compute conditional probability for Fukuoka
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# # 3.1. generate date pairs
#------------------------------------------------------------------------------

#[[['20230603', '20230604', '20230605'], '20230606']]
#T to 1. 
def generate_t_1_pair(date_list, t):
    generated_pair = list()
    n = len(date_list)
    for i in range(n-t):
        generated_pair.append([[date_list[i+j] for j in range(t)], date_list[i+t]])
    return generated_pair

date_fuk_list = list(mob_fuk.keys())
date_fuk_list.sort()
print (len(date_fuk_list))
generated_item_fuk = generate_t_1_pair(date_fuk_list, 4)
print (generated_item_fuk[-1])

#------------------------------------------------------------------------------
# # 3.2. specify the mapping from search terms to mobility POIs
#------------------------------------------------------------------------------

fuk_mapping = {"0": ["0","1","2"], "1": ["0"], "2": ["2"],\
               "3": ["0"], "4": ["1"], "5": ["2"],\
               "6": ["0"], "7": ["0"], "8": ["1"]}

#------------------------------------------------------------------------------
# # 3.3. compute values
#------------------------------------------------------------------------------

#input: "fuk", generated_item, m_fuk_card, t_fuk_card, fuk_mapping 
#output: n_search_go_all
def generate_n_search_go(city, generated_item, m_card, t_card, city_mapping):
    #extract the count of search & go
    #input: card {'20220902': {'123': {'4567': 1}}}  without repeat
    #output: [1,1,...,1], [100,100,...,100], [2,2,...,2], [200,200,...,200]

    n_search_go_all = [[], [], [], []] #(search, go), (search, notgo), (notsearch, go), (notsearch, notgo)
    n_user = n_user_dict[city]
    n_poi = n_texttype_dict[city]
    n_day = len(generated_item)

    for i in range(n_day):
        if i%5==0:
            print ("i", i)
        text_x = {str(k):{} for k in range(n_user)}
        for j in range(4):
            d = generated_item[i][0][j]   #'20230603'
            t_one_day = t_card[d]     #[user][loc] = 1
            for user in t_one_day:
                if len(t_one_day[user]) >= 1:
                    for poi in t_one_day[user]:
                        for p_poi in city_mapping[poi]:
                            text_x[user][p_poi] = 1

        mob_y = {str(k):{} for k in range(n_user)}
        d = generated_item[i][1]        #'20230606'
        m_one_day = m_card[d]       #[user][loc] = 1
        for user in m_one_day:    
            if len(m_one_day[user]) >= 1:
                for p_poi in m_one_day[user]:
                    mob_y[user][p_poi] = 1

        n_search_go, n_search_notgo, n_notsearch_go, n_notsearch_notgo = 0, 0, 0, 0
        for user in range(n_user):
            str_user = str(user)
            for poi in range(n_poi):
                str_poi = str(poi)
                a = str_poi in text_x[str_user]
                b = str_poi in mob_y[str_user]
                if a == True and b == True:
                    n_search_go += 1
                if a == True and b == False:
                    n_search_notgo += 1
                if a == False and b == True:
                    n_notsearch_go += 1 
                if a == False and b == False:
                    n_notsearch_notgo += 1        
        n_search_go_all[0].append(n_search_go)  
        n_search_go_all[1].append(n_search_notgo)  
        n_search_go_all[2].append(n_notsearch_go)  
        n_search_go_all[3].append(n_notsearch_notgo)
    return n_search_go_all

n_search_go_all_fuk = generate_n_search_go("fuk", generated_item_fuk, m_fuk_card, t_fuk_card, fuk_mapping)

print ("search&Go", np.mean(n_search_go_all_fuk[0]))
print ("search&NotGo", np.mean(n_search_go_all_fuk[1]))
print ("NotSearch&Go", np.mean(n_search_go_all_fuk[2]))
print ("NotSearch&NotGo", np.mean(n_search_go_all_fuk[3]))
print (np.sum([np.mean(n_search_go_all_fuk[i]) for i in range(4)]))
print (314408*9)

def generate_condition_probability(n_search_go_all):
    p_search_then_go = list()
    p_notsearch_then_go = list()
    for i in range(len(n_search_go_all[0])):
        n0, n1, n2, n3 = n_search_go_all[0][i], n_search_go_all[1][i], n_search_go_all[2][i], n_search_go_all[3][i]
        p_search_then_go.append((n0+1)/(n0+n1+1))
        p_notsearch_then_go.append((n2+1)/(n2+n3+1))
    return p_search_then_go, p_notsearch_then_go

p_search_then_go_fuk, p_notsearch_then_go_fuk = generate_condition_probability(n_search_go_all_fuk)

def save_count(n_search_go_all_city, file_name):
    dict_to_save = {"search_go": n_search_go_all_city[0], "search_notgo": n_search_go_all_city[1],\
                    "notsearch_go": n_search_go_all_city[2], "notsearch_notgo": n_search_go_all_city[3]}
    with open(file_name, 'w') as json_file:
        json.dump(dict_to_save, json_file)

city_name = "fukuoka"
save_count(n_search_go_all_fuk, "count_save/" + city_name + ".json")

#------------------------------------------------------------------------------
# # 3.4. draw values
#------------------------------------------------------------------------------

fig= plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(2, 1, 1)
x = range(len(p_search_then_go_fuk))
plt.plot(x, p_search_then_go_fuk, linewidth=1, label="P(Go|Search)", color="orangered")
plt.plot(x, p_notsearch_then_go_fuk, linewidth=1, label="P(Go|NotSearch)", color="deepskyblue")

plt.title('Sports, Fukuoka, 2023', fontsize=12)

plt.xticks(fontsize=12)
plt.xlabel('Day', fontsize=12)

#ax.set_yscale('log')
my_y_ticks = [0, 0.015, 0.03]
plt.yticks(my_y_ticks, fontsize=12)
plt.ylim(bottom=0)
plt.ylabel('Probability', fontsize=12)

plt.legend(loc=2, fontsize=7)
plt.savefig("con_prob_save/" + "fuk.svg", bbox_inches = 'tight')

print (np.mean(p_search_then_go_fuk))
print (np.mean(p_notsearch_then_go_fuk))
print ("ratio = ", np.mean(p_search_then_go_fuk)/np.mean(p_notsearch_then_go_fuk))

#------------------------------------------------------------------------------
# # 4. compute conditional probability for Kumamoto
#------------------------------------------------------------------------------

date_kum_2_list = list(mob_kum_2.keys())
date_kum_2_list.sort()
print (len(date_kum_2_list))
generated_item_kum_2 = generate_t_1_pair(date_kum_2_list, 4)
print (generated_item_kum_2[-1])

kum_type = pd.read_csv(folder + "result_1/poi/kum_type.csv", header=None)
shelter_kum = pd.read_csv(folder + "result_1/poi/shelter_kuma_new.csv")
shelter_kum_type = list(shelter_kum["type"])
n_shelter_kum = len(shelter_kum)
english_kum_to_number = {"Elementary School":1,\
                         "High School":2,\
                         "Junior High School":3,\
                         "Park":4,\
                         "Center":5,\
                         "Gymnasium":6,\
                         "University":7,\
                         "Bridge":8,\
                         "Hall":9,\
                         "Stadium":10,\
                         "Field":11,\
                         "Plaza":12,\
                         "Plant":13,\
                         "Facility":14}
#kum_mapping = {"0":["0","1",...,"268"], "1":...}
kum_mapping = {}
kum_mapping["0"] = [str(i) for i in range(n_shelter_kum)]
for i in range(14):
    kum_mapping[str(i+1)] = []
for i in range(len(shelter_kum_type)):
    loc_type = shelter_kum_type[i]
    index = english_kum_to_number[loc_type]
    kum_mapping[str(index)].append(str(i))
print (len(kum_mapping))

n_search_go_all_kum_2 = generate_n_search_go("kum", generated_item_kum_2,\
                                             m_kum_2_card, t_kum_2_card, kum_mapping)

p_search_then_go_kum_2, p_notsearch_then_go_kum_2 =\
generate_condition_probability(n_search_go_all_kum_2)

fig= plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(2, 1, 1)
x = range(len(p_search_then_go_kum_2))
plt.plot(x, p_search_then_go_kum_2, linewidth=1, label="P(Go|Search)", color="orangered")
plt.plot(x, p_notsearch_then_go_kum_2, linewidth=1, label="P(Go|NotSearch)", color="deepskyblue")

plt.title('Typhoon, Kumamoto, 2022', fontsize=12)

plt.xticks(fontsize=12)
plt.xlabel('Day', fontsize=12)

my_y_ticks = [0, 0.0005, 0.001]
plt.ylim(bottom=0)
plt.yticks(my_y_ticks, fontsize=12)
plt.ylabel('Probability', fontsize=12)

plt.savefig("con_prob_save/" + "kum.svg", bbox_inches = 'tight')
plt.show()

print (np.mean(p_search_then_go_kum_2))
print (np.mean(p_notsearch_then_go_kum_2))
print ("ratio = ", np.mean(p_search_then_go_kum_2)/np.mean(p_notsearch_then_go_kum_2))

stats.ttest_ind(p_search_then_go_kum_2, p_notsearch_then_go_kum_2, alternative="greater")

city_name = "kumamoto_2"
save_count(n_search_go_all_kum_2, "count_save/" + city_name + ".json")

#------------------------------------------------------------------------------
# # 5. compute conditional probability for Kagoshima
#------------------------------------------------------------------------------

#5.1 date
date_kag_2_list = list(mob_kag_2.keys())
date_kag_2_list.sort()
print (len(date_kag_2_list))
generated_item_kag_2 = generate_t_1_pair(date_kag_2_list, 4)
print (generated_item_kag_2[-1])

#5.2 mapping
kag_type = pd.read_csv(folder + "result_1/poi/" + "kag_type.csv", header=None)
shelter_kag = pd.read_csv(folder + "result_1/poi/" + "shelter_kago_new.csv")
n_shelter_kag = len(shelter_kag)
print (n_shelter_kag)
shelter_kag_type = list(shelter_kag["type"])
english_kag_to_number = {"Elementary School":1,\
                         "Junior High School":2,\
                         "High School":3,\
                         "Hall":4,\
                         "House":5,\
                         "Center":6,\
                         "Gymnasium":7,\
                         "Building":8,\
                         "School":9,\
                         "University":10,\
                         "College":11,\
                         "Park":12,\
                         "Shelter":13,\
                         "Ferry":14,\
                         "Facility":15}
kag_mapping = {}
kag_mapping["0"] = [str(i) for i in range(n_shelter_kag)]
for i in range(15):
    kag_mapping[str(i+1)] = []
for i in range(len(shelter_kag_type)):
    loc_type = shelter_kag_type[i]
    index = english_kag_to_number[loc_type]
    if index>=1:
        kag_mapping[str(index)].append(str(i))

#5.3 compute values
n_search_go_all_kag_2 = generate_n_search_go("kag", generated_item_kag_2,\
                                             m_kag_2_card, t_kag_2_card, kag_mapping)

p_search_then_go_kag_2, p_notsearch_then_go_kag_2 =\
generate_condition_probability(n_search_go_all_kag_2)

fig= plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(2, 1, 1)
x = range(len(p_search_then_go_kag_2))
plt.plot(x, p_search_then_go_kag_2, linewidth=1, label="P(Go|Search)", color="orangered")
plt.plot(x, p_notsearch_then_go_kag_2, linewidth=1, label="P(Go|NotSearch)", color="deepskyblue")

plt.title('Typhoon, Kagoshima, 2022', fontsize=12)

plt.xticks(fontsize=12)
plt.xlabel('Day', fontsize=12)

#ax.set_yscale('log')
my_y_ticks = [0, 0.0015, 0.003]
plt.yticks(my_y_ticks, fontsize=12)
plt.ylim(bottom=0)
plt.ylabel('Probability', fontsize=12)

#plt.legend(loc=2, fontsize=6)
plt.savefig("con_prob_save/" + "kag_2.svg", bbox_inches = 'tight')
plt.show()

print (np.mean(p_search_then_go_kag_2))
print (np.mean(p_notsearch_then_go_kag_2))
print ("ratio = ", np.mean(p_search_then_go_kag_2)/np.mean(p_notsearch_then_go_kag_2))

city_name = "kagoshima_2"
save_count(n_search_go_all_kag_2, "count_save/" + city_name + ".json")

#------------------------------------------------------------------------------
# # 6. Ratio and test
#------------------------------------------------------------------------------

ratio_fuk = np.mean(p_search_then_go_fuk)/np.mean(p_notsearch_then_go_fuk)
ratio_kum_2 = np.mean(p_search_then_go_kum_2)/np.mean(p_notsearch_then_go_kum_2)
ratio_kag_2 = np.mean(p_search_then_go_kag_2)/np.mean(p_notsearch_then_go_kag_2)
print ("fuk", ratio_fuk)
print ("kum_2", ratio_kum_2)
print ("kag_2", ratio_kag_2)

print (stats.ttest_ind(p_search_then_go_fuk, p_notsearch_then_go_fuk, alternative="greater"))
print (stats.ttest_ind(p_search_then_go_kum_2, p_notsearch_then_go_kum_2, alternative="greater"))
print (stats.ttest_ind(p_search_then_go_kag_2, p_notsearch_then_go_kag_2, alternative="greater"))
