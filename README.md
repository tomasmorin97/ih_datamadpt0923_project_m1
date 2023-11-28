
Step into the realm of sustainable mobility. In this exploration, we'll delve into two urban endeavors: Bicimad and Biciparkd. Our aim is to foster seamless communication between sports facilities and bike parks while comprehending the role these bicycle transportation alternatives play in enhancing our city's sustainability and the well-being of its residents.

Both initiatives present avant-garde solutions designed to promote bicycle usage as a viable mode of transport within urban landscapes.

## 🙋 Name
Bicimad & Bicipark Application

## 👶 Status
Ironhack Data Analytics Module 1 Project

## 🏃 One-liner
Embark on a journey through urban cycling with Bicimad & Bicipark Explorer, a project dedicated to the analysis and visualization of data from two leading bike-sharing initiatives.

## 💻 Technology stack
- import pandas as pd
- import requests
- import modules.extraction as ex
- import modules.analysis as an
- import modules.argparse as arg
- from shapely.geometry import Point
- import geopandas as gpd
- import argparse
- from fuzzywuzzy import process


## 💥 Core technical concepts and inspiration
Bicimad & Bicipark Explorer aims to offer a comprehensive snapshot of bicycle parking facilities around our sports centers, empowering users to compare the availability of Bicimad and Bicipark. The project is driven by the increasing significance of sustainable urban mobility and the demand for immediate access to relevant data.

Utilizing geolocation techniques, we ensure precise results tailored to the user's location. This enables the real-time identification and visualization of the closest sports facilities and bike stations.

Our implementation incorporates argparse and fuzzy matching algorithms to enhance search capabilities. These algorithms facilitate the discovery of approximate matches between text strings, simplifying the identification of locations, even in the presence of typos or naming variations.

## 🔧 Configuration
Requirements
- Python3 
- Pandas as pd
- Requests
- Numpy as np
- Fuzz and process from fuzzywuzzy

Prerequisites
- Python:
Bicimad & Bicipark Explorer is built using Python. Make sure you have Python installed on your system. You can download it from python.org.
- Pandas:
Bicimad & Bicipark Explorer relies on the Pandas library for data manipulation. Install it using the command:
```sh
pip install pandas
```
- FuzzyWuzzy:
FuzzyWuzzy is used for fuzzy string matching. Install it using the command:
```sh
pip install fuzzywuzzy
```
Installation Instructions:

- Clone the Repository:
Clone this repository to your local machine using the following command:
```sh
git clone [repository_url]
```
- Navigate to the Project Directory:
Change your working directory to the project folder:
``` sh
cd [project_folder]
```
- Install Dependencies:
Install the project dependencies by running the following command:
```sh
pip install -r requirements.txt
```
- Run the Application:
Execute the main script to run the Bicimad & Bicipark Explorer:
```sh
python script.py -t [type] -l [location]
```
## 🙈 Usage
Parameters
- Application: Choose between Bicimad or Bicipark.
- Location (optional): Specify a location to filter results using fuzzy matching.

Examples

Explore Bicimad:

```sh
python script.py -t BICIMAD
```
Explore Bicipark and filter by location "WiZink Center":

```sh
python script.py -t BICIPARK -l "WiZink Center"
```

## 📁 Folder Structure

└── __h_datamadpt0923_project_m1__
  
    ├── _wip_ 
    ├── modules
    ├   ── __pycache__
    │   └──  analysis.py
    |   └──  arg_parse.py
    |   └──  extraction.py
    ├── notebooks
    |    └── dev_notebook_ipynb
    ├── .gitignore
    ├── LICENSE
    ├── main.py
    ├── README
    ├──  __trash__
    ├──  data
        ├── bicimad_stations.csv
        └── bicipark_stations.csv
    ├──  output
        ├── bicimad_distance.csv
        └── bicipark_distance.csv

## 💩 ToDo
Implement fuzzy matching for better location filtering.

Handle additional user input. 

## ℹ️ Further Info

Credits:
- Open Data sources for Bicimad and Bicipark.
- Open data sources for sports centers 
