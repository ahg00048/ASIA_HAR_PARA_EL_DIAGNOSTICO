from core.ahp.alternative import *
from core.ahp.criteria import *
from core.ahp.criteria_data_params import *
from core.ahp.alternatives_data_params import *
from core.config import DATA
import json

_data_persistence = DATA['SUBDIR']['PERSISTENT']

# crit and alt
_all_name = _data_persistence['CRIT_ALT_DATA_NAME']
_all_weight = _data_persistence['CRIT_ALT_DATA_REL_WEIGHT']
_all_rel_crit = _data_persistence['CRIT_ALT_DATA_REL_CRIT']

_crit_set_name = _data_persistence['CRIT_SET_NAME']
_crit_rel = _data_persistence['CRIT_DATA_REL']

_alt_param_set_name = _data_persistence['CRIT_PARAM_SET_NAME']
_crit_param_method = _data_persistence['CRIT_PARAM_DATA_METHOD']
_crit_param_param = _data_persistence['CRIT_PARAM_DATA_PARAM']

_alt_param_set_name = _data_persistence['ALT_PARAM_SET_NAME']
_alt_param_func = _data_persistence['ALT_PARAM_DATA_FUNC']

_alt_set_name = _data_persistence['ALT_SET_NAME']
_alt_rel_alt = _data_persistence['ALT_DATA_REL_ALT']
_alt_rel = _data_persistence['ALT_DATA_REL']

# time range
_time_start = _data_persistence['TIME_START']
_time_range = _data_persistence['TIME_RANGE']


'''
===============================================================
|               Serializing to and from json                  |
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
        alt_rels = alt.getAlternativeRels()

        dict = {
            _all_name : alt.name,
            _alt_rel : [
            ] 
        }

        for rel in alt_rels:
            if rel.alt == alt:
                continue

            dict[_alt_rel].append({
                _all_rel_crit : rel.crit.name,
                _alt_rel_alt : rel.alt.name,
                _all_weight : rel.weight
            })

        alt_list.append(dict.copy())

    return json.dumps({_alt_set_name : alt_list})


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
    if _alt_set_name not in alt_list_aux:
        return []
    
    for alt_aux in alt_list_aux[_alt_set_name]:
        alt_list.append((Alternative(alt_aux[_all_name]), alt_aux[_alt_rel]))
    
    return alt_list

'''
====================================================================================================================
'''


'''
Function that converts alternatives params to json string
'''
def alt_param_list_to_json(alt_params: list[AlternativesDataParams]):
    alt_param_list = []
    
    for alt_p in alt_params:
        dict = {
            _alt_rel_alt : alt_p.alt,
            _all_rel_crit : alt_p.crit,
            _alt_param_func : alt_p.func
        }

        alt_param_list.append(dict.copy())

    return json.dumps({_alt_param_set_name : alt_param_list})


'''
Function that converts json string to list of alternatives
Returns the list of tuples of alternatives data parameters without the relation to the criteria
'''
def alt_param_list_from_json(alt_param_json) -> list[AlternativesDataParams]:
    alt_param_list = []
    
    alt_param_list_aux = json.loads(alt_param_json)
    if _alt_param_set_name not in alt_param_list_aux:
        return []

    for alt_param_aux in alt_param_list_aux[_alt_param_set_name]:
        alt_param_list.append(AlternativesDataParams(alt_param_aux[_alt_rel_alt], alt_param_aux[_all_rel_crit], alt_param_aux[_alt_param_func]))
    
    return alt_param_list


'''
====================================================================================================================
'''


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

    return json.dumps({_crit_set_name : crit_list})


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
    if _crit_set_name not in crit_list_aux:
        return []

    for crit_aux in crit_list_aux[_crit_set_name]:
        crit_list.append((Criteria(crit_aux[_all_name]), crit_aux[_crit_rel]))
    
    return crit_list


'''
====================================================================================================================
'''


'''
Function that converts criteria params to json string
'''
def crit_param_list_to_json(crit_params: list[CriteriaDataParams]):
    crit_param_list = []
    
    for crit_p in crit_params:
        dict = {
            _all_rel_crit : crit_p.crit,
            _crit_param_param : crit_p.param,
            _crit_param_method : crit_p.method
        }

        crit_param_list.append(dict.copy())

    return json.dumps({_alt_param_set_name : crit_param_list})


'''
Function that converts json string to list of criteria
Returns the list of tuples of criteria data parameters without the relation to the criteria
'''
def crit_param_list_from_json(crit_param_json) -> list[CriteriaDataParams]:
    crit_param_list = []
    
    crit_param_list_aux = json.loads(crit_param_json)
    if _alt_param_set_name not in crit_param_list_aux:
        return []

    for crit_param_aux in crit_param_list_aux[_alt_param_set_name]:
        crit_param_list.append(CriteriaDataParams(crit_param_aux[_crit_param_param], crit_param_aux[_crit_param_method], crit_param_aux[_all_rel_crit]))
    
    return crit_param_list


'''
====================================================================================================================
'''


'''
Function that converts time range into json
'''
def time_to_json(time_start: int, time_range: int):
    time_dict = {
        _time_start : time_start,
        _time_range : time_range
    }

    return json.dumps(time_dict)


'''
Function that converts json into time range
'''
def time_from_json(time_json: str) -> tuple[int, int]:
    time_dict = json.loads(time_json)

    if _time_start not in time_dict or _time_range not in time_dict:
        return (0, 0)

    return (int(time_dict[_time_start]), int(time_dict[_time_range]))


'''
====================================================================================================================
'''

'''
Function that returns named string list from json 
'''
def str_list_from_json(name: str, content: str) -> list[str]:
    dict = json.loads(content)

    if name not in dict:
        return []

    return dict[name]