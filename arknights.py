# -*- encoding=utf8 -*-
from airtest.core.api import *
__author__ = "madyezi"
auto_setup(__file__)
blueStartBtn=Template(r"tpl1567924657620.png", record_pos=(0.419, 0.231), resolution=(1440, 810))
redStartBtn=Template(r"tpl1567853029132.png", record_pos=(0.36, 0.119), resolution=(1440.0, 810.0))
finishImg=Template(r"tpl1567853569965.png", record_pos=(-0.333, 0.21), resolution=(1440, 810))
# 使用药剂回复选项为白色
usePotion=Template(r"tpl1567857774467.png", record_pos=(0.11, -0.218), resolution=(1440, 810)) 
# 使用源石回复为白色
useStone=Template(r"tpl1567868289683.png", record_pos=(0.363, -0.216), resolution=(1440, 810))
# 确认使用药剂
confirmUsePotion=Template(r"tpl1567857978170.png", record_pos=(0.351, 0.172), resolution=(1440, 810)) 
agentFailedMessage=Template(r"tpl1567860026280.png", record_pos=(-0.216, -0.048), resolution=(1440, 810))
continueSettlement=Template(r"tpl1567860934823.png", record_pos=(0.158, 0.112), resolution=(1440, 810))
giveup=Template(r"tpl1567861220806.png", record_pos=(-0.149, 0.114), resolution=(1440, 810))
actionFailed=Template(r"tpl1567861331827.png", record_pos=(0.22, -0.026), resolution=(1440, 810))
agentEnabled=Template(r"tpl1567921000391.png", record_pos=(0.391, 0.179), resolution=(1440, 810))
agentDisabled=Template(r"tpl1567921198118.png", record_pos=(0.392, 0.181), resolution=(1440, 810))
# def exit(msg):
#     assert_equal(0,1,msg)
    
def start():#处理战斗开始前的各种状况
    touch(wait(blueStartBtn))
     # 检测理智不足时使用药剂
    if exists(usePotion):#显示使用药剂，证明药剂还有的用
        touch(confirmUsePotion)
        touch(wait(blueStartBtn))
        touch(wait(redStartBtn))
        return True,"理智不足，使用药水补充"
    # 没理智没药剂，直接退出，碎石不存在的~
    if exists(useStone):#显示使用源石,则证明药剂已经使用完
        #点击下边界外退回最开始的界面
        touch(Template(r"tpl1567869056815.png", record_pos=(0.385, 0.235), resolution=(1440, 810)))
        return False,"理智药水不足，结束运行。"
    # 如果没有补充理智的选项也没有红色按钮，那么八成是不用理智的特殊活动没门票了
    if not exists(redStartBtn):
        return False,"活动门票不足，结束运行。"
    # 点击红色开始
    touch(redStartBtn)
    return True,""

def runEpoch():# 执行一轮战斗,如果代理失误reurn False，否则return True
    while True:#等待此次战斗结束
        sleep(30)
        # 如果进入结算，结束此次战斗
        if exists(finishImg):
            sleep(5) # 避免结算页面刚弹出来点击无效
            touch(finishImg)
            return True
        # 如果代理失误，选择放弃行动
        if exists(agentFailedMessage):
            touch(giveup)
            touch(wait(actionFailed))
            return False

# 运行成功一定次数后结束
def run(successTimes=-1):
    runTimes=0
    agentFailedTimes=0
    # 如果忘记选中代理指挥，选上
    if not exists(agentEnabled):
        touch(agentDisabled)
    while True:
        startStatus,startMsg = start()
        if startMsg != "":
            print(startMsg)
        if not startStatus: # 如果开始状态为False，无法继续战斗，退出
            return
        if not runEpoch():#如果此轮战斗代理失误，计数+1
            agentFailedTimes = agentFailedTimes + 1
        runTimes=runTimes+1
        print("脚本已经运行 "+str(runTimes)+" 次，代理指挥失误 "+str(agentFailedTimes)+" 次")
        if (successTimes!=-1) and (runTimes-agentFailedTimes>=successTimes): #指定成功次数够了退出
            print("脚本运行结束")
            return
run()