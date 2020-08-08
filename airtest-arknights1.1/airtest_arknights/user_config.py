from .util import Util


class UserConfig():
    def __init__(self):
        # 读取用户配置
        self.userConfig = Util.readJSON("run.json")

    def getUserOperations(self):
        return self.userConfig["operations"]



    
    
