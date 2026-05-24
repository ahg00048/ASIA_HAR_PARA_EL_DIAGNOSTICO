from ASIA_HAR_DESKTOP.core.config import * 
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
def retrieveLocalData_Zip(path):
    zip_f = ZipFile(path)

    data_frames = {text_file.filename : pd.read_csv(zip_f.open(text_file.filename)) 
            for text_file in zip_f.infolist() if text_file.filename.endswith('.csv')}

    print(data_frames)
    return data_frames


# Eliminar el zip descargado con la api
def removeLocalData(path):
    if not os.path.exists(path) or path == INVALID_PATH:
        return

    os.remove(path)


# Obtiene los datos de ejemplo
def retrieveDataExample():
    house_id = 2
    url = url_api_root + url_example + '?house_id={0}&time_range_in_seconds={1}'
    url = url.format(house_id, 86400)

    zip_filename = retrieveRemoteData_Zip(url, house_id)
    print(zip_filename)
    dfs = retrieveLocalData_Zip(zip_filename)
    removeLocalData(zip_filename)   