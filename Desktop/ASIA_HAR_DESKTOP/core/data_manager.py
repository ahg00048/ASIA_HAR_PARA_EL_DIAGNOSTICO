from config import * 
from serializer_utils import *
import os
import pandas as pd
import requests
from zipfile import ZipFile


path_data_temp = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['TEMP']
path_data_persist = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['PERSISTENT']['NAME']

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

data_persistence = DATA['SUBDIR']['PERSISTENT']

crit_data = data_persistence['CRIT_DATA']
crit_data_bu = data_persistence['CRIT_DATA_BU']
alt_data = data_persistence['ALT_DATA']
alt_data_bu = data_persistence['ALT_DATA_BU']

_all_name = data_persistence['CRIT_ALT_DATA_NAME']
_all_weight = data_persistence['CRIT_ALT_DATA_REL_WEIGHT']
_all_rel_crit = data_persistence['CRIT_ALT_DATA_REL_CRIT']

_crit_rel = data_persistence['CRIT_DATA_REL']

_alt_rel_alt = data_persistence['ALT_DATA_REL_ALT']
_alt_rel = data_persistence['ALT_DATA_REL']


#=================================================================

def get_all_crit(backup = False):
    criteria_aux = []

    data_path = (crit_data if not backup else crit_data_bu)
    with open(path_data_persist / data_path) as f:
        f_content = f.read()
        criteria_aux = crit_list_from_json(f_content)

    criteria = [ t[0] for t in criteria_aux ]
    
    for i in range(len(criteria_aux)):
        curr_crit = criteria[i]
        curr_crit.addCriteriaRel_Self()
        curr_crit_rel = criteria_aux[i][1]

        for rel in curr_crit_rel:
            for j in range(len(criteria)):
                if rel[_all_rel_crit] == criteria[j].name and not curr_crit.hasCriteriaInRels(criteria[j]):
                    relateCriterias(curr_crit, criteria[j], rel[_all_weight])
                    break

    return criteria


def save_all_crit(criteria: list[Criteria], backup = False):
    file_content = crit_list_to_json(criteria)

    data_path = (crit_data if not backup else crit_data_bu)
    with open(path_data_persist / data_path, "w") as f:
        f.write(file_content)


#=================================================================

def get_all_alt(criteria: list[Criteria], backup = False):
    alternatives_aux = []

    data_path = (alt_data if not backup else alt_data_bu)
    with open(path_data_persist / data_path) as f:
        f_content = f.read()
        alternatives_aux = alt_list_from_json(f_content)

    alternatives = [ t[0] for t in alternatives_aux ]
    
    for i in range(len(alternatives_aux)):
        curr_alt = alternatives[i]
        curr_alt_rel = alternatives_aux[i][1]

        for crit in criteria:
            curr_alt.addAlternativeRel_Self(crit)

        curr_crit = None
        for rel in curr_alt_rel:
            for crit in criteria:
                if crit.name == rel[_all_rel_crit]:
                    curr_crit = crit

            for j in range(len(alternatives)):
                if rel[_alt_rel_alt] == alternatives[j].name and not curr_alt.hasAlternativeInRels(curr_crit, alternatives[j]):
                    relateAlternatives(curr_crit, curr_alt, alternatives[j], rel[_all_weight])
                    break

    return alternatives


def save_all_alt(alternatives: list[Alternative], backup = False):
    file_content = alt_list_to_json(alternatives)

    data_path = (alt_data if not backup else alt_data_bu)
    with open(path_data_persist / data_path, "w") as f:
        f.write(file_content)


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

    removeLocalData(zip_filename)   