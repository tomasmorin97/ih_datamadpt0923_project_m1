# LEEMOS EL SET DE DATOS:
# El objetivo de este punto es llegar a leer los datos y transformarlos en un dataframe de pandas

#Import libraries
import pandas as pd
import requests
import modules.extraction as ex
import modules.analysis as an
import modules.argparse as arg
from shapely.geometry import Point
import geopandas as gpd
import argparse
from fuzzywuzzy import process

# Data

#Construimos el url para coger el json de espacios deportivos
bicimad_path = "./data/bicimad_stations.csv"
bicipark_path = "./data/bicipark_stations.csv"
#Construimos el url para coger el json de espacios deportivos
url = "https://datos.madrid.es/egob/catalogo/212808-0-espacio-deporte.json"
#body = "/catalogo/212808-0-espacio-deporte.json"

def main():
    # Leemos los tres datasets
    df_bicimad = ex.data_bicimad(bicimad_path)
    df_bicipark = ex.data_bicipark(bicipark_path)
    df_deporte = ex.data_deporte(url)
    # Limpiamos los datos y los organizamos como queremos
    # Bicimad
    # Columnas con las que nos quedamos
    field = "geometry.coordinates"
    bicimad_columnas = ['id', 'name', 'address', 'dock_bikes', 'Longitud', 'Latitud']
    df_bicimad1 = ex.coordinates_separator(df_bicimad, bicimad_columnas, ex.separator_longitud, ex.separator_latitud, field)
    # Bicipark
    bicipark_columnas = ['stationId', 'stationName', 'address', 'dock_bikes', 'Longitud', 'Latitud']
    df_bicipark_int = ex.available_bikes(df_bicipark,'total_places','free_places')
    df_bicipark1 = ex.coordinates_separator(df_bicipark, bicipark_columnas, ex.separator_longitud, ex.separator_latitud, field)
    # Deporte
    deporte_columnas = ["id","title", "address", "Longitud","Latitud"]
    deporte_columnas_final = ["id","title", "address_final", "Longitud","Latitud"]
    field_json = "location"
    df_deporte_int = ex.coordinates_separator(df_deporte, deporte_columnas, ex.separator_longitud_json, ex.separator_latitud_json, field_json)
    df_deporte1 = ex.deporte_clean (df_deporte_int, ex.address_extractor,deporte_columnas_final)

    # ANÁLISIS
    # Bicimad
    column_rename1 = {'title': 'Sports spot', 'address_final': 'Sports Address', 'name': 'BiciMAD spot', 'address': 'Address BiciMAD', 'dock_bikes':'Available bikes', 'Distancia en m': 'Distance in m'}
    column_list1 = ["Sports spot", "Sports Address", "BiciMAD spot", "Address BiciMAD", "Available bikes", "Distance in m"]
    bicimad_merge = an.merge(df_deporte1, df_bicimad1)
    bicimad_min_dist = an.distance_min (bicimad_merge, an.distance_meters)
    print(bicimad_min_dist)
    bicimad_clean = an.column_cleaning (bicimad_min_dist, column_list1, column_rename1)
    print(bicimad_clean)

    # Bicipark
    df_bicipark1["key"] = 0
    column_rename2 = {'title': 'Sports spot', 'address_final': 'Sports Address', 'stationName': 'BiciPark spot',  'address': 'Address BiciPark', 'dock_bikes':'Available bikes', 'Distancia en m': 'Distance in m'}
    column_list2 = ["Sports spot", "Sports Address", "BiciPark spot", "Address BiciPark", "Available bikes", "Distance in m"]
    bicipark_merge = an.merge(df_deporte1, df_bicipark1)
    bicipark_min_dist = an.distance_min (bicipark_merge, an.distance_meters)
    bicipark_clean = an.column_cleaning (bicipark_min_dist, column_list2, column_rename2)
    print(bicipark_clean)

    # Guardamos en un CSV en la ruta correspondiente
    bicimad_path_final = "./output/bicimad_distance.csv"
    bicipark_path_final = "./output/bicipark_distance.csv"
    an.data_output(bicimad_clean, bicipark_clean, bicimad_path_final, bicipark_path_final)

    arg.argument_parser
    print(arg.funcion_arg_parse())
# Argparse y FuzzyBuzzy
#Fuzzy
if __name__ == '__main__':
    main ()