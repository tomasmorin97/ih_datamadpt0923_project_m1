# LEEMOS EL SET DE DATOS:
# El objetivo de este punto es llegar a leer los datos y transformarlos en un dataframe de pandas

#Import libraries
import pandas as pd
import requests

#Leemos el csv de bicimad estaciones
df_bicimad = pd.read_csv("./data/bicimad_stations.csv", sep='\t')

#Leemos el csv de bicipark estaciones
df_bicipark = pd.read_csv("./data/bicipark_stations.csv", sep=';')

#Construimos el url para coger el json de espacios deportivos
base_url = "https://datos.madrid.es/egob"
body = "/catalogo/212808-0-espacio-deporte.json"
response = requests.get(base_url + body)
print(response)

#Cogemos el content del json
content = response.content
json_data = response.json()

#Vemos las keys del json porque no construye un df partiendo del json
print(json_data.keys())

#La información que nos interesa es la de la key de graph
df_deporte = pd.DataFrame(json_data['@graph'])
print(df_deporte)

#LIMPIEZA DE DATOS
#El objetivo de este punto es llegar a tener todos los datos de la forma más limpia posible

#BICIMAD
#Exploramos los datos
print(df_bicimad.head())
print(df_bicimad.info())

# El objetivo es separar latitud y longitud, así que observamos un registro:
df_bicimad["geometry.coordinates"][0]
# La longitud es el primer elemento de la lista y la latitud el segundo:
def separator_longitud(column):
    return float(column.split(',')[0].replace('[',''))
def separator_latitud(column):
    return float(column.split(',')[1].replace(']',''))

# Comprobamos que funciona en un registro concreto
print(separator_latitud(df_bicimad["geometry.coordinates"][0]))

# Aplicamos las funciones a toda la columna del geometry coordinates:
df_bicimad['Longitud'] = df_bicimad.apply(lambda x: separator_longitud(x["geometry.coordinates"]), axis=1)
df_bicimad['Latitud'] = df_bicimad.apply(lambda x: separator_latitud(x["geometry.coordinates"]), axis=1)
print(df_bicimad.head())

# Seleccionamos las columnas que vamos a necesitar:
df_bicimad_res = df_bicimad[['id', 'name', 'address', 'dock_bikes', 'Longitud', 'Latitud']]
print(df_bicimad_res)

#BICIPARK
#Exploramos los datos
print(df_bicipark.head())
print(df_bicipark.info())

# Añadimos el campo de las bicis disponibles
df_bicipark['dock_bikes'] = df_bicipark['total_places'] - df_bicipark['free_places']
print(df_bicipark)

# Aplicamos las funciones que separan las columnas de latitud y longitud a todo el dataframe:
df_bicipark['Longitud'] = df_bicipark.apply(lambda x: separator_longitud(x["geometry.coordinates"]), axis=1)
df_bicipark['Latitud'] = df_bicipark.apply(lambda x: separator_latitud(x["geometry.coordinates"]), axis=1)
print(df_bicipark)

# Seleccionamos las columnas que vamos a necesitar:
df_bicipark_res = df_bicipark[['stationId', 'stationName', 'address', 'dock_bikes', 'Longitud', 'Latitud']]
print(df_bicipark_res)

# ESPACIO DEPORTE
# Exploramos los datos
print(df_deporte.info())
print(df_deporte.head())
print(df_deporte["location"][0]['longitude'])

# El objetivo es obtener la latitud y longitud para poder meterla en dos campos
# Al estar en un diccionario, hacemos una función que extraiga el valor de lat y lon
def separator_longitud_json(column):
    for i in column:
        return column["longitude"]
def separator_latitud_json(column):
    for i in column:
        return column["latitude"]
    
# Comprobamos que funcione correctamente
print(separator_longitud_json(df_deporte["location"][0]))

# Aplicamos a todo el dataframe
df_deporte['Longitud'] = df_deporte.apply(lambda x: separator_longitud_json(x["location"]), axis=1)
df_deporte['Latitud'] = df_deporte.apply(lambda x: separator_latitud_json(x["location"]), axis=1)
print(df_deporte)

# Observamos el que el valor de address está en un diccionario dentro de la key street-address
df_deporte['address'][0]['street-address']

# Diseñamos una función que extraiga el valor de address de un diccionario
def address_extractor (column):
    for i in column:
        return column["street-address"]
    
# Comprobamos que funcione
print(address_extractor (df_deporte['address'][0]))

# Aplicamos a todo el dataframe para añadir un campo con el address
df_deporte['address_final'] = df_deporte.apply(lambda row: address_extractor(row["address"]), axis=1)
print(df_deporte)

# Seleccionamos únicamente los campos que nos interesan para poder hacer los cálculos
df_deporte_res = df_deporte[["id","title", "address_final", "Longitud","Latitud"]]
print(df_deporte_res)

