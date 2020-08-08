import json
import os


class Util:

    @classmethod
    def readJSON(cls, path):
        with open(path, "r", encoding="utf8") as f:
            return json.loads(f.read())

    @classmethod
    def writJSON(cls, path, data):
        with open(path, "w", encoding="utf8") as f:
            f.write(json.dumps(data))

    @classmethod
    def appendFile(cls, path, data):
        with open(path, "a", encoding="utf8") as f:
            f.write(data+os.linesep)

    @classmethod
    def cleanFile(cls, path):
        with open(path, "w", encoding="utf8") as _:
            return
