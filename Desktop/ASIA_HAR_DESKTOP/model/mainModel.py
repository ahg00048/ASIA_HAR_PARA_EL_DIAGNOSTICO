import asyncio

import core.dataManagement.dataframe_utils as dtf_utils
import core.dataManagement.dataManager as dm

class mainModel():
    def __init__(self):
        time_tuple = dm.get_time()
        
        self._criteria = dm.get_all_crit()
        self._criteriaParams = dm.get_all_crit_data_param()
        self._alternatives = dm.get_all_alt(self._criteria)
        self._alternativesParams = dm.get_all_alt_data_param()

        self._timeStart = time_tuple[0]
        self._timeRange = time_tuple[1]
        self._timeInterval = time_tuple[2]
        
        self._version = 2
        self._house_id = 2

        self._dataFrames = None
        self._task_dfs = None
        self._loadingDFs = False
        self._unableToConnectToServer = False
        self._dataFrames_intervalList = [[]]

# Alts and Crit

    def getCriteria(self):
        return self._criteria.copy()

    def getCriteriaParams(self):
        return self._criteriaParams.copy()

    def getAlternatives(self):
        return self._alternatives.copy()
    
    def getAlternativesParams(self):
        return self._alternativesParams.copy()


    def updateCriteria(self, criteria):
        self._criteria = criteria

    def saveCriteria(self):
        dm.save_all_crit(self._criteria)


    def updateCriteriaParams(self, criteriaParams):
        self._criteriaParams = criteriaParams

    def saveCriteriaParams(self):
        dm.save_all_crit_data_param(self._criteriaParams)


    def updateAlternatives(self, alternatives):
        self._alternatives = alternatives

    def saveAlternatives(self):
        dm.save_all_alt(self._alternatives)

        
    def updateAlternativesParams(self, alternativesParams):
        self._alternativesParams = alternativesParams

    def saveAlternativesParams(self):
        dm.save_all_alt_data_param(self._alternativesParams)

# Time

    def setTime(self, start, end, interval):
        self._timeStart = start
        self._timeRange = end - start
        self._timeInterval = interval

    def getTime(self):
        return (self._timeStart, self._timeRange, self._timeInterval)

    def saveTime(self):
        dm.save_time(self._timeStart, self._timeRange, self._timeInterval)

# House and version

    def setHouseId(self, house_id):
        self._house_id = house_id

    def setVersion(self, version):
        self._version = version

    def writeResults(self, content):
        dm.write_results(self._version, self._house_id, content)

# Dataframes
    
    def getDataframes(self):
        if self._loadingDFs:
            return None
        return self._dataFrames

    def fetchDataframes(self):
        if self._loadingDFs:
            return 
        self._loadingDFs = True
        self._task_dfs = asyncio.ensure_future(self._fetchDataframes())

    async def _fetchDataframes(self):
        try:
            self._unableToConnectToServer = False
            self._dataFrames = await dm.retrieveDataExample(self._timeStart, self._timeRange, self._house_id, self._version)
        except Exception:
            self._unableToConnectToServer = True
        finally: 
            self._loadingDFs = False

    def errorObtainingDFs(self):
        return self._unableToConnectToServer

    def cancelDataframes(self):
        if self._task_dfs is None:
            return 
        self._task_dfs.cancel()
        self._loadingDFs = False
        self._dataFrames = None

    def getDfsValidProperties(self): 
        if self._dataFrames is None:
            return []

        excludedProps = dm.get_config_dfs_excludedParameters()
        validProps = []

        for df in self._dataFrames.values():
            df_props = dtf_utils.dataFrames_properties(df)
            for prop in df_props:
                if all(x not in prop for x in excludedProps) and prop not in validProps: 
                    validProps.append(prop)

        return validProps

    def getDfsMethods(self):
        return ["Media", "Max", "Min", "Suma"]
    
    def getDataframes_intervalList(self):
        if self._dataFrames is not None:
            max = 0
            data_list = []
            for df in self._dataFrames.values():
                dataFrame_interval = dtf_utils.dataFrames_split(df, self._timeInterval * 60)
                if max < len(dataFrame_interval):
                    max = len(dataFrame_interval)
                data_list.append(dataFrame_interval)

            self._dataFrames_intervalList = [[] for _ in range(max)]
            for i in range(max):
                for df_interval in data_list:
                    self._dataFrames_intervalList[i].append(df_interval[i] if i < len(df_interval) else dtf_utils.dataFrames_empty())

        return self._dataFrames_intervalList