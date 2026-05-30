import os
import json
import numpy as np
import pandas as pd
import random
import geopandas as gpd

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from shapely.geometry import Point
from sklearn.linear_model import LinearRegression

#------------------------------------------------------------------------------
# # Step 1: read files
#------------------------------------------------------------------------------

search_go_five_poi_loc = "search_go_16_poi" + "/"
all_files = os.listdir(search_go_five_poi_loc)
print(len(all_files))

folder_kyoto = "2023_YJ_MI_MA/2_large_shapefile/kyoto_shp/"
file_kyoto = "kyoto_shp.shp" 
kyoto_file = os.path.join(folder_kyoto, file_kyoto) 
print(kyoto_file)

#------------------------------------------------------------------------------
# # Step 2: functions
#------------------------------------------------------------------------------

def get_search_go(selected_id_list):
    #selected_id_list = [46656, 45712, 45728, 45941]
    poi_region_search_go_all = {str(poi_id): {str(region_id): [0, 0, 0, 0] for region_id in range(36)} for poi_id in selected_id_list}
    poi_region_search_all = {str(poi_id): {str(region_id): 0 for region_id in range(36)} for poi_id in selected_id_list}
    poi_region_go_all = {str(poi_id): {str(region_id): 0 for region_id in range(36)} for poi_id in selected_id_list}

    for file_name in all_files:
        if file_name[-4:] == "json":
            f_path = "search_go_16_poi/" + file_name
            with open(f_path, 'r') as f:
                df = json.load(f)
                for poi_id in selected_id_list:
                    for region_id in range(36):
                        for k in range(4):
                            poi_region_search_go_all[str(poi_id)][str(region_id)][k] += df[str(poi_id)][str(region_id)][k]

                        poi_region_search_all[str(poi_id)][str(region_id)] = df[str(poi_id)][str(region_id)][0]+df[str(poi_id)][str(region_id)][1]
                        poi_region_go_all[str(poi_id)][str(region_id)] = df[str(poi_id)][str(region_id)][0]+df[str(poi_id)][str(region_id)][2]
    return poi_region_search_all, poi_region_go_all, poi_region_search_go_all

#Append information to shapefile
def update_data_for_idx(df_kyoto, idx, poi_region_search_all, poi_region_go_all, poi_region_search_go_all):
    df_kyoto_idx = df_kyoto
    df_kyoto_idx[idx+"Search"] = [poi_region_search_all[idx][str(i)] for i in range(36)]
    df_kyoto_idx[idx+"Go"] = [poi_region_go_all[idx][str(i)] for i in range(36)]
    df_kyoto_idx[idx+"SearchGoRatio"] = [poi_region_search_go_all[idx][str(i)][0]/\
                                 (poi_region_search_go_all[idx][str(i)][0]+poi_region_search_go_all[idx][str(i)][1]+0.001) for i in range(36)]
    return df_kyoto_idx

def plot_based_on_column(df_kyoto_idx, column_name, i, x, y, text, lon_sample_list, lat_sample_list,\
                         save_file):
    fig, ax = plt.subplots(1,figsize=(3, 2),dpi=300)
    df_kyoto_idx.plot(ax=ax, linewidth=0.20, edgecolor='black', alpha = 1.0, column = column_name, cmap='Reds')

    large_lon_sample_list = [lon_sample_list[i]]
    large_lat_sample_list = [lat_sample_list[i]]
    plt.scatter(large_lon_sample_list, large_lat_sample_list, s=20, color="dodgerblue", edgecolor='black', linewidths=0.3)
    
    plt.text(x, y, text)
    #plt.text(x_loc, y_loc, text_loc)
    
    ax.get_xaxis().set_ticks([135.32, 135.93])
    ax.get_yaxis().set_ticks([34.84, 35.43])

    cax = fig.add_axes([0.76, 0.11, 0.03, 0.77])
    vmin, vmax = 0.0, 1.0
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm, cax=cax)
    
    cbar.set_ticks([0, 0.5, 1.0])
    cbar.set_ticklabels(['0', '0.5', '1.0'])

    #plt.text(-12, 1.03, "Origin of search \n to Kiyomizu-dera")
    plt.savefig(save_file, bbox_inches='tight')
    plt.show()

