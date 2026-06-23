from core.config import * 
from core.serializer_utils import *
import os
import pandas as pd
import requests
import asyncio
import aiohttp
import aiofiles
from zipfile import ZipFile


_path_data_temp = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['TEMP']
_path_data_persist = BASE_DIR / DATA['ROOT_DIR'] / DATA['SUBDIR']['PERSISTENT']['NAME']

_url_api_root = 'http://' + API_HOST['IP_ADDRESS'] + ':' + API_HOST['PORT']  + '/' + API_HOST['ROOT_URL']

_url_users_get_post = API_HOST['URLs'][USERS_GET_POST]
_url_users_del_put = API_HOST['URLs'][USERS_DELETE_PUT]
_url_patients_get_post = API_HOST['URLs'][PATIENTS_GET_POST]
_url_patients_del_put_getData = API_HOST['URLs'][PATIENTS_DELETE_PUT_GETDATA]
_url_example = API_HOST['URLs'][EXAMPLE]


'''
===============================================================
|                         temp data                           |
===============================================================
'''

# Obtiene el zip dado una url de la api y su id de hogar, y lo almacena en temp
async def retrieveRemoteData_Zip(url, house_id):    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 204:
                return INVALID_PATH

            zip_filename = _path_data_temp / 'house_{0}.zip'.format(house_id)

            async with aiofiles.open(zip_filename, 'wb') as zip_file:
                async for chunk in response.content.iter_chunked(255): 
                    await zip_file.write(chunk)

    return zip_filename


# Obtiene el los archivos csv del zip en el sistema de archivos local
def retrieveDataFrames_Zip(path):
    # with ZipFile(path) as zip_f:
    #     data_frames = {
    #         text_file.filename: pd.read_csv(zip_f.open(text_file.filename))
    #         for text_file in zip_f.infolist()
    #         if text_file.filename.endswith('.csv')
    #     }    
    with ZipFile(path) as zip_f:
        data_frames = {}
        for text_file in zip_f.infolist():
            if text_file.filename.endswith('.csv'):
                with zip_f.open(text_file) as csv_file:
                    data_frames[text_file.filename] = pd.read_csv(csv_file)

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

_data_persistence = DATA['SUBDIR']['PERSISTENT']

# config
_config = _data_persistence['CONFIG']
_config_bu = _data_persistence['CONFIG_BU']

_dfs_exclude = _data_persistence['DFS_EXCLUDE']

# crit and alt
_crit_data = _data_persistence['CRIT_DATA']
_crit_data_bu = _data_persistence['CRIT_DATA_BU']
_crit_data_params = _data_persistence['CRIT_DATA_PARAMS']
_crit_data_params_bu = _data_persistence['CRIT_DATA_PARAMS_BU']
_alt_data_params = _data_persistence['ALT_DATA_PARAMS']
_alt_data_params_bu = _data_persistence['ALT_DATA_PARAMS_BU']
_alt_data = _data_persistence['ALT_DATA']
_alt_data_bu = _data_persistence['ALT_DATA_BU']
_time_data = _data_persistence['TIME_DATA']
_time_data_bu = _data_persistence['TIME_DATA_BU']

_all_name = _data_persistence['CRIT_ALT_DATA_NAME']
_all_weight = _data_persistence['CRIT_ALT_DATA_REL_WEIGHT']
_all_rel_crit = _data_persistence['CRIT_ALT_DATA_REL_CRIT']

_crit_rel = _data_persistence['CRIT_DATA_REL']

_alt_param_set_name = _data_persistence['ALT_PARAM_SET_NAME']
_alt_param_func = _data_persistence['ALT_PARAM_DATA_FUNC']

_alt_rel_alt = _data_persistence['ALT_DATA_REL_ALT']
_alt_rel = _data_persistence['ALT_DATA_REL']

# time range
_time_start = _data_persistence['TIME_START']
_time_start = _data_persistence['TIME_RANGE']

#=================================================================

def get_all_crit(backup = False):
    criteria_aux = []

    data_path = (_crit_data if not backup else _crit_data_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return criteria_aux
    
    with f:
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

    data_path = (_crit_data if not backup else _crit_data_bu)

    try:
        f = open(_path_data_persist / data_path, "w")
    except OSError:
        return 
    
    with f:
        f.write(file_content)

#=================================================================

def get_all_crit_data_param(backup = False):
    criteria_p = [] 
    
    data_path = (_crit_data_params if not backup else _crit_data_params_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return criteria_p
    
    with f:
        f_content = f.read()
        criteria_p = crit_param_list_from_json(f_content)

    return criteria_p


def save_all_crit_data_param(criteria_p: list[CriteriaDataParams], backup = False):
    file_content = crit_param_list_to_json(criteria_p)

    data_path = (_crit_data_params if not backup else _crit_data_params_bu)

    try:
        f = open(_path_data_persist / data_path, "w")
    except OSError:
        return 
    
    with f:
        f.write(file_content)

#=================================================================

def get_all_alt(criteria: list[Criteria], backup = False):
    alternatives_aux = []

    data_path = (_alt_data if not backup else _alt_data_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return alternatives_aux

    with f:
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

    data_path = (_alt_data if not backup else _alt_data_bu)

    try:
        f = open(_path_data_persist / data_path, "w")
    except OSError:
        return 
    
    with f:
        f.write(file_content)

#=================================================================

def get_all_alt_data_param(backup = False):
    alternatives_p = [] 
    
    data_path = (_alt_data_params if not backup else _alt_data_params_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return alternatives_p
    
    with f:
        f_content = f.read()
        alternatives_p = alt_param_list_from_json(f_content)

    return alternatives_p


def save_all_alt_data_param(alternatives_p: list[CriteriaDataParams], backup = False):
    file_content = alt_param_list_to_json(alternatives_p)

    data_path = (_alt_data_params if not backup else _alt_data_params_bu)

    try:
        f = open(_path_data_persist / data_path, "w")
    except OSError:
        return 
    
    with f:
        f.write(file_content)


#=================================================================

def get_time(backup = False):
    data_path = (_time_data if not backup else _time_data_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return (0, 0)

    with f:
        f_content = f.read()
        time_tuple = time_from_json(f_content)

    return time_tuple


def save_time(time_start, time_range, backup = False):
    file_content = time_to_json(time_start, time_range)

    data_path = (_time_data if not backup else _time_data_bu)
    
    try:
        f = open(_path_data_persist / data_path, "w")
    except OSError:
        return

    with f:
        f.write(file_content)


#=================================================================


def get_config_dfs_excludedParameters(backup = False):
    data_path = (_config if not backup else _config_bu)

    try:
        f = open(_path_data_persist / data_path, "r")
    except OSError:
        return []
        
    with f:
        f_content = f.read()
        exclude_params = str_list_from_json(_dfs_exclude, f_content)

    return exclude_params



'''
========================================================================================
'''

# Obtiene los datos de ejemplo
async def retrieveDataExample(time_start, time_range):
    house_id = 2
    url = _url_api_root + _url_example + '?house_id={0}&time_start_in_seconds={1}&time_range_in_seconds={2}'
    url = url.format(house_id, time_start, time_range)

    # Ahora se espera correctamente el resultado asíncrono
    zip_filename = await retrieveRemoteData_Zip(url, house_id)

    if zip_filename == INVALID_PATH:
        raise Exception()

    dfs = retrieveDataFrames_Zip(zip_filename)
    
    removeLocalData(zip_filename)
    
    return dfs