import pandas as pd


'''
===============================================================
|               Obtaining values with dfs                     |
===============================================================
'''
_on = 'on'
_off = 'off'


def dataFrames_min_max(df: pd.DataFrame, property: str) -> tuple:
    min = float('inf')
    max = float('-inf')

    try:
        for (idx, row) in df.iterrows():
            value = row.loc[property]

            if isinstance(value, str):
                if value == _on:
                    value = 1.0
                else:
                    value = 0.0
                
            if value < min:
                min = value
            if value > max:
                max = value
    except KeyError:
        return None

    return (min, max)


def dataFrames_max(df: pd.DataFrame, property: str) -> float:
    max = float('-inf')
    min = float('inf')

    try:
        for (idx, row) in df.iterrows():
            value = row.loc[property]

            if isinstance(value, str):
                if value == _on:
                    value = 1.0
                else:
                    value = 0.0
                
            if value > max:
                max = value
            if value < min:
                min = value
    except KeyError:
        return None

    return max if property != 'steps' else max - min


def dataFrames_min(df: pd.DataFrame, property: str) -> float:
    min = float('-inf')

    try:
        for (idx, row) in df.iterrows():
            value = row.loc[property]

            if isinstance(value, str):
                if value == _on:
                    value = 1.0
                else:
                    value = 0.0
                
            if value < min:
                min = value
    except KeyError:
        return None

    return min


def dataFrames_sum(df: pd.DataFrame, property: str) -> float:
    sum = 0.0

    try:
        for (idx, row) in df.iterrows():
            value = row.loc[property]

            if isinstance(value, str):
                if value == _on:
                    value = 1.0
                else:
                    value = 0.0
                
            sum += value
    except KeyError:
        return None

    return sum


def dataFrames_mean(df: pd.DataFrame, property: str) -> float:
    sum = 0.0

    try:
        for (idx, row) in df.iterrows():
            value = row.loc[property]

            if isinstance(value, str):
                if value == _on:
                    value = 1.0
                else:
                    value = 0.0
                
            sum += value
    except KeyError:
        return None

    return sum / len(df.index)


def dataFrames_list(df: pd.DataFrame, property: str) -> list:
    values = []
    
    try:
        for (idx, row) in df.iterrows():
            values.append(row.loc[property])
    except KeyError:
        return None

    return values


def dataFrames_properties(df: pd.DataFrame) -> list[str]:
    return df.columns


def dataFrames_check_property_exist(df: pd.DataFrame, name: str) -> bool:
    return (name in df)


def dataFrames_check_empty(df: pd.DataFrame):
    return df.empty


def dataFrames_split(df: pd.DataFrame, time_interval_in_seconds: int) -> list[pd.DataFrame]:
    if df.empty or 'timestamp' not in df:
        return []

    df = df.copy()

    splited = []
    start_idx = 0
    start_time = df.loc[0, 'timestamp']

    for i in range(1, len(df)):
        if df.loc[i, 'timestamp'] - start_time > time_interval_in_seconds:
            splited.append(df.iloc[start_idx:i].reset_index(drop=True))
            start_idx = i
            start_time = df.loc[i, 'timestamp']

    splited.append(df.iloc[start_idx:].reset_index(drop=True))

    return splited


def dataFrames_empty():
    return pd.DataFrame()