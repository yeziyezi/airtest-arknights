# -*- encoding=utf8 -*-
import templates as tpl
class Normal:
    def start():
        touch(tpl.blueStart)
        # 药剂用完,直接退出
        if exists(useStone):#显示使用源石,则证明药剂已经使用完
                #点击下边界外退回最开始的界面
                touch(Template(r"tpl1567869056815.png", record_pos=(0.385, 0.235), resolution=(1440, 810)))
                exit("理智合剂已消耗完毕,结束运行.")
        # 检测理智不足时使用药剂
        if exists(usePotion):
            touch(confirmUsePotion)
            touch(wait(blueStartBtn))
        # 点击红色开始
        touch(wait(redStartBtn))

        