from .settings import *
import os
import zlib
import zipfile

def retrieveDataPathsFromHouseID(house_id):
    pass

def retrieveDataPathsFromHouseID_Test(house_id):
    dataRootDir = DATASETS_TEST['DIR']
    dataSubDirs = DATASETS_TEST['SUBDIRS_FORMAT'] 
    dataFilesFormat = DATASETS_TEST['FILES_FORMAT'] # list

    path_formated = "%s/%s{0}/{1}{0}.{2}" % (dataRootDir, dataSubDirs) 
    validPaths = []

    for dataFileFormat in dataFilesFormat:
        filePath = path_formated.format(house_id, dataFileFormat, DATASETS_FILE_EXTENSION)
        if os.path.exists(filePath):
            validPaths.append(filePath)

    print(validPaths)

    return validPaths


def compressFiles(filePaths, house_id):
    dataRootDir = DATASETS_TEST['DIR']
    dataSubDirs = DATASETS_TEST['SUBDIRS_FORMAT'] 
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs) 

    compression = zipfile.ZIP_DEFLATED
    # create the zip file first parameter path/name, second mode
    zf = zipfile.ZipFile(zip_name.format(house_id), mode="w")
    try:
        for file_name in filePaths:
            zf.write(file_name, file_name.split("/")[-1], compress_type=compression)

    except FileNotFoundError:
        print("Unable to compress file")
    finally:
        zf.close()


def isDataCompressed(house_id):
    dataRootDir = DATASETS_TEST['DIR']
    dataSubDirs = DATASETS_TEST['SUBDIRS_FORMAT'] 
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs) 

    return os.path.exists(zip_name.format(house_id))
    

def getCompressedDataPath(house_id):
    dataRootDir = DATASETS_TEST['DIR']
    dataSubDirs = DATASETS_TEST['SUBDIRS_FORMAT'] 
    zip_name = "%s/%s{0}/%s{0}.zip" %  (dataRootDir, dataSubDirs, dataSubDirs)

    return zip_name.format(house_id) 