import json
import sys

from Elevator import Elevator

class Building:
    def __init__(self, buildStr):
        try:
            file = open(buildStr, "r")              # opening the json file
            jBuild = json.load(file)  # makes json suitable for python (dict type convertion)
            file.close()
        except:
            print("problems with building file")
            exit(1)


        self._minFloor = jBuild["_minFloor"]
        self._maxFloor = jBuild["_maxFloor"]
        self._elevators = []
        for elev in jBuild["_elevators"]:       # set the elevators in the array
            curr = Elevator(dict(elev))
            self._elevators.append(curr)


    def getElevators(self):
        return self._elevators

    """
    gets the total amount of levels
    """
    def getRange(self):
        return self._maxFloor - self._minFloor + 1

