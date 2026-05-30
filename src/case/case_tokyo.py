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

#1. Sample POIs in Tokyo.
#(1) Sports venues.
#7983,139.714558,35.677821,国立競技場,building,stadium                [Japan National Stadium] 
#172264,139.751966,35.705525,東京ドーム,sport,baseball;multi          [Tokyo Dome] 

#(2) Leisure.
#174139,139.772948,35.715004,上野恩賜公園,leisure,park                [Ueno Park] 
#179668,139.396719,35.70951,国営昭和記念公園,leisure,park             [Showa Memorial Park] 
#147731,139.766976,35.659854,浜離宮恩賜庭園,tourism,information        [Hamarikyu Gardens] 

#(3) Shopping.
#127504,139.698672,35.661951,渋谷PARCO,shop,mall                       [Shibuya Parco] 
#3203,139.764053,35.669562,GINZA SIX,building,retail                   [GINZA SIX] 
#7995,139.701114,35.691287,ルミネエスト新宿,building,retail             [LUMINE EST Shinjuku] 

#(4) Tourism.
#149972,139.810714,35.710045,東京スカイツリー,tourism,attraction       [Tokyo Skytree] 
#173525,139.778003,35.633107,お台場レインボー公園,leisure,park          [Odaiba]

#------------------------------------------------------------------------------
# # Step 0: read files
#------------------------------------------------------------------------------

search_go_20_poi_loc = "search_go_20_poi" + "/"
all_files = os.listdir(search_go_20_poi_loc)
print(len(all_files))

home_loc = "2023_YJ_MI_MA/"

loc = home_loc + "2_large_shapefile/"+"tokyo_prefecture_shp/tokyo_prefecture_shp.shp"
df_tokyo = gpd.read_file(loc)
print(len(df_tokyo))
n_tokyo = len(df_tokyo)
df_tokyo.plot()

folder_tokyo = home_loc + "2_large_shapefile/tokyo_prefecture_shp/"
file_tokyo = "tokyo_prefecture_shp.shp" 
tokyo_file = os.path.join(folder_tokyo, file_tokyo)

#------------------------------------------------------------------------------
# # Step 0: functions
#------------------------------------------------------------------------------

def get_search_go(selected_id_list):
    poi_region_search_go_all = {str(poi_id): {str(region_id): [0, 0, 0, 0] for region_id in range(n_tokyo)} for poi_id in selected_id_list}
    poi_region_search_all = {str(poi_id): {str(region_id): 0 for region_id in range(n_tokyo)} for poi_id in selected_id_list}
    poi_region_go_all = {str(poi_id): {str(region_id): 0 for region_id in range(n_tokyo)} for poi_id in selected_id_list}

    for file_name in all_files:
        if file_name[-4:] == "json":
            f_path = "search_go_20_poi/" + file_name
            with open(f_path, 'r') as f:
                df = json.load(f)
                for poi_id in selected_id_list:
                    for region_id in range(n_tokyo):
                        for k in range(4):
                            poi_region_search_go_all[str(poi_id)][str(region_id)][k] += df[str(poi_id)][str(region_id)][k]

                        poi_region_search_all[str(poi_id)][str(region_id)] = df[str(poi_id)][str(region_id)][0]+df[str(poi_id)][str(region_id)][1]
                        poi_region_go_all[str(poi_id)][str(region_id)] = df[str(poi_id)][str(region_id)][0]+df[str(poi_id)][str(region_id)][2]
    return poi_region_search_all, poi_region_go_all, poi_region_search_go_all

