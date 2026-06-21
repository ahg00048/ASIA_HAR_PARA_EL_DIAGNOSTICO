from alternative import *
from criteria import *
from config import DATA
import json

data_persistence = DATA['SUBDIR']['PERSISTENT']

_all_name = data_persistence['CRIT_ALT_DATA_NAME']
_all_weight = data_persistence['CRIT_ALT_DATA_REL_WEIGHT']
_all_rel_crit = data_persistence['CRIT_ALT_DATA_REL_CRIT']

_crit_rel = data_persistence['CRIT_DATA_REL']

_alt_rel_alt = data_persistence['ALT_DATA_REL_ALT']
_alt_rel = data_persistence['ALT_DATA_REL']


'''
===============================================================
|               Obtaining values with dfs                     |
===============================================================
'''

'''
Function that converts alternative to json string
'''
def alt_to_json(alt: Alternative) -> str:
    alt_rel = alt.getAlternativeRels()

    dict = {
        _all_name : alt.name,
        _alt_rel : [
        ] 
    }

    for rel in alt_rel:
        if rel.alt == alt:
            continue

        dict[alt_rel].append({
            _all_rel_crit : rel.crit.name,
            _alt_rel_alt : rel.alt.name,
            _all_weight : rel.weight
        })

    return json.dumps(dict)


'''
Function that converts list of criteria to json string
'''
def alt_list_to_json(alts: list[Alternative]):
    alt_list = []
    
    for alt in alts:
        alt_rel = alt.getAlternativeRels()

        dict = {
            _all_name : alt.name,
            _alt_rel : [
            ] 
        }

        for rel in alt_rel:
            if rel.alt == alt:
                continue

            dict[alt_rel].append({
                _all_rel_crit : rel.crit.name,
                _alt_rel_alt : rel.alt.name,
                _all_weight : rel.weight
            })

        alt_list.append(dict.copy())

    return json.dumps({"alternatives" : alt_list})


'''
Function that converts json string to alternative
Returns the alternative without relations and the list of related alternatives with its weights
'''
def alt_from_json(alt_json) -> tuple[Alternative, list[dict]]:
    alt_aux = json.loads(alt_json)
    alt_object = Alternative(alt_aux[_all_name])

    return (alt_object, alt_aux[_alt_rel])


'''
Function that converts json string to list of alternatives
Returns the list of tuples of alternative without relations and the list of related alternatives with its weights
'''
def alt_list_from_json(alt_json) -> list[tuple[Alternative, list[dict]]]:
    alt_list = []
    
    alt_list_aux = json.loads(alt_json)
    if 'alternatives' not in alt_list_aux:
        return []
    
    for alt_aux in alt_list_aux['alternatives']:
        alt_list.append((Alternative(alt_aux[_all_name]), alt_aux[_alt_rel]))
    
    return alt_list


'''
Function that converts criteria to json string
'''
def crit_to_json(crit: Criteria):
    crit_rel = crit.getCriteriaRels()

    dict = {
        _all_name : crit.name,
        _crit_rel : [
        ] 
    }

    for rel in crit_rel:
        if rel.crit == crit:
            continue

        dict[crit_rel].append({
            _all_rel_crit : rel.crit.name,
            _all_weight : rel.weight
        })

    return json.dumps(dict)



'''
Function that converts criteria to json string
'''
def crit_list_to_json(crits: list[Criteria]):
    crit_list = []
    
    for crit in crits:
        crit_rel = crit.getCriteriaRels()

        dict = {
            _all_name : crit.name,
            _crit_rel : [] 
        }

        for rel in crit_rel:
            if rel.crit == crit:
                continue

            dict[_crit_rel].append({
                _all_rel_crit : rel.crit.name,
                _all_weight : rel.weight
            })

        crit_list.append(dict.copy())

    return json.dumps({"criteria" : crit_list})


'''
Function that converts json string to criteria
Returns the criteria without relations and the list of related criteria with its weights
'''
def crit_from_json(crit_json) -> tuple[Criteria, list[dict]]:
    crit_aux = json.loads(crit_json)
    crit_object = Criteria(crit_aux[_all_name])

    return (crit_object, crit_aux[_crit_rel])


'''
Function that converts json string to list of criteria
Returns the list of tuples of criteria without relations and the list of related criteria with its weights
'''
def crit_list_from_json(alt_json) -> list[tuple[Criteria, list[dict]]]:
    crit_list = []
    
    crit_list_aux = json.loads(alt_json)
    if 'criteria' not in crit_list_aux:
        return []

    for crit_aux in crit_list_aux['criteria']:
        crit_list.append((Criteria(crit_aux[_all_name]), crit_aux[_crit_rel]))
    
    return crit_list
