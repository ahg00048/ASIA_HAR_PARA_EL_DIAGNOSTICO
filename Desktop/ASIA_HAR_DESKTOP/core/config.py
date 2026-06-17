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
            'CRIT_ALT_DATA' : 'base_crit_alt.json',
            'CRIT_ALT_DATA_BU' : 'base_crit_alt_backup.json'
        }
    }
}