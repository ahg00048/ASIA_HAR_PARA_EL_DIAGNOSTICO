import simpful as sf


'''
+===========================================================+
| PRESET DE VARIABLES LINGUISTICAS (TEMP, HUMEDAD, PRESION) |
+===========================================================+
'''

# Obtener variable linguistica de temperatura dando sus limites superior, inferior y mediano (calor, frio, templado).
def create_linguisticVariable_Temperature(temp_lowerBound: float = 5.0, temp_interBound: float = 20.0, temp_upperBound: float = 30.0, gauss_func_sigma: float = 8) -> tuple[sf.LinguisticVariable, list[str]]:
    terms = ["cold", "warm", "hot"]
    
    S_1 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_lowerBound, sigma=gauss_func_sigma), term=terms[0] )
    S_2 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_interBound, sigma=gauss_func_sigma), term=terms[1] )
    S_3 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_upperBound, sigma=gauss_func_sigma), term=terms[2] )

    return ( sf.LinguisticVariable( [S_1, S_2, S_3], concept="Temperature", universe_of_discourse=[temp_lowerBound, temp_upperBound] ), terms )


# Obtener variable linguistica de humedad dando sus limites superior, inferior y medianos (humedad excesiva, baja, media y alta).
def create_linguisticVariable_Humidity(humd_lowerBound: float = 0.3, humd_lowInterBound: float = 0.45, humd_upInterBound: float = 0.6, humd_upperBound: float = 0.8, gauss_func_sigma: float = 8) -> tuple[sf.LinguisticVariable, list[str]]:
    terms = ["low", "medium", "high", "excessive"]

    S_1 = sf.FuzzySet( function=sf.Gaussian_MF(mu=humd_lowerBound, sigma=gauss_func_sigma), term=terms[0] )
    S_2 = sf.FuzzySet( function=sf.Gaussian_MF(mu=humd_lowInterBound, sigma=gauss_func_sigma), term=terms[1] )
    S_3 = sf.FuzzySet( function=sf.Gaussian_MF(mu=humd_upInterBound, sigma=gauss_func_sigma), term=terms[2] )
    S_4 = sf.FuzzySet( function=sf.Gaussian_MF(mu=humd_upperBound, sigma=gauss_func_sigma), term=terms[3] )

    return ( sf.LinguisticVariable( [S_1, S_2, S_3, S_4], concept="Humidity", universe_of_discourse=[0.0, 1.0] ), terms )


# Obtener variable linguistica de proximidad (0 pegado, -200 señal perdida) dando sus limites superior e inferior (fuera y dentro del lugar en el que se encuentra la baliza).
def create_linguisticVariable_Proximity(press_lowerBound: float = -50.0, press_upperBound: float = -150.0, gauss_func_sigma: float = 8) -> tuple[sf.LinguisticVariable, list[str]]:
    terms = ["in", "out"]
    
    S_1 = sf.FuzzySet( function=sf.Gaussian_MF(mu=press_lowerBound, sigma=gauss_func_sigma), term=terms[0] )
    S_2 = sf.FuzzySet( function=sf.Gaussian_MF(mu=press_upperBound, sigma=gauss_func_sigma), term=terms[1] )

    return ( sf.LinguisticVariable( [S_1, S_2], concept="Proximity", universe_of_discourse=[0.0, -200.0]), terms )


# faltan

# Obtener variable linguistica de presion (mmHg) dando sus limites ...
def create_linguisticVariable_Pressure() -> sf.LinguisticVariable:
    return None
    S_1 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_lowerBound, sigma=gauss_func_sigma), term="cold" )
    S_2 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_interBound, sigma=gauss_func_sigma), term="warm" )
    S_3 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_upperBound, sigma=gauss_func_sigma), term="hot" )

    return sf.LinguisticVariable( [S_1, S_2, S_3], concept="Pressure", universe_of_discourse=[temp_lowerBound, temp_upperBound])


# Obtener variable linguistica de pasos (fitness?) dando sus limites ...
def create_linguisticVariable_Steps() -> sf.LinguisticVariable:
    return None
    S_1 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_lowerBound, sigma=gauss_func_sigma), term="cold" )
    S_2 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_interBound, sigma=gauss_func_sigma), term="warm" )
    S_3 = sf.FuzzySet( function=sf.Gaussian_MF(mu=temp_upperBound, sigma=gauss_func_sigma), term="hot" )

    return sf.LinguisticVariable( [S_1, S_2, S_3], concept="Fitness", universe_of_discourse=[temp_lowerBound, temp_upperBound])


'''
+===========================================================+
|                    PRESET DE REGLAS                       |
+===========================================================+
'''

def create_rule_IF_A_THEN_B(ling_var_one: str, ling_var_one_term: str, ling_var_two: str, ling_var_two_term: str):
    return "IF ({0} IS {1}) THEN ({2} IS {3})".format(ling_var_one, ling_var_one_term, ling_var_two, ling_var_two_term)


def create_rule_IF_A_OR_B_THEN_C(ling_var_one: str, ling_var_one_term: str, ling_var_two: str, ling_var_two_term: str, ling_var_three: str, ling_var_three_term: str):
    return "IF ({0} IS {1}) OR ({2} IS {3}) THEN ({4} IS {5})".format(ling_var_one, ling_var_one_term, ling_var_two, ling_var_two_term, ling_var_three, ling_var_three_term)


def create_rule_IF_A_AND_B_THEN_C(ling_var_one: str, ling_var_one_term: str, ling_var_two: str, ling_var_two_term: str, ling_var_three: str, ling_var_three_term: str):
    return "IF ({0} IS {1}) AND ({2} IS {3}) THEN ({2} IS {3})".format(ling_var_one, ling_var_one_term, ling_var_two, ling_var_two_term, ling_var_three, ling_var_three_term)