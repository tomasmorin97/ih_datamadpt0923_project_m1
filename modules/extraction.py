# LEEMOS EL SET DE DATOS:
# El objetivo de este punto es llegar a leer los datos y transformarlos en un dataframe de pandas

#Import libraries
import pandas as pd
import requests


#Leemos el csv de bicimad estaciones y bicipark estaciones
def data_bicimad(bicimad_data):
    df_bicimad = pd.read_csv(bicimad_data, sep='\t')
    return df_bicimad

def data_bicipark(bicipark_data):
    df_bicipark = pd.read_csv(bicipark_data, sep=';')
    return df_bicipark

def data_deporte(url):
    response = requests.get(url)
    json_data = response.json()
    df_deporte = pd.DataFrame(json_data['@graph'])
    return df_deporte


#LIMPIEZA DE DATOS
#El objetivo de este punto es llegar a tener todos los datos de la forma más limpia posible

#BICIMAD
#Exploramos los datos

# El objetivo es separar latitud y longitud:
# La longitud es el primer elemento de la lista y la latitud el segundo:
def separator_longitud(column):
    return float(column.split(',')[0].replace('[',''))
def separator_latitud(column):
    return float(column.split(',')[1].replace(']',''))
    

# Aplicamos las funciones a toda la columna del geometry coordinates y seleccionamos las columnas correspondientes:
# Me vale para bicimad y bicipark
def coordinates_separator(df, lista_columnas, function_lat, function_long, field):
    df['Longitud'] = df.apply(lambda x: function_long(x[field]), axis=1)
    df['Latitud'] = df.apply(lambda x: function_lat(x[field]), axis=1)
    df_clean = df[lista_columnas]
    return df_clean


#BICIPARK
def available_bikes(df, spots, free_spots):
    df['dock_bikes'] = df[spots] - df[free_spots]
    return df

# ESPACIO DEPORTE
# El objetivo es obtener la latitud y longitud para poder meterla en dos campos
# Al estar en un diccionario, hacemos una función que extraiga el valor de lat y lon
def separator_longitud_json(column):
    for i in column:
        return column["longitude"]
def separator_latitud_json(column):
    for i in column:
        return column["latitude"]

# Diseñamos una función que extraiga el valor de address de un diccionario
def address_extractor (column):
    for i in column:
        return column["street-address"]
    

# Limpiamos el dataset de deporte y nos quedamos con las variables útiles
def deporte_clean (df, function, fields):
    df["address_final"] = df.apply(lambda row: function(row["address"]), axis = 1)
    df_clean = df[fields]
    return df_clean