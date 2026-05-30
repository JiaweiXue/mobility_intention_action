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

n_user_dict = {"kyo":817400}      ## 129789
n_poi_dict = {"kyo":47532}
n_texttype_dict = {"kyo":8}

folder = "/home/umni2/a/umnilab/users/xue120/umni4/2023_YJ_MI_MA/"
root_path = folder + "0_data/"
mob_path = root_path + "mob/"
text_type_path = root_path + "text_type/"
loc_name_list = ["kyoto"]

df_kyoto = pd.read_csv(root_path + 'user_active_region/Kyoto.csv')
print (df_kyoto.columns)

active_user_set = set()
our_id_list, city_eng_list = df_kyoto["our_id"], df_kyoto["CITY_ENG"]
for i in range(len(our_id_list)):
    if city_eng_list[i] == city_eng_list[i]:
        active_user_set.add(str(our_id_list[i]))
print (len(active_user_set))

#input: loc: "kyoto"
#output: {"20230101": {"1":{"2":1}}
#date: "20230101"; 
#user: "1"
#loc: "2"
def read_mob(city):
    time1 = time.time()
    card_mob = dict() #include empty_date
    empty_date, error_date = list(), list()
    count_mob = dict()
    idx = 0
    mob_path_city = mob_path + city + "/"
    all_files = os.listdir(mob_path_city)
    for f_name in all_files:
        idx = idx + 1
        
        if f_name[0:2] == "20":
            f_path = mob_path_city + f_name
            date = f_name.split("_")[0]
        
            try:
                with open(f_path, 'r') as f:
                    df = json.load(f)     
                user_dict_day = {j:{} for j in active_user_set}
                count = 0
                for two_hour in df:
                    df_two_hour = df[two_hour]
                    for loc in df_two_hour:
                        for user in df_two_hour[loc]:
                            if user in user_dict_day:
                                user_dict_day[user][loc] = 1
                                count = 1
                card_mob[date] = user_dict_day   #{"20220902": {"123":{"4567":1}}} 
                count_mob[date] = count 
            except:
                error_date.append(date)
                print ("error date: ", date)
        if idx % 5 == 1:
            print (idx)
            time2 = time.time()
            print ("time until now:", time2-time1)

    for date in count_mob:
        if count_mob[date] == 0:
            empty_date.append(date) 
    return card_mob, empty_date, error_date

m_kyo_card, empty_date_kyo, error_date_kyo = read_mob("kyoto")

print (len(m_kyo_card))

empty_date_kyo.sort()
print (empty_date_kyo)
print (len(empty_date_kyo))

error_date_kyo.sort()
print (error_date_kyo)
print (len(error_date_kyo))

#input: loc: "kyoto"
#output: {"20230101": {"1":{"2":1}}
#date: "20230101"; 
#user: "1"
#loc: "2"
def read_texttype(city):
    time1 = time.time()
    
    card_text = dict()
    empty_date = list()
    count_text = dict()
    
    text_path_city = text_type_path + city + "/" + "t1/"
    all_files = os.listdir(text_path_city)
    
    for f_name in all_files:
        if f_name[0:2] == "20":           
            f_path = text_path_city + f_name
            date = f_name.split("_")[0]
            
            with open(f_path, 'r') as f:
                df = json.load(f)
            user_dict_day = {j:{} for j in active_user_set}
            count = 0
            for two_hour in df:
                df_two_hour = df[two_hour]
                for loc in df_two_hour:
                    for user in df_two_hour[loc]:
                        if user in user_dict_day:
                            user_dict_day[user][loc] = 1
                            count = 1
            card_text[date] = user_dict_day   #{"20220902": {"123":{"4567":1}}}
            count_text[date] = count 
    for date in count_text:
        if count_text[date] == 0:
            empty_date.append(date) 
    return card_text, empty_date

t_kyo_card, t_empty_date_kyo = read_texttype("kyoto")

t_empty_date_kyo.sort()
print (t_empty_date_kyo)
print (len(t_empty_date_kyo))

#------------------------------------------------------------------------------
# # 2. compute conditional probability
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# # 2.1 generate date pairs
#------------------------------------------------------------------------------

#[[['20230603', '20230604', '20230605'], '20230606']]
#T to 1. 
def generate_t_1_pair(date_list, t, empty_date_kyo, error_date_kyo):
    generated_pair = list()
    n = len(date_list)
    for i in range(n-t):
        isMissing = 0
        missing_num = 0
        date_seq = [date_list[i+j] for j in range(t+1)]
        for date in date_seq:
             if date in empty_date_kyo or date in error_date_kyo:
                isMissing = 1
        if isMissing == 0:
            generated_pair.append([[date_list[i+j] for j in range(t)], date_list[i+t]])
    return generated_pair

date_kyo_list = list(m_kyo_card.keys())

date_kyo_list.sort()
print (len(date_kyo_list))
generated_item_kyo = generate_t_1_pair(date_kyo_list, 4, empty_date_kyo, error_date_kyo)
print (len(generated_item_kyo))

#------------------------------------------------------------------------------
# # 2.2 specify the mapping from search terms to mobility POIs
#------------------------------------------------------------------------------

kyo_index_to_POI = {"0": "amenity",\
                   "1": "building",\
                   "2": "emergency",\
                   "3": "leisure",\
                   "4": "public_transport",\
                   "5": "shop",\
                   "6": "sport",\
                   "7": "tourism"}

poitype_to_index = {}
with open(folder+"/3_extract_POI/2_kyoto/kyoto_47532.txt", 'r') as file:
    for line in file:
        line_split = line.strip().split(",")
        index, poi_type = line_split[0], line_split[-2]
        if poi_type not in poitype_to_index:
            poitype_to_index[poi_type] = [index]
        else:
            poitype_to_index[poi_type].append(index)

