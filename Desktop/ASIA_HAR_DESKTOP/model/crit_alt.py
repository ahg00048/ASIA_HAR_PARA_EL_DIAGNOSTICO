from core import ahp_analysis, criteria
from core import alternative
import core.dataManager as dm

class mainModel():
    def __init__(self):
        self._criteria = dm.get_all_crit()
        self._alternatives = dm.get_all_alt(self._criteria)
        self._timeStart = 0.0
        self._timeRange = 0.0    

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

    def setTime(self, start, end):
        self._timeStart = start
        self._timeRange = end - start

    def getTime(self):
        return (self._timeStart, self._timeRange)