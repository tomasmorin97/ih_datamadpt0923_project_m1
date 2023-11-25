
# ANÁLISIS DE DATOS
# BiciMAD
# conda install -c conda-forge geopandas 
# (shapely is a geopandas dependance)

import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

# Methods

def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c

def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair points in degrees 
    # (e.g.: Start Point -> 40.4400607 / -3.6425358 End Point -> 40.4234825 / -3.6292625)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)


# El objetivo ahora es conseguir un df en el que cada punto de interés esté asociado con un punto de bicimad
# De esta forma conseguiremos calcular las distancias entre cada punto
# Posteriormente seleccionaremos la distancia mínima
# Añadimos una key a cada valor para que luego haga el merge por cada una de las keys
def merge (df1, df2):
    df1["key"] = 0
    df2["key"] = 0
    df3 = pd.merge(df1, df2, on = 'key')
    return df3
# Hacemos un merge para tener la relación de cada punto de interés con los bicimad
# Apply lambda al dataframe y así recorre toda la fila aplicando la función distance meters
def distance_min(df, function):
    df['Distancia en m'] = df.apply(lambda x: function(x['Latitud_x'], x['Longitud_x'], x['Latitud_y'], x['Longitud_x']), axis=1)
# Encontrar el índice del mínimo valor en la columna distance meters
    df1 = df.groupby(["title"])['Distancia en m'].idxmin()
# Seleccionar el mínimo valor y el resto de los registros
    df_min_distance = df.loc[df1].reset_index()
    return df_min_distance

# BiciPark
# Mismas funciones que en bicimad

# LIMPIEZA DE DATOS FINALES
# BiciMAD
#Seleccionamos las columnas relevantes para el ejercicio y las renombras

def column_cleaning (df, column_list, column_rename):
    df.rename(columns = column_rename)
    df1 = df[column_list]
    return df1


# Guardamos en un CSV en la ruta correspondiente
def data_output(df1, df2, path1, path2):
    df1.to_csv(path1)
    df2.to_csv(path2)
    return "Both files were succesfully saved"


