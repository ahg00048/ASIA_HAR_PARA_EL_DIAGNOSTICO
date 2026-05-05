from criteria import *

class alternative_rel:
    weight = 1
    crit = None
    alt = None

    def __init__(self, crit, alt, weight):
        self.weight = weight
        self.crit = crit
        self.alt = alt

    def __init__(self, crit, alt):
        self.weight = 1
        self.crit = crit
        self.alt = alt

    def __str__(self):
        return "Criteria {0}: {1} -> {2}".format(self.crit.name, self.weight, self.alt.name)

# alternative ---------------------------------------------------

class alternative:
    name = ""
    __alternative_relations = []

    def __init__(self, name):
        self.name = name

# añadir relaciones entre criterios

    def addAlternativeRel_Self(self, crit):
        if not any((rel.alt == self and rel.crit == crit) for rel in self.__alternative_relations):
            self.__alternative_relations.append(alternative_rel(crit, self))

    def addAlternativeRel_AltRel(self, alt_rel):
        if self.__alternative_relations.count(alt_rel) == 0:
            self.__alternative_relations.append(alt_rel)

    def addAlternativeRel_alt(self, crit, alt, weight):
        if not any((rel.alt == alt and rel.crit == crit) for rel in self.__alternative_relations):
            self.__alternative_relations.append(alternative_rel(crit, alt, weight))

# Eliminar relaciones entre criterios

    def rmAlternativeRel_AltRel(self, alt_rel):
        if self.__alternative_relations.count(alt_rel) != 0:
            self.__alternative_relations.remove(alt_rel)
        
    def rmAlternativeRel_alt(self, alt):
        for rel in self.__alternative_relations:
            if rel.alt == alt:
                self.__alternative_relations.remove(rel)

# Obtener relaciones entre criterios

    def getAlternativeRels(self):
        return self.__alternative_relations.copy()

# Obtener pesos

    def getTotalWeight_Crit(self, crit):
        weight = 0.0
        for rel in self.__alternative_relations:
            if rel.crit == crit:
                weight += rel.weight
        return weight

    def getAltWeight_Crit_Alt(self, crit, alt):
        for rel in self.__alternative_relations:
            if rel.crit == crit and rel.alt == alt:
                return rel.weight
            
    def getAltWeight_Name(self, critName, altName):
        for rel in self.__alternative_relations:
            if rel.crit.name == critName and rel.alt.name == altName:
                return rel.weight

    def __str__(self):
        return "Alternative {0} -> Weights: {1}".format(self.name, self.__alternative_relations)

    def __eq__(self, value):
        return self.name == value.name

# funciones

def relateAlternatives(crit: criteria, alt_one: alternative, alt_two: alternative, w_two_by_one: float):
    alt_one.addAlternativeRel_alt(crit, alt_two, w_two_by_one)
    alt_two.addAlternativeRel_alt(crit, alt_one, 1 / w_two_by_one)

def unrelateAlternatives(crit: criteria, alt_one: alternative, alt_two: alternative):
    alt_one.rmAlternativeRel_alt(crit, alt_two)
    alt_two.rmAlternativeRel_alt(crit, alt_one, 1)