def update_data_for_idx(df_tokyo, idx, poi_region_search_all, poi_region_go_all, poi_region_search_go_all):
    df_tokyo_idx = df_tokyo
    df_tokyo_idx[idx+"Search"] = [poi_region_search_all[idx][str(i)] for i in range(n_tokyo)]
    df_tokyo_idx[idx+"Go"] = [poi_region_go_all[idx][str(i)] for i in range(n_tokyo)]
    df_tokyo_idx[idx+"SearchGoRatio"] = [poi_region_search_go_all[idx][str(i)][0]/\
                                 (poi_region_search_go_all[idx][str(i)][0]+poi_region_search_go_all[idx][str(i)][1]+0.001) for i in range(n_tokyo)]
    return df_tokyo_idx

def plot_based_on_column(df_tokyo_idx, column_name, i, x, y, text, lon_sample_list, lat_sample_list,\
                         save_file):
    fig, ax = plt.subplots(1,figsize=(3, 2),dpi=300)
    df_tokyo_idx.plot(ax=ax, linewidth=0.20, edgecolor='black', alpha = 1.0, column = column_name, cmap='Reds')

    large_lon_sample_list = [lon_sample_list[i]]
    large_lat_sample_list = [lat_sample_list[i]]
    plt.scatter(large_lon_sample_list, large_lat_sample_list, s=20, color="dodgerblue", edgecolor='black', linewidths=0.3)
    
    plt.text(x, y, text)
    
    ax.get_xaxis().set_ticks([138.89, 139.97])
    ax.get_yaxis().set_ticks([35.47, 35.93])

    cax = fig.add_axes([0.934, 0.19, 0.03, 0.61])
    vmin, vmax = 0.0, 1.0
    sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm._A = []
    cbar = fig.colorbar(sm, cax=cax)
    cbar.set_ticks([0, 0.5, 1.0])
    cbar.set_ticklabels(['0', '0.5', '1.0'])
    
    plt.savefig(save_file, bbox_inches='tight')
    plt.show()

#------------------------------------------------------------------------------
# # Step 1: Sport places
#------------------------------------------------------------------------------

selected_id_list = [7983, 172264, 180457, 172349, 172529]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    loc_id = str(selected_id_list[i])
    print("loc_id", loc_id)
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_tokyo = gpd.read_file(tokyo_file)
for idx in selected_id_list:
    df_tokyo = update_data_for_idx(df_tokyo, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

pois = dict()
pois["lon"] = [139.714558, 139.751966, 139.527075, 139.794383, 139.699994]
pois["lat"] = [35.677821, 35.705525, 35.664253, 35.643422, 35.667327]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'}
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

#------------------------------------------------------------------------------
# # Japan National Stadium
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "7983"+"SearchGoRatio", 0, 139.06, 35.96,\
                      "Japan National Stadium", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/sports/1_Japan_National_Stadium.pdf")

#------------------------------------------------------------------------------
# # Tokyo Dome
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "172264"+"SearchGoRatio", 1, 139.23, 35.96, 
                     "Tokyo Dome", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/sports/2_Tokyo_Dome.pdf")

#------------------------------------------------------------------------------
# # Step 2: Leisure places
#------------------------------------------------------------------------------

selected_id_list = [174139, 176118, 179668, 174207, 147731]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all["176118"])
print (poi_region_search_all["176118"])
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    loc_id = str(selected_id_list[i])
    print("loc_id", loc_id)
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_tokyo = gpd.read_file(tokyo_file)
for idx in selected_id_list:
    df_tokyo = update_data_for_idx(df_tokyo, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

pois = dict()
pois["lon"] = [139.772948, 139.695217, 139.396719, 139.81645, 139.766976]
pois["lat"] = [35.715004, 35.670226, 35.70951, 35.699019, 35.659854]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} 
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

#------------------------------------------------------------------------------
# # Ueno Park
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "174139"+"SearchGoRatio", 0, 139.25, 35.96,\
                      "Ueno Park", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/leisure/1_Ueno_Park.pdf")

#------------------------------------------------------------------------------
# # Showa Memorial Park
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "179668"+"SearchGoRatio", 2, 139.10, 35.96,\
                      "Showa Memorial Park", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/leisure/3_Showa_Memorial_Park.pdf")

