from config import * 
import os
import pandas as pd
import numpy as np
import requests
import math
from zipfile import ZipFile


path_data_temp = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['TEMP']
path_data_persist = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['PERSISTENT']

url_api_root = 'http://' + API_HOST['IP_ADDRESS'] + ':' + API_HOST['PORT']  + '/' + API_HOST['ROOT_URL']

url_users_get_post = API_HOST['URLs'][USERS_GET_POST]
url_users_del_put = API_HOST['URLs'][USERS_DELETE_PUT]
url_patients_get_post = API_HOST['URLs'][PATIENTS_GET_POST]
url_patients_del_put_getData = API_HOST['URLs'][PATIENTS_DELETE_PUT_GETDATA]
url_example = API_HOST['URLs'][EXAMPLE]


'''
===============================================================
|                         temp data                           |
===============================================================
'''

# Obtiene el zip dado una url de la api y su id de hogar, y lo almacena en temp
def retrieveRemoteData_Zip(url, house_id):
    response = requests.get(url, stream=True)
    
    if response.status_code == requests.status_codes._codes[204]:
        return INVALID_PATH

    zip_filename = path_data_temp / 'house_{0}.zip'.format(house_id)

    with open(zip_filename, 'wb') as zip_file:
        for chunk in response.iter_content(chunk_size=255): 
            if chunk:
                zip_file.write(chunk)

    return zip_filename


# Obtiene el los archivos csv del zip en el sistema de archivos local
def retrieveDataFrames_Zip(path):
    zip_f = ZipFile(path)

    data_frames = {text_file.filename : pd.read_csv(zip_f.open(text_file.filename)) 
            for text_file in zip_f.infolist() if text_file.filename.endswith('.csv')}

    return data_frames


# Eliminar el zip descargado con la api
def removeLocalData(path):
    if not os.path.exists(path) or path == INVALID_PATH:
        return

    os.remove(path)


'''
===============================================================
|                     persistent data                         |
===============================================================
'''

def retrieveLocalData(path):
    pass


def saveData(path, data):
    pass


'''
===============================================================
|               Obtaining values with dfs                     |
===============================================================
'''

def dataFrames_min_max(dfs: pd.DataFrame, property: str) -> tuple:
    min = float('inf')
    max = float('-inf')

    try:
        for (idx, row) in dfs.iterrows():
            value = row.loc[property]
            if value < min:
                min = value
            if value > max:
                max = value
    except KeyError:
        return None

    return (min, max)


def dataFrames_max(dfs: pd.DataFrame, property: str):
    max = float('-inf')

    try:
        for (idx, row) in dfs.iterrows():
            value = row.loc[property]
            if value > max:
                max = value
    except KeyError:
        return None

    return max


def dataFrames_min(dfs: pd.DataFrame, property: str):
    min = float('-inf')

    try:
        for (idx, row) in dfs.iterrows():
            value = row.loc[property]
            if value < min:
                min = value
    except KeyError:
        return None

    return min


def dataFrames_sum(dfs: pd.DataFrame, property: str):
    sum = 0.0

    try:
        for (idx, row) in dfs.iterrows():
            sum += row.loc[property]
    except KeyError:
        return None

    return sum


def dataFrames_mean(dfs: pd.DataFrame, property: str):
    sum = 0.0
    
    try:
        for (idx, row) in dfs.iterrows():
            sum += row.loc[property]
    except KeyError:
        return None

    return sum / len(dfs.index)


def dataFrames_list(dfs: pd.DataFrame, property: str):
    values = []
    
    try:
        for (idx, row) in dfs.iterrows():
            values.append(row.loc[property])
    except KeyError:
        return None

    return values

'''
========================================================================================
'''


# Obtiene los datos de ejemplo
def retrieveDataExample():
    house_id = 2
    url = url_api_root + url_example + '?house_id={0}&time_range_in_seconds={1}'
    url = url.format(house_id, 86400)
    print(url)

    zip_filename = retrieveRemoteData_Zip(url, house_id)

    dfs = retrieveDataFrames_Zip(zip_filename)
    for dfk in dfs.keys():
        print(dataFrames_min_max(dfs[dfk], 'humidity'))
        print(dataFrames_mean(dfs[dfk], 'pressure'))
        print(dataFrames_sum(dfs[dfk], 'temperature'))
        print()

    removeLocalData(zip_filename)   

if __name__ == '__main__':
    retrieveDataExample()