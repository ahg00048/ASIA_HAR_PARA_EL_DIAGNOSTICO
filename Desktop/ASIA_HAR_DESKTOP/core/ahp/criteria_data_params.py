import core.dataManagement.dataframe_utils as dfs_utils

class CriteriaDataParams:
    def __init__(self, param, method, crit):
        self.crit = crit
        self.param = param
        self.method = method
    
    def useMethod(self, dfs):
        for df in dfs.values():
            if not dfs_utils.dataFrames_check_property_exist(df, self.param) or dfs_utils.dataFrames_check_empty(df): 
                continue
            match self.method:
                case "Media":
                    return dfs_utils.dataFrames_mean(df, self.param)
                case "Max":
                    return dfs_utils.dataFrames_max(df, self.param)
                case "Min":
                    return dfs_utils.dataFrames_min(df, self.param)
                case "Suma":
                    return dfs_utils.dataFrames_sum(df, self.param)
                
        return None