#------------------------------------------------------------------------------
# # Sport places
#------------------------------------------------------------------------------

selected_id_list = [46656, 45712, 45728, 45941]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    loc_id = str(selected_id_list[i])
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))


df_kyoto = gpd.read_file(kyoto_file)
for idx in selected_id_list:
    df_kyoto = update_data_for_idx(df_kyoto, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

df_kyoto_CITY_ENG = list(df_kyoto["CITY_ENG"])
new_list = list()
for i in range(len(df_kyoto_CITY_ENG)):
    if df_kyoto_CITY_ENG[i][0:9] == "Kyoto-shi" or df_kyoto_CITY_ENG[i] == "Kameoka-shi" or df_kyoto_CITY_ENG[i] == "Nantan-shi":
        new_list.append("Kyoto-shi")
    else:
        new_list.append("0")
        
df_kyoto["NEW_CITY_ENG"] = new_list
df_kyoto = df_kyoto[df_kyoto["NEW_CITY_ENG"]=="Kyoto-shi"]

pois = dict()
pois["lon"] = [135.584884, 135.71502, 135.714637, 135.72728]
pois["lat"] = [35.017142, 34.995511, 34.993315, 34.906381]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} # define coordinate reference system
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

plot_based_on_column(df_kyoto, "46656"+"SearchGoRatio", 0, 135.375, 35.46,\
                      "Sanga Stadium \n  by KYOCERA", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/sports/1_Sanga_Stadium_by_KYOCERA.pdf")

plot_based_on_column(df_kyoto, "45712"+"SearchGoRatio", 1, 135.30, 35.46, 
                     "Kataoka Arena Kyoto", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/sports/2_Kataoka_Arena_Kyoto.pdf")

plot_based_on_column(df_kyoto, "45728"+"SearchGoRatio", 2, 135.41, 35.46, "Nishikyogoku \n Athletic Park",\
                     lon_sample_list, lat_sample_list, 
                     save_file="plot_16_kyoto_20260406/sports/3_Nishikyogoku_Athletic_Park.pdf")

#------------------------------------------------------------------------------
# # Leisure places
#------------------------------------------------------------------------------

selected_id_list = [1147, 3711, 15896, 1670]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    print("loc_id", loc_id)
    loc_id = str(selected_id_list[i])
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_kyoto = gpd.read_file(kyoto_file)
for idx in selected_id_list:
    df_kyoto = update_data_for_idx(df_kyoto, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

df_kyoto_CITY_ENG = list(df_kyoto["CITY_ENG"])
new_list = list()
for i in range(len(df_kyoto_CITY_ENG)):
    if df_kyoto_CITY_ENG[i][0:9] == "Kyoto-shi" or df_kyoto_CITY_ENG[i] == "Kameoka-shi" or df_kyoto_CITY_ENG[i] == "Nantan-shi":
        new_list.append("Kyoto-shi")
    else:
        new_list.append("0")
        
df_kyoto["NEW_CITY_ENG"] = new_list
df_kyoto = df_kyoto[df_kyoto["NEW_CITY_ENG"]=="Kyoto-shi"]

pois = dict()
pois["lon"] = [135.780824, 135.747744, 135.772406, 135.780964]
pois["lat"] = [35.014303, 34.987589, 35.003482, 35.012842]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} # define coordinate reference system
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

plot_based_on_column(df_kyoto, "1147"+"SearchGoRatio", 0, 135.29, 35.46,\
                      "ROHM Theatre Kyoto", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/leisure/1_ROHM_Theatre_Kyoto.pdf")

plot_based_on_column(df_kyoto, "15896"+"SearchGoRatio", 2, 135.34, 35.46,\
                      "Minamiza Theater", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/leisure/3_Minamiza_Theater.pdf")

plot_based_on_column(df_kyoto, "1670"+"SearchGoRatio", 3, 135.32, 35.46,\
                      "Kyoto International \n    Exhibition Hall", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/leisure/4_Kyoto_International_Exhibition_Hall.pdf")

#------------------------------------------------------------------------------
# # Shopping places
#------------------------------------------------------------------------------

selected_id_list = [4164, 15439, 27764, 28900]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    print("loc_id", loc_id)
    loc_id = str(selected_id_list[i])
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_kyoto = gpd.read_file(kyoto_file)
for idx in selected_id_list:
    df_kyoto = update_data_for_idx(df_kyoto, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

df_kyoto_CITY_ENG = list(df_kyoto["CITY_ENG"])
new_list = list()
for i in range(len(df_kyoto_CITY_ENG)):
    if df_kyoto_CITY_ENG[i][0:9] == "Kyoto-shi" or df_kyoto_CITY_ENG[i] == "Kameoka-shi" or df_kyoto_CITY_ENG[i] == "Nantan-shi":
        new_list.append("Kyoto-shi")
    else:
        new_list.append("0")
        
df_kyoto["NEW_CITY_ENG"] = new_list
df_kyoto = df_kyoto[df_kyoto["NEW_CITY_ENG"]=="Kyoto-shi"]

pois = dict()
pois["lon"] = [135.755855, 135.764949, 135.741148, 135.72091]
pois["lat"] = [34.982737, 35.005019, 35.010532, 35.004171]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} # define coordinate reference system
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

plot_based_on_column(df_kyoto, "15439"+"SearchGoRatio", 1, 135.40, 35.46,\
                      "Nishiki Market", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/shopping/2_Nishiki_Market.pdf")

plot_based_on_column(df_kyoto, "27764"+"SearchGoRatio", 2, 135.475, 35.46,\
                      "BiVi-Nijō", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/shopping/3_BiVi_Nijo.pdf")

plot_based_on_column(df_kyoto, "28900"+"SearchGoRatio", 3, 135.425, 35.46,\
                      "Kyoto Family", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/shopping/4_Kyoto_Family.pdf")

#------------------------------------------------------------------------------
# # Tourism
#------------------------------------------------------------------------------

selected_id_list = [35267, 33166, 34743, 35308]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    print("loc_id", loc_id)
    loc_id = str(selected_id_list[i])
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_kyoto = gpd.read_file(kyoto_file)
for idx in selected_id_list:
    df_kyoto = update_data_for_idx(df_kyoto, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

df_kyoto_CITY_ENG = list(df_kyoto["CITY_ENG"])
new_list = list()
for i in range(len(df_kyoto_CITY_ENG)):
    if df_kyoto_CITY_ENG[i][0:9] == "Kyoto-shi" or df_kyoto_CITY_ENG[i] == "Kameoka-shi" or df_kyoto_CITY_ENG[i] == "Nantan-shi":
        new_list.append("Kyoto-shi")
    else:
        new_list.append("0")
        
df_kyoto["NEW_CITY_ENG"] = new_list
df_kyoto = df_kyoto[df_kyoto["NEW_CITY_ENG"]=="Kyoto-shi"]

pois = dict()
pois["lon"] = [135.784466, 135.730211, 135.748549, 135.75933]
pois["lat"] = [34.99453, 35.039089, 35.01396, 34.987552]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} # define coordinate reference system
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

plot_based_on_column(df_kyoto, "33166"+"SearchGoRatio", 1, 135.48, 35.46,\
                      "Kinkaku-ji", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/tourism/2_Kinkaku-ji.pdf")

plot_based_on_column(df_kyoto, "34743"+"SearchGoRatio", 2, 135.44, 35.46,\
                      "Nijo Casetle", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/tourism/3_Nijo_Casetle.pdf")

plot_based_on_column(df_kyoto, "35308"+"SearchGoRatio", 3, 135.34, 35.46,\
                      "Nidec Kyoto Tower", lon_sample_list, lat_sample_list,\
                        save_file="plot_16_kyoto_20260406/tourism/4_Nidec_Kyoto_Tower.pdf")
