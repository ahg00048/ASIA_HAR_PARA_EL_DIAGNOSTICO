import core.fuzzy.fuzzySystem_utils as fs_utils  
from core.ahp.alternatives_data_params import *

class FuzzyCriteria:
    def __init__(self, crit, alternatives_params):
        self.crit = crit
        self.alternatives_params = alternatives_params
        self._fuzzy_system = fs_utils.create_fuzzySystem()
        self.addAlternativesParams()


    def addAlternativesParams(self):
        if len(self.alternatives_params) == 0:
            return

        terms = []
        for alt_p in self.alternatives_params:
            terms.append((alt_p.alt, alt_p.func))

        ling_var, self._terms = fs_utils.create_linguisticVariable(terms)
        self._fuzzy_system.add_linguistic_variable(self.crit, ling_var)


    def getMembershipValue(self, alt, value):
        fs_sets = self._fuzzy_system.get_fuzzy_sets(self.crit)

        for fs_set in fs_sets:
            if fs_set.get_term() == alt:
                return fs_set.get_value(value)
            
        return 0.0