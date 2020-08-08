from .read_image import Images
from airtest.core.api import loop_find, TargetNotFoundError, touch, wait, sleep


class UIHelper:
    def __init__(self):
        self.images = Images()

    def exists(self, name, timeout=3):
        """
        按名称查找图片，找到返回坐标，没找到返回False
        """
        try:
            pos = loop_find(self.images.get(name), timeout)
        except TargetNotFoundError:
            return False
        else:
            return pos

    def touch(self, v, isWait=False, waitTimeOut=None):
        """
        如果参数是字符串，按此名称查找图片并点击;如果不是认为v为坐标，直接点击
        """
        if isinstance(v, str):
            if isWait:
                touch(wait(self.images.get(v), timeout=waitTimeOut))
            else:
                touch(self.images.get(v))
        else:
            touch(v)

    def sleep(self, time=5):
        sleep(time)

    def notExist(self, name, timeout=3):
        return not self.exists(name, timeout)
