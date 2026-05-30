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
# # 2. List the regions for Kyoto, Fukuoka, Kagoshima, and Kumamoto
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# # 2.1 Kyoto
#------------------------------------------------------------------------------

df_kyoto = df_japan[df_japan["KEN"]=='京都府']
print (len(df_kyoto))

df_kyoto.plot()

geod = Geod(ellps="WGS84")
area = 0.0
for i in range(len(df_kyoto)):
    poly = list(df_kyoto["geometry"])[i]
    area += abs(geod.geometry_area_perimeter(poly)[0])
print (area/1000/1000)

print ("population", sum(df_kyoto["P_NUM"]))

df_kyoto.to_file("kyoto_shp")

#------------------------------------------------------------------------------
# # 2.2 Fukuoka
#------------------------------------------------------------------------------

df_fukuoka_name =\
['Fukuoka-shi, Higashi-ku', 'Fukuoka-shi, Hakata-ku', 'Fukuoka-shi, Chuo-ku',\
 'Fukuoka-shi, Minami-ku', 'Fukuoka-shi, Nishi-ku', 'Fukuoka-shi, Jonan-ku',\
 'Fukuoka-shi, Sawara-ku']
df_fukuoka = df_japan[df_japan["KEN"]=='福岡県']
print (len(df_fukuoka))

df_fukuoka.plot()

geod = Geod(ellps="WGS84")
area = 0.0
for i in range(len(df_fukuoka)):
    poly = list(df_fukuoka["geometry"])[i]
    area += abs(geod.geometry_area_perimeter(poly)[0])
print (area/1000/1000)

print ("population", sum(df_fukuoka["P_NUM"]))

df_fukuoka.to_file("fukuoka_shp")

#------------------------------------------------------------------------------
# # 2.3 Kagoshima
#------------------------------------------------------------------------------

df_kagoshima = df_japan[df_japan["KEN"]=='鹿児島県']
df_kagoshima = df_kagoshima[df_kagoshima["geometry"].centroid.y > 30.938891]
print (len(df_kagoshima))

df_kagoshima.plot()

geod = Geod(ellps="WGS84")
area = 0.0
for i in range(len(df_kagoshima)):
    poly = list(df_kagoshima["geometry"])[i]
    area += abs(geod.geometry_area_perimeter(poly)[0])
print (area/1000/1000)

print ("population", sum(df_kagoshima["P_NUM"]))

df_kagoshima.to_file("kagoshima_shp")

#------------------------------------------------------------------------------
# # 2.4. Kumamoto
#------------------------------------------------------------------------------

df_kumamoto = df_japan[df_japan["KEN"]=='熊本県']
print (len(df_kumamoto))

df_kumamoto.plot()

geod = Geod(ellps="WGS84")
area = 0.0
for i in range(len(df_kumamoto)):
    poly = list(df_kumamoto["geometry"])[i]
    area += abs(geod.geometry_area_perimeter(poly)[0])
print (area/1000/1000)

print ("population", sum(df_kumamoto["P_NUM"]))

df_kumamoto.to_file("kumamoto_shp")
