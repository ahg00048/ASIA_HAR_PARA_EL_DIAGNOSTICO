from core.ahp.criteria import *

class Alternative_rel:
    weight = 1
    df_id = 0
    crit = None
    alt = None

    def __init__(self, crit, alt, df_id = 0, weight = 1):
        self.weight = weight
        self.crit = crit
        self.alt = alt
        self.df_id = df_id

    def __str__(self):
        return "Criteria {0}: {1} -> {2}".format(self.crit.name, self.weight, self.alt.name)

# alternative ---------------------------------------------------

class Alternative:
    name = ""

    def __init__(self, name):
        self._alternative_relations = list() 
        self.name = name

# añadir relaciones entre criterios

    def addAlternativeRel_Self(self, crit, df_id):
        if not any((rel.alt == self and rel.crit == crit) for rel in self._alternative_relations):
            self._alternative_relations.append(Alternative_rel(crit, self, df_id))

    def addAlternativeRel_AltRel(self, alt_rel):
        if self._alternative_relations.count(alt_rel) == 0:
            self._alternative_relations.append(alt_rel)

    def addAlternativeRel_alt(self, crit, alt, df_id, weight):
        if not any((rel.alt == alt and rel.crit == crit and rel.df_id == df_id) for rel in self._alternative_relations):
            self._alternative_relations.append(Alternative_rel(crit, alt, df_id, weight))

# Eliminar relaciones entre criterios

    def rmAlternativeRel_AltRel(self, alt_rel):
        if self._alternative_relations.count(alt_rel) != 0:
            self._alternative_relations.remove(alt_rel)
        
    def rmAlternativeRel_alt(self, crit, alt, df_id):
        for rel in self._alternative_relations:
            if rel.alt == alt and rel.crit == crit and rel.df_id == df_id:
                self._alternative_relations.remove(rel)

# Obtener relaciones entre criterios

    def getAlternativeRels(self):
        return self._alternative_relations.copy()

    def hasAlternativeInRels(self, crit, alt, df_id):
        for rel in self._alternative_relations:
            if rel.crit == crit and rel.alt == alt and rel.df_id == df_id:
                return True
        return False
# Obtener pesos

    def getTotalWeight_Crit(self, crit, df_id):
        weight = 0.0
        for rel in self._alternative_relations:
            if rel.crit == crit and rel.df_id == df_id:
                weight += rel.weight
        return weight

    def getAltWeight_Crit_Alt(self, crit, alt, df_id):
        for rel in self._alternative_relations:
            if rel.crit == crit and rel.alt == alt and rel.df_id == df_id:
                return rel.weight
            
    def getAltWeight_Name(self, critName, altName, df_id):
        for rel in self._alternative_relations:
            if rel.crit.name == critName and rel.alt.name == altName and rel.df_id == df_id:
                return rel.weight

    def __str__(self):
        return "Alternative {0} -> Weights: {1}".format(self.name, self._alternative_relations)

    def __eq__(self, value):
        return self.name == value.name

# funciones

def relateAlternatives(crit: Criteria, alt_one: Alternative, alt_two: Alternative, df_id: int, w_two_by_one: float):
    alt_one.addAlternativeRel_alt(crit, alt_two, df_id, w_two_by_one)
    alt_two.addAlternativeRel_alt(crit, alt_one, df_id, 1 / w_two_by_one)

def alterAlternativesWeight(crit: Criteria, alt_one: Alternative, alt_two: Alternative, df_id: int, w_two_by_one: float):
    for alt_rel in alt_one._alternative_relations:
        if alt_rel.alt == alt_two and alt_rel.crit == crit and alt_rel.df_id == df_id:
            alt_rel.weight = w_two_by_one
    for alt_rel in alt_two._alternative_relations:
        if alt_rel.alt == alt_one and alt_rel.crit == crit and alt_rel.df_id == df_id:
            alt_rel.weight = (1 / w_two_by_one)

def unrelateAlternatives(crit: Criteria, alt_one: Alternative, alt_two: Alternative, df_id: int):
    alt_one.rmAlternativeRel_alt(crit, alt_two, df_id)
    alt_two.rmAlternativeRel_alt(crit, alt_one, df_id)