import json
import sys

from Elevator import Elevator

class Building:
    def __init__(self, buildStr):
        try:
            file = open(buildStr, "r")
        except:
            print("problems with building file")
            exit(1)

        jBuild = json.load(file)
        self._minFloor = jBuild["_minFloor"]
        self._maxFloor = jBuild["_maxFloor"]
        self._elevators = []
        for elev in jBuild["_elevators"]:
            curr = Elevator(dict(elev))
            self._elevators.append(curr)
        file.close()

    def getElevators(self):
        return self._elevators

    def getRange(self):
        return self._maxFloor - self._minFloor

