from ASIA_HAR_DESKTOP.core import ahp_analysis, criteria
from ASIA_HAR_DESKTOP.core import alternative
import ASIA_HAR_DESKTOP.core.data_manager.data_manager as dm

class Crit_Alt():
    def __init__(self):
        self._criteria = dm.all_crit()
        self._alternatives = dm.all_alt()
        self.initCriteriaAlternatives()


    def initCriteriaAlternatives(self):
        for i in range(len(self._criteria)):
            for j in range(i + 1, len(self._criteria)):
                criteria.relateCriterias(self._criteria[i], self._criteria[j], 1.0)
                
        for i in range(len(self._alternatives)):
            for j in range(i + 1, len(self._alternatives)):
                criteria.relateCriterias(self._alternatives[i], self._alternatives[j], 1.0)

    
    def getCriteria(self):
        return self.criteria.values()


    def getAlternatives(self):
        return self.criteria.values()