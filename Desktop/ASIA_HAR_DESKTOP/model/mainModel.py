import asyncio

from core import ahp_analysis, criteria, alternative, criteria_data_params
import core.dataframe_utils as dtf_utils
import core.dataManager as dm

class mainModel():
    def __init__(self):
        time_tuple = dm.get_time()
        
        self._criteria = dm.get_all_crit()
        self._criteriaParams = dm.get_all_crit_data_param()
        self._alternatives = dm.get_all_alt(self._criteria)
        self._alternativesParams = dm.get_all_alt_data_param()

        self._timeStart = time_tuple[0]
        self._timeRange = time_tuple[1]
        
        self._dataFrames = None
        self._task_dfs = None
        self._loadingDFs = False
        self._unableToConnectToServer = False

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

    def setTime(self, start, end):
        self._timeStart = start
        self._timeRange = end - start

    def getTime(self):
        return (self._timeStart, self._timeRange)

    def saveTime(self):
        dm.save_time(self._timeStart, self._timeRange)

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
            self._dataFrames = await dm.retrieveDataExample(self._timeStart, self._timeRange)
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