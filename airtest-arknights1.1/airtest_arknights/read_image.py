# -*- encoding=utf8 -*-
from airtest.core.api import Template
import json
from .util import Util
class Images:
    def __init__(self):
        self.resolution = (1440, 810)
        with open("airtest_arknights/image.json","r",encoding="utf8") as f:
            self.json=json.loads(f.read())
        self.json=Util.readJSON("airtest_arknights/image.json")
    def setResolution(self, width, height):
        self.resolution = (width, height)

    def get(self,key):
        current=self.json[key]
        pos=(current["pos"]["x"],current["pos"]["y"])
        return Template("airtest_arknights/images/"+current["name"], record_pos=(pos), resolution=self.resolution)
