class Criteria_rel:
    weight = 1
    crit = None

    def __init__(self, crit, weight):
        self.weight = weight
        self.crit = crit

    def __init__(self, crit):
        self.weight = 1
        self.crit = crit

    def __str__(self):
        return "{0} -> {1}".format(self.weight, self.crit.name)

# criteria ---------------------------------------------------

class Criteria:
    name = ""
    __criteria_relations = []

    def __init__(self, name):
        self.name = name
        self.__criteria_relations.append(Criteria_rel(self))

# añadir relaciones entre criterios

    def addCriteriaRel_CritRel(self, crit_rel):
        if self.__criteria_relations.count(crit_rel) == 0:
            self.__criteria_relations.append(crit_rel)

    def addCriteriaRel_Crit(self, crit, weight):
        if not any(rel.crit == crit for rel in self.__criteria_relations):
            self.__criteria_relations.append(Criteria_rel(crit, weight))

# Eliminar relaciones entre criterios

    def rmCriteriaRel_CritRel(self, crit_rel):
        if self.__criteria_relations.count(crit_rel) != 0:
            self.__criteria_relations.remove(crit_rel)
        
    def rmCriteriaRel_Crit(self, crit):
        for rel in self.__criteria_relations:
            if rel.crit == crit:
                self.__criteria_relations.remove(rel)

# Obtener relaciones entre criterios

    def getCriteriaRels(self):
        return self.__criteria_relations.copy()

# Obtener pesos

    def getTotalWeight(self):
        weight = 0.0
        for rel in self.__criteria_relations:
            weight += rel.weight
        return weight

    def getCritWeight_Crit(self, crit):
        for rel in self.__criteria_relations:
            if rel.crit == crit:
                return rel.weight
            
    def getCritWeight_Name(self, critName):
        for rel in self.__criteria_relations:
            if rel.crit.name == critName:
                return rel.weight

    def __str__(self):
        return "Criteria {0} -> Weights: {1}".format(self.name, self.__criteria_relations)

    def __eq__(self, value):
        return self.name == value.name

# funciones

def relateCriterias(crit_one: Criteria, crit_two: Criteria, w_two_by_one: float):
    crit_one.addCriteriaRel_Crit(crit_two, w_two_by_one)
    crit_two.addCriteriaRel_Crit(crit_one, 1 / w_two_by_one)

def unrelateCriterias(crit_one: Criteria, crit_two: Criteria):
    crit_one.rmCriteriaRel_Crit(crit_two)
    crit_two.rmCriteriaRel_Crit(crit_one)