kyo_mapping = {str(i):poitype_to_index[kyo_index_to_POI[str(i)]]  for i in range(len(kyo_index_to_POI))}

#------------------------------------------------------------------------------
# # 2.3 compute values
#------------------------------------------------------------------------------

#input: "fuk", generated_item, m_fuk_card, t_fuk_card, fuk_mapping 
#output: n_search_go_all
def generate_n_search_go(city, generated_item, m_card, t_card, city_mapping):
    #extract the count of search & go
    #input: card {'20220902': {'123': {'4567': 1}}}  without repeat
    #output: [1,1,...,1], [100,100,...,100], [2,2,...,2], [200,200,...,200]
    time1=time.time()
    n_search_go_all = [[], [], [], []] #(search, go), (search, notgo), (notsearch, go), (notsearch, notgo)
    n_user = n_user_dict[city]
    n_poi = n_texttype_dict[city]
    n_day = len(generated_item)

    for i in range(n_day):
        if i%1==0:
            print ("i", i)
        text_x = {j:{} for j in active_user_set}
        for j in range(4):
            print ("j", j)
            d = generated_item[i][0][j]   #'20230603'
            t_one_day = t_card[d]     #[user][loc] = 1
            for user in t_one_day:
                if len(t_one_day[user]) >= 1:
                    for poi in t_one_day[user]:
                        for p_poi in city_mapping[poi]:
                            text_x[user][p_poi] = 1
        print ("text_x done")
        
        mob_y = {j:{} for j in active_user_set}
        d = generated_item[i][1]        #'20230606'
        m_one_day = m_card[d]       #[user][loc] = 1
        for user in m_one_day:    
            if len(m_one_day[user]) >= 1:
                for p_poi in m_one_day[user]:
                    mob_y[user][p_poi] = 1
        
        print ("mob_y done")
        n_search_go, n_search_notgo, n_notsearch_go, n_notsearch_notgo = 0, 0, 0, 0
        for user in active_user_set:
            for poi in range(n_poi):
                str_poi = str(poi)
                a = str_poi in text_x[user]
                b = str_poi in mob_y[user]
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
        time2=time.time()
        print ("running time: ", time2-time1)
    return n_search_go_all

n_search_go_all_kyo = generate_n_search_go("kyo", generated_item_kyo, m_kyo_card, t_kyo_card, kyo_mapping)

print ("search&Go", np.mean(n_search_go_all_kyo[0]))
print ("search&NotGo", np.mean(n_search_go_all_kyo[1]))
print ("NotSearch&Go", np.mean(n_search_go_all_kyo[2]))
print ("NotSearch&NotGo", np.mean(n_search_go_all_kyo[3]))
print (np.sum([np.mean(n_search_go_all_kyo[i]) for i in range(4)]))

def generate_condition_probability(n_search_go_all):
    p_search_then_go = list()
    p_notsearch_then_go = list()
    for i in range(len(n_search_go_all[0])):
        n0, n1, n2, n3 = n_search_go_all[0][i], n_search_go_all[1][i], n_search_go_all[2][i], n_search_go_all[3][i]
        p_search_then_go.append((n0+1)/(n0+n1+1))
        p_notsearch_then_go.append((n2+1)/(n2+n3+1))
    return p_search_then_go, p_notsearch_then_go

p_search_then_go_kyo, p_notsearch_then_go_kyo = generate_condition_probability(n_search_go_all_kyo)

#------------------------------------------------------------------------------
# # 2.4. draw values
#------------------------------------------------------------------------------

fig= plt.figure(figsize=(4,3), dpi=300)
ax = fig.add_subplot(2, 1, 1)
x = range(len(p_search_then_go_kyo))
plt.plot(x, p_search_then_go_kyo, linewidth=1, label="P(Go|Search)", color="orangered")
plt.plot(x, p_notsearch_then_go_kyo, linewidth=1, label="P(Go|NotSearch)", color="deepskyblue")

plt.title('Regular, Kyoto, 2023', fontsize=12)
my_x_ticks = [0, 40, 80, 120, 160]
plt.xticks(my_x_ticks, fontsize=12)
plt.xlabel('Day', fontsize=12)

my_y_ticks = [0, 0.006, 0.012]
plt.yticks(my_y_ticks, fontsize=12)
plt.ylim(bottom=0)
plt.ylabel('Probability', fontsize=12)

plt.legend(loc=1, fontsize=7)
plt.savefig("con_prob_save/" + "kyo.svg", bbox_inches = 'tight')
plt.show()

def save_count(n_search_go_all_city, file_name):
    dict_to_save = {"search_go": n_search_go_all_city[0], "search_notgo": n_search_go_all_city[1],\
                    "notsearch_go": n_search_go_all_city[2], "notsearch_notgo": n_search_go_all_city[3]}
    with open(file_name, 'w') as json_file:
        json.dump(dict_to_save, json_file)

city_name = "kyoto"
save_count(n_search_go_all_kyo, "count_save/" + city_name + ".json")

#------------------------------------------------------------------------------
# # 3. ratio and test
#------------------------------------------------------------------------------

print (np.mean(p_search_then_go_kyo))
print (np.mean(p_notsearch_then_go_kyo))
print ("ratio = ", np.mean(p_search_then_go_kyo)/np.mean(p_notsearch_then_go_kyo))

print (stats.ttest_ind(p_search_then_go_kyo,\
                       p_notsearch_then_go_kyo, alternative="greater"))
