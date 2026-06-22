import asyncio

from core import ahp_analysis, criteria
from core import alternative
import core.dataframe_utils as dtf_utils
import core.dataManager as dm

class mainModel():
    def __init__(self):
        time_tuple = dm.get_time()
        
        self._criteria = dm.get_all_crit()
        self._alternatives = dm.get_all_alt(self._criteria)
        
        self._timeStart = time_tuple[0]
        self._timeRange = time_tuple[1]
        
        self._dataFrames = None
        self._task_dfs = None
        self._loadingDFs = False

        self._unableToConnectToServer = False

# Alts and Crit

    def getCriteria(self):
        return self._criteria.copy()

    def getAlternatives(self):
        return self._alternatives.copy()

    def updateCriteria(self, criteria):
        self._criteria = criteria

    def saveCriteria(self):
        dm.save_all_crit(self._criteria)

    def updateAlternatives(self, alternatives):
        self._alternative = alternatives

    def saveAlternatives(self):
        dm.save_all_alt(self._alternatives)

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

    def getDfsValidProperties():
        excludedProps = dm.get_config_dfs_excludedParameters()
        
        return [ x for x in dtf_utils.dataFrames_properties() if x not in excludedProps ]