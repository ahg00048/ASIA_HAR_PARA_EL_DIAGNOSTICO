import core.dataframe_utils as dfs_utils

class CriteriaDataParams:
    def __init__(self, param, method, crit):
        self.crit = crit
        self.param = param
        self.method = method
    
    def useMethod(self, df):
        match self.method:
            case "Media":
                return dfs_utils.dataFrames_mean(df, self.param)
            case "Max":
                return dfs_utils.dataFrames_max(df, self.param)
            case "Min":
                return dfs_utils.dataFrames_min(df, self.param)
            case "Suma":
                return dfs_utils.dataFrames_sum(df, self.param)
            case _:
                return None