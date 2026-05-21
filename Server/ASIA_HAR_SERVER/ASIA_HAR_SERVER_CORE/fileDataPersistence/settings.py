from ASIA_HAR_SERVER.settings import BASE_DIR

DATASETS_FILE_EXTENSION = 'csv'
TEMP_DIR = 'temp'

DATASETS = {
    'DIR': BASE_DIR / 'ASIA_HAR_DATASETS_ROOT',
    'SUBDIRS_FORMAT': 'house_',
     'FILES_FORMAT': [ # data_{house_id}.extension
        'data_',
        'data_band_',
        'data_rssi_',
        'data_temp&humidity_',
    ]
}

DATASETS_TEST = {
    'DIR': BASE_DIR / 'ASIA_HAR_DATASETS_TEST',
    'SUBDIRS_FORMAT': 'house_', # house_{house_id}.extension
    'FILES_FORMAT': [ # data_{house_id}.extension
        'data_',
        'data_band_',
        'data_rssi_',
        'data_temp&humidity_',
    ]
}