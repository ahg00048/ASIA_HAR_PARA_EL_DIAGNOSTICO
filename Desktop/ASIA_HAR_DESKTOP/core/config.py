import sys
from enum import Enum
from pathlib import Path


if getattr(sys, 'frozen', False):
    _BASE_DIR = Path(sys._MEIPASS)          # recursos de solo lectura
    _DATA_ROOT = Path.home() / "AppData" / "Roaming" / "ASIA_HAR_DESKTOP"
else:
    _BASE_DIR = Path(__file__).resolve().parent.parent
    _DATA_ROOT = _BASE_DIR

RESOURCES_DIR = _BASE_DIR / "ui" / "resources"

DATA_DIR = _DATA_ROOT / "data"
TEMP_DIR = DATA_DIR / "temp"
PERSISTENT_DIR = DATA_DIR / "persistent"

TEMP_DIR.mkdir(parents=True, exist_ok=True)
PERSISTENT_DIR.mkdir(parents=True, exist_ok=True)

if getattr(sys, 'frozen', False) and not any(PERSISTENT_DIR.iterdir()):
    import shutil
    _default_persist = _BASE_DIR / "data" / "persistent"
    if _default_persist.exists():
        shutil.copytree(_default_persist, PERSISTENT_DIR, dirs_exist_ok=True)


BASE_DIR = _BASE_DIR
INVALID_PATH = 'INVALID'

API_HOST = {
    'IP_ADDRESS': '127.0.0.1',
    'PORT': '8000',
    'ROOT_URL': 'ASIA_HAR/api/',
    'URLs': [
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


DATA = {
    'ROOT_DIR': str(DATA_DIR),  
    'SUBDIR': {
        'TEMP': str(TEMP_DIR),
        'PERSISTENT': {
            'NAME': str(PERSISTENT_DIR),
            'CONFIG': 'config.json',
            'CONFIG_BU': 'config_backup.json',
            'CRIT_DATA': 'save_crit.json',
            'CRIT_DATA_BU': 'save_crit_backup.json',
            'CRIT_DATA_PARAMS': 'save_crit_params.json',
            'CRIT_DATA_PARAMS_BU': 'save_crit_params_backup.json',
            'ALT_DATA': 'save_alt.json',
            'ALT_DATA_BU': 'save_alt_backup.json',
            'ALT_DATA_PARAMS': 'save_alt_params.json',
            'ALT_DATA_PARAMS_BU': 'save_alt_params_backup.json',
            'TIME_DATA': 'save_time_range.json',
            'TIME_DATA_BU': 'save_time_range_backup.json',
            'CRIT_SET_NAME': 'criteria',
            'CRIT_ALT_DATA_NAME': 'name',
            'CRIT_ALT_DATA_REL_WEIGHT': 'weight',
            'CRIT_ALT_DATA_REL_CRIT': 'crit',
            'CRIT_DATA_REL': 'criteria_relations',
            'CRIT_PARAM_SET_NAME': 'criteria_data_params',
            'CRIT_PARAM_DATA_PARAM': 'param',
            'CRIT_PARAM_DATA_METHOD': 'method',
            'ALT_SET_NAME': 'alternatives',
            'ALT_DATA_REL_ALT': 'alt',
            'ALT_DATA_REL': 'alternatives_relations',
            'ALT_PARAM_SET_NAME': 'alternatives_data_params',
            'ALT_PARAM_DATA_FUNC': 'trap_func',
            'TIME_START': 'time_start',
            'TIME_RANGE': 'time_range',
            'DFS_EXCLUDE': 'dfs_exclude_properties'
        }
    }
}