#------------------------------------------------------------------------------
# # Hamarikyu Gardens
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "147731"+"SearchGoRatio", 4, 139.11, 35.96,\
                      "Hamarikyu Gardens", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/leisure/5_Hamarikyu_Gardens.pdf")

#------------------------------------------------------------------------------
# # Step 3: Leisure places
#------------------------------------------------------------------------------

selected_id_list = [127504, 3203, 17657, 128014, 7995]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    loc_id = str(selected_id_list[i])
    print("loc_id", loc_id)
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_tokyo = gpd.read_file(tokyo_file)
for idx in selected_id_list:
    df_tokyo = update_data_for_idx(df_tokyo, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

pois = dict()
pois["lon"] = [139.698672, 139.764053, 139.708707, 139.705415, 139.701114]
pois["lat"] = [35.661951, 35.669562, 35.667288, 35.669135, 35.691287]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'}
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

#------------------------------------------------------------------------------
# # Shibuya Parco
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "127504"+"SearchGoRatio", 0, 139.21, 35.96,\
                      "Shibuya Parco", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/shopping/1_Shibuya_Parco.pdf")

#------------------------------------------------------------------------------
# # GINZA SIX
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "3203"+"SearchGoRatio", 1, 139.25, 35.96,\
                      "GINZA SIX", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/shopping/2_GINZA_SIX.pdf")

#------------------------------------------------------------------------------
# # LUMINE EST Shinjuku
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "7995"+"SearchGoRatio", 4, 139.10, 35.96,\
                      "LUMINE EST Shinjuku", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/shopping/5_LUMINE_EST_Shinjuku.pdf")

#------------------------------------------------------------------------------
# # 4. Tourism
#------------------------------------------------------------------------------

selected_id_list = [55173, 149972, 151164, 173525, 148411]
poi_region_search_all, poi_region_go_all, poi_region_search_go_all = get_search_go(selected_id_list)

print (poi_region_search_go_all)
print (poi_region_search_all)
for i in range(len(selected_id_list)):
    print("----------------------------------------")
    loc_id = str(selected_id_list[i])
    print("loc_id", loc_id)
    print ("search count", np.mean(list(poi_region_search_all[loc_id].values())))
    print ("mobility count", np.mean(list(poi_region_go_all[loc_id].values())))

df_tokyo = gpd.read_file(tokyo_file)
for idx in selected_id_list:
    df_tokyo = update_data_for_idx(df_tokyo, str(idx), poi_region_search_all, poi_region_go_all, poi_region_search_go_all)

pois = dict()
pois["lon"] = [139.796072, 139.810714, 139.700525, 139.778003, 139.745446]
pois["lat"] = [35.713954, 35.710045, 35.67398, 35.633107, 35.658586]
lon_sample_list = list(pois["lon"])
lat_sample_list = list(pois["lat"])
data = {"lon": lon_sample_list, "lat": lat_sample_list, "geometry":[0 for i in range(len(lon_sample_list))]}
home_df = pd.DataFrame(data, index=[i for i in range(len(lon_sample_list))])
home_crs = {'init':'epsg:4326'} 
home_geometry = [Point(xy) for xy in zip(lon_sample_list, lat_sample_list)]
home_gpd = gpd.GeoDataFrame(home_df, crs = home_crs, geometry = home_geometry)

#------------------------------------------------------------------------------
# # Tokyo Skytree
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "149972"+"SearchGoRatio", 1, 139.215, 35.96,\
                      "Tokyo Skytree", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/tourism/2_Tokyo_Skytree.pdf")

#------------------------------------------------------------------------------
# # Odaiba
#------------------------------------------------------------------------------

plot_based_on_column(df_tokyo, "173525"+"SearchGoRatio", 3, 139.31, 35.96,\
                      "Odaiba", lon_sample_list, lat_sample_list,\
                        save_file="plot_20/tourism/4_Odaiba.pdf")
