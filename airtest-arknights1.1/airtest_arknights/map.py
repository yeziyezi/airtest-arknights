from .util import Util


class Mapper:
    def __init__(self):
        self.map = Util.readJSON("airtest_arknights/map.json")

    def getMap(self):
        return self.map
