from Building import Building
from Elevator import Elevator

class Algo:
    UP = 1
    LEVEL = 0
    DOWN = -1
    def __init__(self, build, calls):
        self.building = build
        self.elevators = build._elevators
        self.lenElev = len(self.elevators)
        self.calls = calls
        self.up = []
        self.down = []
        self.level = []
        self.stops = []
        self.direction = [0] * self.lenElev

        for i in range(self.lenElev):
            self.level.append(i)
            self.stops[i] = []

    def allocateAnElevator(self, c):
        ans = 0
        if (self.lenElev > 1):
            if c["src"] < c["dst"]:
                ans = self.getBestIndexUp(c)
                self._direction[ans] = self.UP
                self.level.remove(ans)
                self.up.append(ans)
            else:
                ans = self.getBestIndexDown(c)
                self._direction[ans] = self.DOWN
                self.level.remove(ans)
                self.down.append(ans)
        self.perform(ans, c["dt"])
        return ans
    
    def perform(self, eId, dt):
        lenStop = len(self.stops[eId])
        i = 0
        while lenStop > 0:
            if self.stops[eId][0]["et"] > dt:
                #add the check of status
                if self.stops[eId][0]["mode"] != Elevator.GOTO:
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"]
                else:
                    posGap = self.stops[eId][0]["et"] - dt              ## position - (end_time - dt)*speed gets the curr position if in goto
                    posGap *= self.elevators[eId]._speed
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"] - int(posGap)
                break
            self.elevators[eId]._pos = self.stops[eId][0]["pos"]
            self.stops[eId].remove(0)


    def getBestIndexUp(self, c):
        if self.lenElev == 1:
            return 0
        index = 0
        for i in range(self.lenElev):
            curr = self.elevators[i]
            if (self._direction[i] == self.DOWN or ((len(self.up) == self.lenElev - 1) and self._direction[i] == self.LEVEL)):
                continue
            if curr._minFloor <= c["src"] and c["dst"] <= curr._maxFloor:
                if len(self.stop[i]) == 0 or curr._pos <= c["src"]:
                    if self.getCalcTimeUp(curr, c["src"], c["dst"]) <= self.getCalcTimeUp(self._elevators[i], c["src"], c["dst"]):
                        index = i
        return index

    def getBestIndexDown(self, c):
        if self.lenElev == 1:
            return 0
        index = 0
        for i in range(self.lenElev):
            curr = self.elevators[i]
            if (self._direction[i] == self.UP or ((len(self.down) == self.lenElev - 1) and self._direction[i] == self.LEVEL)):
                continue
            if curr._minFloor <= c["dst"] and c["src"] <= curr._maxFloor:
                if len(self.stop[i]) == 0 or curr._pos >= c["src"]:
                    if self.getCalcTimeDown(curr, c["src"], c["dst"]) <= self.getCalcTimeDown(self._elevators[i], c["src"], c["dst"]):
                        index = i
        return index

    def getCalcTimeUp(self, curr, src, dst):
        stopsNum = self.howManyStopsUp(curr._id, dst)
        time = stopsNum * curr.getTimeOverall()
        time += (abs(dst - src) + abs(curr._pos - src)) / curr._speed
        return time

    def getCalcTimeDown(self, curr, src, dst):
        stopsNum = self.howManyStopsDown(curr._id, dst)
        time = stopsNum * curr.getTimeOverall()
        time += (abs(dst - src) + abs(curr._pos - src)) / curr._speed

    def howManyStopsUp(self, eId, dst):
        count = 0
        currInd = self.building._minFloor - 1
        for stop in self.stops[eId]:
            if currInd == stop["pos"]:
                continue
            if stop["pos"] < dst:
                count += 1
                currInd = stop["pos"]

        return count

    def howManyStopsDown(self, eId, dst):
        count = 0
        currInd = self.building._minFloor - 1
        for stop in self.stops[eId]:
            if currInd == stop["pos"]:
                continue
            if stop["pos"] > dst:
                count += 1
                currInd = stop["pos"]

        return count

    def setStops(self, eId, c):
        count = 0
        currInd = self.building._minFloor - 1
        ind = 0
        retArr = []
        if c["src"] < c["dst"]:
            for stop in self.stops[eId]:
                if currInd == stop["pos"]:
                    continue
                if stop["pos"] < c["src"]:
                    count += 1
                    currInd = stop["pos"]
                if stop["pos"] >= c["src"]:
                    break
                ind += 1

            if ind == len(self.stops[eId]) and ind > 0:
                retArr = self.elevators[eId].arrayOfTime(c, self.stops[eId][ind - 1]["et"])
            elif ind == len(self.stops[eId]) and ind == 0:
                retArr = self.elevators[eId].arrayOfTime(c, c["dt"])
        else:
            for stop in self.stops[eId]:
                if currInd == stop["pos"]:
                    continue
                if stop["pos"] > c["src"]:
                    count += 1
                    currInd = stop["pos"]
                if stop["pos"] <= c["src"]:
                    break
                ind += 1

        if count == 0:
            retArr = self.elevators[eId].arrayOfTime(c, c["dt"])
        else:
            retArr = self.elevators[eId].arrayOfTime(c, self.stops[eId][ind]["et"])























