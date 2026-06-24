from core.ahp.alternative import *
from core.ahp.criteria import *

RANDOM_INDEX = [0, 0, 0.58, 0.89, 1.11, 1.24, 1.32, 1.4, 1.45, 1.49]
VALID_UPPER_BOUND_CONSISTENCY_RELATION = 0.10

'''
    C1  C2  C3
C1  p1  p4  p7  pt1
C2  p2  p5  p8  pt2
C3  p3  p6  99  pt3
    x1  x2  x3
'''

# calcular indice de consistencia para la matriz de criterios (tambien calcula las sumas y sus pesos)
def calculate_CI(criteria_list: list[Criteria], sums: list[float], weights: list[float]) -> float:
    n_criteria = len(criteria_list)
    consistency_index = 0.0
    sums = []
    weights = []

    # Obtenemos las sumas de la matriz
    for crit_one in criteria_list:
        sum = 0.0
        for crit_two in criteria_list:
            sum += crit_two.getCritWeight_Crit(crit_one)
        sums.append(sum)

    # Obtenemos los pesos de la matriz
    for crit_one in criteria_list:
        sum = 0.0
        for i in range(n_criteria):
            num = crit_one.getCritWeight_Crit(criteria_list[i])
            denom = sums[i]
            sum += (num / denom)
        weights.append(sum / n_criteria)

    # Calculamos el indice de consistencia
    nMax = 0.0
    for i in range(n_criteria):
        nMax += sums[i] * weights[i]

    consistency_index = (nMax - n_criteria) / (n_criteria - 1)

    return consistency_index


# calcular indice de consistencia para la matriz de alternativas de un criterio (tambien calcula las sumas y sus pesos)
def calculate_CI(criteria: Criteria, alternatives_list: list[Alternative], sums: list[float], weights: list[float]) -> float:
    n_alternatives = len(alternatives_list)
    consistency_index = 0.0
    sums = []
    weights = []

    # Obtenemos las sumas de la matriz
    for alt_one in alternatives_list:
        sum = 0.0
        for alt_two in alternatives_list:
            sum += alt_two.getAltWeight_Crit_Alt(criteria, alt_one)
        sums.append(sum)

    # Obtenemos los pesos de la matriz
    for alt_one in alternatives_list:
        sum = 0.0
        for i in range(n_alternatives):
            num = alt_one.getAltWeight_Crit_Alt(criteria, alternatives_list[i])
            denom = sums[i]
            sum += (num / denom)
        weights.append(sum / n_alternatives)

    # Calculamos el indice de consistencia
    nMax = 0.0
    for i in range(n_alternatives):
        nMax += sums[i] * weights[i]

    consistency_index = (nMax - n_alternatives) / (n_alternatives - 1)

    return consistency_index


# Calcula la relacion de consistencia dado su indice de consistencia y el numero de elementos
def calculate_CR(consistency_index: float, n_elements: int) -> float:
    return consistency_index / RANDOM_INDEX[n_elements]


# Comprueba que se trata de un valor de relacion de consistencia valido
def check_Valid_CR(consistency_relation: float) -> float:
    return consistency_relation <= VALID_UPPER_BOUND_CONSISTENCY_RELATION


# Calcula el valor final de la alternativa
def calculate_Alt_Result(criteria_weights: list[float], alternative_weights_by_crit: list[float]) -> float:
    sum = 0.0

    for i in range(len(criteria_weights)):
        sum += criteria_weights[i] * alternative_weights_by_crit[i]

    return sum


# Calcula el indice del mejor resultado de alternativa
def calculate_Best_Alt(alternatives_results: list[float]) -> int:
    return alternatives_results.index(max(alternatives_results))