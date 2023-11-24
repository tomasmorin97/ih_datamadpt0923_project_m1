# import library
import pandas as pd
import argparse
from fuzzywuzzy import process

# Cargar df

df_distancia_bicimad_min_res = pd.read_csv("./output/bicimad_distance.csv")
df_distancia_bicipark_min_res = pd.read_csv("./output/bicipark_distance.csv")

# Script functions 
# Argument parser function

def argument_parser():
    parser = argparse.ArgumentParser(description= 'Application to find the nearest location of a bicimad or bicipark from a sports spot' )
    help_message ='You have two options. Option 1: "bicimad" shows the entire dataframe or if you add any location,\
         it will show the nearest bicimad station from that spot. Option 2: "bicipark" shows the entire dataframe or if you add any location,\
         it will show the nearest bicimad station from that spot' 
    parser.add_argument('-t', '--type', help=help_message, type=str)
    parser.add_argument('-l', '--location', help=help_message, type=str)
    args = parser.parse_args()
    return args


# Pipeline execution
def funcion_arg_parse():
    bicimad_location = process.extractOne(argument_parser().location, list(df_distancia_bicimad_min_res["Sports spot"]))[0]
    bicipark_location = process.extractOne(argument_parser().location, list(df_distancia_bicipark_min_res["Sports spot"]))[0]
    bici_type = argument_parser().type
    if bici_type == 'bicimad':
        if bicimad_location != None:
            idx_bicimad = df_distancia_bicimad_min_res.index[df_distancia_bicimad_min_res["Sports spot"] == bicimad_location].tolist()[0]
            bicimad_station = df_distancia_bicimad_min_res.loc[idx_bicimad]
            return f'The nearest bicimad station from {bicimad_location} is {bicimad_station["BiciMAD spot"]} ({bicimad_station["Address BiciMAD"]}) and the number of available bikes are {bicimad_station["Available bikes"]}.'
        else:
            return df_distancia_bicimad_min_res
    elif bici_type == 'bicipark':
        if bicipark_location != None:
            idx_bicipark = df_distancia_bicipark_min_res.index[df_distancia_bicipark_min_res["Sports spot"] == bicipark_location].tolist()[0]
            bicipark_station = df_distancia_bicipark_min_res.loc[idx_bicipark]
            return f'The nearest bicimad station from {bicipark_location} is {bicipark_station["BiciPark spot"]} ({bicipark_station["Address BiciPark"]}) and the number of available bikes are {bicipark_station["Available bikes"]}.'
        else:
            return df_distancia_bicipark_min_res
    
