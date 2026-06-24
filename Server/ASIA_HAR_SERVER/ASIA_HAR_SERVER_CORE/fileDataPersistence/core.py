from .settings import *
import os
import shutil
import zlib
import zipfile
import pandas as pd
import numpy as np


def removeFiles(filePaths):
    for file in filePaths:
        if os.path.isfile(file):
            os.remove(file)
        else:
            shutil.rmtree(file)

    filePaths.clear()


def compressFiles(filePaths, house_id, dataRootDir, dataSubDirs):
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs) 

    compression = zipfile.ZIP_DEFLATED
    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(zip_name.format(house_id), mode="w")
    try:
        for file_name in filePaths:
            zf.write(file_name, file_name.split("/")[-1], compress_type=compression)
    except FileNotFoundError:
        raise Exception
    finally:
        zf.close()


def isDataCompressed(house_id, dataRootDir, dataSubDirs):
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs) 

    return os.path.exists(zip_name.format(house_id))
    

def getCompressedDataPath(house_id, dataRootDir, dataSubDirs):
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs)

    return zip_name.format(house_id) 


# Obtiene el los archivos csv del zip en el sistema de archivos local
def retrieveDataFrames(path):
    zip_f = zipfile.ZipFile(path)

    data_frames = {text_file.filename : pd.read_csv(zip_f.open(text_file.filename)) 
            for text_file in zip_f.infolist() if text_file.filename.endswith('.csv')}

    return data_frames


# Recorta los archovos de los sensores para que se encuentren en el margen mas reciente de tiempo dado
def cullDataFromTimeRange(data_frames, time_start_in_seconds, time_range_in_seconds):
    col_label = 'timestamp'
    new_data_frames = {}
    
    for key in data_frames.keys():
        df = data_frames[key]

        # Search begin
        begin_index = 0
        end_index = len(df.index)
        while begin_index < end_index:
            mid_index = (end_index + begin_index) // 2
            
            if mid_index == end_index or mid_index == begin_index:
                break

            if float(df.at[mid_index, col_label]) <= time_start_in_seconds:
                begin_index = mid_index
            else:
                end_index = mid_index
                
        init_index = mid_index;

        time_end_in_seconds = time_start_in_seconds + time_range_in_seconds

        # Search end
        begin_index = 0
        end_index = len(df.index)
        while begin_index < end_index:
            mid_index = (end_index + begin_index) // 2
            
            if mid_index == end_index or mid_index == begin_index:
                break

            if int(df.at[mid_index, col_label]) <= time_end_in_seconds:
                begin_index = mid_index
            else:
                end_index = mid_index
        
        final_index = mid_index

        new_df = df.drop(index=df.index[:init_index], inplace=False)
        new_df.drop(index=df.index[final_index:], inplace=True)

        new_data_frames[key] = new_df

    return new_data_frames


def makeZipFromDataFrames(data_frames, path, subdir_format, house_id):
    if not os.path.exists(path):
        os.makedirs(path)
        
    zip_path = path + subdir_format + '{0}.zip'.format(house_id)
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        i = 1 
        for key in data_frames.keys():
            df = data_frames[key]

            df.to_csv(key) 
            zf.write(key) 
            os.remove(key)  
            i += 1

    return zip_path


# Public =================================================================0

def retrieveData_Test(house_id: int, time_start_in_seconds, time_range_in_seconds):
    dataRootDir = DATASETS_TEST['DIR']
    dataSubDirs = DATASETS_TEST['SUBDIRS_FORMAT'] 
    dataFilesFormat = DATASETS_TEST['FILES_FORMAT'] # list

    path_format = "%s/%s{0}/{1}{0}.{2}" % (dataRootDir, dataSubDirs) 
    validPaths = []

    for dataFileFormat in dataFilesFormat:
        filePath = path_format.format(house_id, dataFileFormat, DATASETS_FILE_EXTENSION)
        if os.path.exists(filePath):
            validPaths.append(filePath)

    if validPaths.count == 0:
        raise FileExistsError()
    
    if not isDataCompressed(house_id, dataRootDir, dataSubDirs):
        compressFiles(validPaths, house_id, dataRootDir, dataSubDirs)

    dataPath = getCompressedDataPath(house_id, dataRootDir, dataSubDirs)
    dfs = retrieveDataFrames(dataPath)
    dfs = cullDataFromTimeRange(dfs, time_start_in_seconds, time_range_in_seconds)

    path_format = "%s/%s{0}/%s/" % (dataRootDir, dataSubDirs, TEMP_DIR)
    resultPath = makeZipFromDataFrames(dfs, path_format.format(house_id), dataSubDirs, house_id)

    return resultPath