# ANÁLISIS DE DATOS
# BiciMAD
# conda install -c conda-forge geopandas 
# (shapely is a geopandas dependance)

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

# Comprobación del funcionamiento de la función para un valor
print(distance_meters(40.4400607, -3.6425358, 40.4234825, -3.6292625))

# Comprobación del funcionamiento de la función para cada valor de una columna
df_deporte['Mercator point'] = df_deporte.apply(lambda x: to_mercator(x['Latitud'], x['Longitud']), axis=1)
print(df_deporte['Mercator point'])

# El objetivo ahora es conseguir un df en el que cada punto de interés esté asociado con un punto de bicimad
# De esta forma conseguiremos calcular las distancias entre cada punto
# Posteriormente seleccionaremos la distancia mínima
# Añadimos una key a cada valor para que luego haga el merge por cada una de las keys
df_deporte_res["key"] = 0
df_bicimad_res["key"] = 0

# Hacemos un merge para tener la relación de cada punto de interés con los bicimad
df_distancia_bicimad = pd.merge(df_deporte_res, df_bicimad_res, on = 'key')
print(df_distancia_bicimad)

# Apply lambda al dataframe y así recorre toda la fila aplicando la función distance meters
df_distancia_bicimad['Distancia en m'] = df_distancia_bicimad.apply(lambda x: distance_meters(x['Latitud_x'], x['Longitud_x'], x['Latitud_y'], x['Longitud_x']), axis=1)
print(df_distancia_bicimad)

# Encontrar el índice del mínimo valor en la columna distance meters
dist_min_idx_bicimad = df_distancia_bicimad.groupby(["title"])['Distancia en m'].idxmin()
print(dist_min_idx_bicimad)

# Seleccionar el mínimo valor y el resto de los registros
df_distancia_bicimad_min = df_distancia_bicimad.loc[dist_min_idx_bicimad].reset_index()
print(df_distancia_bicimad_min)

# BiciPark

df_bicipark_res["key"] = 0

# Hacemos un merge para tener la relación de cada punto de interés con los bicipark
df_distancia_bicipark = pd.merge(df_deporte_res, df_bicipark_res, on = 'key')
print(df_distancia_bicipark)

# Apply lambda al dataframe y así recorre toda la fila aplicando la función distance meters
df_distancia_bicipark['Distancia en m'] = df_distancia_bicipark.apply(lambda x: distance_meters(x['Latitud_x'], x['Longitud_x'], x['Latitud_y'], x['Longitud_x']), axis=1)
print(df_distancia_bicipark)

# Encontrar el índice del mínimo valor en la columna distance meters
dist_min_idx_bicipark = df_distancia_bicipark.groupby(["title"])['Distancia en m'].idxmin()
print(dist_min_idx_bicipark)

# Seleccionar el mínimo valor y el resto de los registros
df_distancia_bicipark_min = df_distancia_bicipark.loc[dist_min_idx_bicipark].reset_index()
print(df_distancia_bicipark_min)

# LIMPIEZA DE DATOS FINALES
# BiciMAD

#Seleccionamos las collumnas relevantes para el ejercicio
df_distancia_bicimad_min[["title", "address_final", "name", "address", "dock_bikes", "Distancia en m"]]

#Renombrado de columnas
df_distancia_bicimad_min = df_distancia_bicimad_min.rename(columns = {'title': 'Sports spot', 'address_final': 'Sports Address', 'name': 'BiciMAD spot', 'address': 'Address BiciMAD', 'dock_bikes':'Available bikes', 'Distancia en m': 'Distance in m'})
df_distancia_bicimad_min_res = df_distancia_bicimad_min[["Sports spot", "Sports Address", "BiciMAD spot", "Address BiciMAD", "Available bikes", "Distance in m"]]
print(df_distancia_bicimad_min_res)

#BiciPark

#Seleccionamos las collumnas relevantes para el ejercicio
df_distancia_bicipark_min[["title", "address_final", "stationName", "address", "dock_bikes", "Distancia en m"]]

#Renombrado de columnas
df_distancia_bicipark_min = df_distancia_bicipark_min.rename(columns = {'title': 'Sports spot', 'address_final': 'Sports Address', 'stationName': 'BiciPark spot',  'address': 'Address BiciPark', 'dock_bikes':'Available bikes', 'Distancia en m': 'Distance in m'})
df_distancia_bicipark_min_res = df_distancia_bicipark_min[["Sports spot", "Sports Address", "BiciPark spot", "Address BiciPark", "Available bikes", "Distance in m"]]
print(df_distancia_bicipark_min_res)

# Guardamos en un CSV en la ruta correspondiente
df_distancia_bicimad_min_res.to_csv("../output/bicimad_distance.csv")
df_distancia_bicipark_min_res.to_csv("../output/bicipark_distance.csv")




# import library