import os
import geopandas as gpd
from pyproj import Geod

#------------------------------------------------------------------------------
# # 1. Read the shapefile
#------------------------------------------------------------------------------

folder_japan = "japan_shp/"
file_japan = "japan_ver821.shp" 
japan_file = os.path.join(folder_japan, file_japan) 
df_japan = gpd.read_file(japan_file)

df_japan.plot()

#------------------------------------------------------------------------------
# # 2. List the region for Tokyo
#------------------------------------------------------------------------------

df_column = df_japan.columns
print (df_column)

df_tokyo_name_1 =\
['Chiyoda-ku', 'Chuo-ku', 'Minato-ku', 'Shinjuku-ku', 'Bunkyo-ku',\
 'Taito-ku', 'Sumida-ku', 'Koto-ku', 'Shinagawa-ku', 'Meguro-ku',\
 'Ota-ku', 'Setagaya-ku', 'Shibuya-ku', 'Nakano-ku', 'Suginami-ku',\
 'Toshima-ku', 'Kita-ku', 'Arakawa-ku', 'Itabashi-ku', 'Nerima-ku',\
 'Adachi-ku', 'Katsushika-ku','Edogawa-ku']

df_tokyo_name_2 =\
["Hachioji-shi", "Tachikawa-shi", "Musashino-shi", "Mitaka-shi", "Ome-shi",\
"Fuchu-shi","Akishima-shi", "Chofu-shi", "Machida-shi", "Koganei-shi",\
"Kodaira-shi", "Hino-shi", "Higashimurayama-shi", "Kokubunji-shi", "Kunitachi-shi",\
"Fussa-shi", "Komae-shi", "Higashiyamato-shi", "Kiyose-shi", "Higashikurume-shi",\
"Musashimurayama-shi", "Tama-shi", "Inagi-shi", "Hamura-shi", "Akiruno-shi",\
"Nishitokyo-shi", "Mizuho-machi", "Hinode-machi", "Hinohara-mura", "Okutama-machi"]

#["Oshima-machi", "Miyake-mura", "Hachijo-machi", "Ogasawara-mura"]
#Islands = "Toshima-mura", "Fuchu-shi", "Aogashima-mura", "Mikurajima-mura", "Kouzushima-mura",
#"Niijima-mura", "Toshima-mura"
#df_tokyo = df_japan[df_japan["KEN"]=='東京都']
df_tokyo = df_japan[df_japan["CITY_ENG"].isin(df_tokyo_name_1+df_tokyo_name_2)]
df_tokyo = df_tokyo[~df_tokyo["JCODE"].isin(["34208"])]
print (len(df_tokyo))

df_tokyo.plot()

geod = Geod(ellps="WGS84")
area = 0.0
for i in range(len(df_tokyo)):
    poly = list(df_tokyo["geometry"])[i]
    area += abs(geod.geometry_area_perimeter(poly)[0])
print (area/1000/1000)

print ("population", sum(df_tokyo["P_NUM"]))
print (sum(df_tokyo["H_NUM"]))

df_tokyo.to_file("tokyo_shp")
