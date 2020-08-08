from .util import Util
from .map import Mapper
from .user_config import UserConfig
from .ui_helper import UIHelper


class Excuter:
    def __init__(self):
        self.log("loading configurations...")
        self.map = Mapper().getMap()
        self.userConfig = UserConfig()
        self.userOperations = self.userConfig.getUserOperations()
        self.ui = UIHelper()
        Util.cleanFile("log.txt")

    def excute(self):
        total_cost = 0
        for op in self.userOperations:
            currentMap = self.map[op["name"]]
            # 定位给到指定关卡
            if not self.locate(currentMap["steps"]):
                self.log(op["name"]+"关卡未开放，跳过")
                continue
            # 如果忘记选中代理指挥，选上
            exists = self.ui.exists("agentDisabled")
            if exists:
                self.ui.touch(exists)
            i = 1
            while i <= op["times"]:
                startable, msg = self.start()
                if msg != "":
                    self.log(msg)
                if not startable:
                    return
                if(self.runEpoch()):
                    total_cost = total_cost+currentMap["cost"]
                    self.log(op["name"]+"第"+str(i)+"次，消耗理智" +
                             str(currentMap["cost"])+",累计消耗"+str(total_cost))
                    i = i+1
                else:
                    total_cost = total_cost+1
                    self.log(op["name"]+" 代理指挥作战失误，消耗理智1,累计消耗"+str(total_cost))

    def runEpoch(self):  # 执行一轮战斗,如果代理失误reurn False，否则return True
        while True:  # 等待此次战斗结束
            self.ui.sleep(5)
            # 如果进入结算，结束此次战斗
            exists = self.ui.exists("finish")
            if exists:
                self.ui.sleep(5)  # 避免结算页面刚弹出来点击无效
                self.ui.touch(exists)
                return True
            # 如果代理失误，选择放弃行动
            exists = self.ui.exists("agentFailedMessage")
            if exists:
                self.ui.touch("giveup")
                self.ui.touch("actionFailed", isWait=True)
                return False
            # 如果升级了，继续刷
            exists = self.ui.exists("levelUp")
            if exists:
                self.ui.sleep(5)
                self.ui.touch(exists)
                self.ui.touch("finish", isWait=True)
                return True

    # 战斗前进行检测，如可以就开始战斗
    def start(self):
        self.ui.touch("blueStartBtn", isWait=True)
        # 检测理智不足时使用药剂
        if(self.ui.exists("usePotionLableWhite")):  # 显示使用药剂，证明药剂还有的用
            self.ui.touch("confirmUsePotion")
            self.ui.touch("blueStartBtn", isWait=True)
            self.ui.touch("redStartBtn", isWait=True)
            return True, "理智不足，使用药剂补充"
        # 没理智没药剂，直接退出，碎石不存在的~
        if self.ui.exists("useStoneLabelWhite"):  # 显示使用源石,则证明药剂已经使用完
            # 点击下边界外退回最开始的界面
            self.ui.touch("backToReady")
            # 回到主界面
            self.ui.touch("homeButton")
            self.ui.touch("goHome", isWait=True)
            return False, "理智药水不足，结束运行。"
        # 如果没有补充理智的选项也没有红色按钮，那么八成是不用理智的特殊活动没门票了
        if self.ui.notExist("redStartBtn"):
            return False, "活动门票不足，结束运行。"
        # 点击红色开始
        self.ui.touch("redStartBtn")
        return True, ""

    def locate(self, steps):
        # 跳转到战斗页面
        exists = self.ui.exists("homeButton", timeout=20)
        if(exists):
            self.ui.touch(exists)
            self.ui.touch("goHome", isWait=True)
        self.ui.touch("blackBattle", isWait=True)
        # 定位到关卡
        for step in steps:
            self.ui.touch(step, isWait=True)
            # 如果关卡未开放
            if(self.ui.exists("not-open")):
                return False
        return True

    # 记录
    def log(self, msg):
        print(msg)
        Util.appendFile("log.txt", msg)
        return
