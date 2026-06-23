from enum import Enum
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
INVALID_PATH = 'INVALID'

API_HOST = {
    'IP_ADDRESS' : '127.0.0.1',
    'PORT' : '8000',
    'ROOT_URL' : 'ASIA_HAR/api/',
    'URLs' : [
        'users/',
        'users/{0}/',
        'users/{0}/patients/',
        'users/{0}/patients/{1}/',
        'example/'
    ]
}

USERS_GET_POST: int = 0
USERS_DELETE_PUT: int = 1
PATIENTS_GET_POST: int = 2
PATIENTS_DELETE_PUT_GETDATA: int = 3
EXAMPLE: int = 4

# LOCAL

DATA = {
    'ROOT_DIR' : 'data/',
    'SUBDIR' : {
        'TEMP' : 'temp/',
        'PERSISTENT' : {
            'NAME' : 'persistent/',
# ========================================================================
            'CONFIG' : 'config.json',
            'CONFIG_BU' : 'config_backup.json',
# ========================================================================
            'CRIT_DATA' : 'save_crit.json',
            'CRIT_DATA_BU' : 'save_crit_backup.json',
            
            'CRIT_DATA_PARAMS' : 'save_crit_params.json',
            'CRIT_DATA_PARAMS_BU' : 'save_crit_params_backup.json',
            
            'ALT_DATA' : 'save_alt.json',
            'ALT_DATA_BU' : 'save_alt_backup.json',
            
            'ALT_DATA_PARAMS' : 'save_alt_params.json',
            'ALT_DATA_PARAMS_BU' : 'save_alt_params_backup.json',
            
            'TIME_DATA' : 'save_time_range.json',
            'TIME_DATA_BU' : 'save_time_range_backup.json',
# ========================================================================
            'CRIT_SET_NAME' : 'criteria',
            'CRIT_ALT_DATA_NAME' : 'name',
            'CRIT_ALT_DATA_REL_WEIGHT' : 'weight',
            'CRIT_ALT_DATA_REL_CRIT' : 'crit',
            'CRIT_DATA_REL' : 'criteria_relations',

            'CRIT_PARAM_SET_NAME' : 'criteria_data_params',
            'CRIT_PARAM_DATA_PARAM' : 'param',
            'CRIT_PARAM_DATA_METHOD' : 'method',

            'ALT_SET_NAME' : 'alternatives',
            'ALT_DATA_REL_ALT' : 'alt',
            'ALT_DATA_REL' : 'alternatives_relations',

            'ALT_PARAM_SET_NAME' : 'alternatives_data_params',
            'ALT_PARAM_DATA_FUNC' : 'trap_func',

            'TIME_START' : 'time_start',
            'TIME_RANGE' : 'time_range',
# ========================================================================
            'DFS_EXCLUDE' : 'dfs_exclude_properties'

        }
    }
}