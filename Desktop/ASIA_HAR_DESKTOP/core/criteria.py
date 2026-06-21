class Criteria_rel:
    weight = 1
    crit = None

    def __init__(self, crit, weight = 1):
        self.weight = weight
        self.crit = crit

    def __str__(self):
        return "{0} -> {1}".format(self.weight, self.crit.name)

# criteria ---------------------------------------------------

class Criteria:
    name = ""

    def __init__(self, name):
        self.name = name
        self._criteria_relations = list()

# añadir relaciones entre criterios

    def addCriteriaRel_Self(self):
        if not any(rel.crit == self for rel in self._criteria_relations):
            self._criteria_relations.append(Criteria_rel(self))

    def addCriteriaRel_CritRel(self, crit_rel):
        if self._criteria_relations.count(crit_rel) == 0:
            self._criteria_relations.append(crit_rel)

    def addCriteriaRel_Crit(self, crit, weight):
        if not any(rel.crit == crit for rel in self._criteria_relations):
            self._criteria_relations.append(Criteria_rel(crit, weight))

# Eliminar relaciones entre criterios

    def rmCriteriaRel_CritRel(self, crit_rel):
        if self._criteria_relations.count(crit_rel) != 0:
            self._criteria_relations.remove(crit_rel)
        
    def rmCriteriaRel_Crit(self, crit):
        for rel in self._criteria_relations:
            if rel.crit == crit:
                self._criteria_relations.remove(rel)

# Obtener relaciones entre criterios

    def getCriteriaRels(self):
        return self._criteria_relations.copy()

    def hasCriteriaInRels(self, crit):
        for rel in self._criteria_relations:
            if rel.crit == crit:
                return True
        return False

# Obtener pesos

    def getTotalWeight(self):
        weight = 0.0
        for rel in self._criteria_relations:
            weight += rel.weight
        return weight

    def getCritWeight_Crit(self, crit):
        for rel in self._criteria_relations:
            if rel.crit == crit:
                return rel.weight
            
    def getCritWeight_Name(self, critName):
        for rel in self._criteria_relations:
            if rel.crit.name == critName:
                return rel.weight

    def __str__(self):
        return "Criteria {0} -> Weights: {1}".format(self.name, self._criteria_relations)

    def __eq__(self, value):
        return self.name == value.name

# funciones

def relateCriterias(crit_one: Criteria, crit_two: Criteria, w_two_by_one: float):
    crit_one.addCriteriaRel_Crit(crit_two, w_two_by_one)
    crit_two.addCriteriaRel_Crit(crit_one, 1 / w_two_by_one)

def alterCriteriasWeight(crit_one: Criteria, crit_two: Criteria, w_two_by_one: float):
    for crit_rel in crit_one._criteria_relations:
        if crit_rel.crit == crit_two:
            crit_rel.weight = w_two_by_one
    for crit_rel in crit_two._criteria_relations:
        if crit_rel.crit == crit_one:
            crit_rel.weight = (1 / w_two_by_one)

def unrelateCriterias(crit_one: Criteria, crit_two: Criteria):
    crit_one.rmCriteriaRel_Crit(crit_two)
    crit_two.rmCriteriaRel_Crit(crit_one)