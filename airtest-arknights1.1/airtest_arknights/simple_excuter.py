from .util import Util
from .ui_helper import UIHelper
import time


class SimpleExcuter:
    def __init__(self):
        self.ui = UIHelper()

    def excute(self, times):
        # 如果忘记选中代理指挥，选上
        exists = self.ui.exists("agentDisabled")
        if exists:
            self.ui.touch(exists)
        success_times = 1  # 成功轮次
        total_times = 1  # 总轮次
        while success_times <= times:
            startable, msg = self.start()
            if msg != "":
                self.log(msg)
            if not startable:
                 # 回到主界面
                self.ui.touch("homeButton")
                self.ui.touch("goHome", isWait=True)
                return
            if(self.runEpoch()):
                self.log("epoch "+str(total_times)+" success")
                success_times = success_times+1
            else:
                self.log("epoch "+str(total_times)+" failed.")
            total_times = total_times+1
        # 回到主界面
        self.ui.touch("homeButton")
        self.ui.touch("goHome", isWait=True)

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
                # 有时会出现莫名其妙没有升级但还是进入这个循环里面然后找不到finish图片直接报错停止
                exists = self.ui.exists("finish")
                if exists:
                    self.ui.touch(exists)
                else:
                    continue
                return True

    # 战斗前进行检测，如可以就开始战斗
    def start(self):
        self.ui.touch("blueStartBtn", isWait=True)
        # 显示使用源石,则证明药剂已经使用完，等待5分钟
        if self.ui.exists("useStone", timeout=5):
            # 点击下边界外退回最开始的界面
            self.ui.touch("backToReady")
            self.log("The potion is not enough,wait for five minute")
            time.sleep(60*5)
            self.start()
            return False, ""
        # # 显示使用源石,则证明药剂已经使用完，退出
        # if self.ui.exists("useStone", timeout=5):
        #     # 点击下边界外退回最开始的界面
        #     self.ui.touch("backToReady")
        #     return False, "The potion is not enough, stop running"
        # 如果不是显示使用源石，且还有使用药剂恢复字样，则还有剩余药剂，使用之
        if self.ui.exists("usePotion"):
            self.ui.touch("confirmUsePotion")
            self.ui.touch("blueStartBtn", isWait=True)
            self.ui.touch("redStartBtn", isWait=True)
            return True, "Loss of sanity.Using the potion."
        # 如果没有补充理智的选项也没有红色按钮，那么八成是不用理智的特殊活动没门票了
        if self.ui.notExist("redStartBtn"):
            return False, "活动门票不足，结束运行。"
        # 点击红色开始
        self.ui.touch("redStartBtn")
        return True, ""

    # 记录

    def log(self, msg):
        print(msg)
        return
