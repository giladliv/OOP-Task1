import pandas as pd

from Building import Building
from Elevator import Elevator


class AlgoBest:
    UP = 1
    LEVEL = 0
    DOWN = -1

    def __init__(self, build, calls, outFile):
        self.building = Building(build)
        self.elevators = self.building.getElevators()
        self.lenElev = len(self.elevators)
        self.column_names = ["str", "dt", "src", "dst", "state", "alc"]
        self.calls = pd.read_csv(calls, names=self.column_names)
        self.up = []
        self.down = []
        self.level = []
        self.stops = [0] * self.lenElev
        self.stopsFlr = [0] * self.lenElev
        self.direction = [0] * self.lenElev
        self.outFile = outFile
        self.maxStops = int(self.building.getRange() / self.lenElev)
        self.upDownElevators()

        for i in range(self.lenElev):
            self.level.append(i)
            self.stops[i] = []
            self.stopsFlr[i] = []

    def __del__(self):
        del self.up
        del self.down
        del self.level
        del self.stops
        del self.stopsFlr
        del self.direction

    def upDownElevators(self):
        up = 0
        down = 0
        for i in self.calls.index:
            if self.calls["src"][i] < self.calls["dst"][i]:
                up += 1
            else:
                down += 1
        sum = up + down
        if down < up:
            self.upAmount = int((up / sum) * self.lenElev)
            self.downAmount = self.lenElev - self.upAmount
        else:
            self.downAmount = int((down / sum) * self.lenElev)
            self.upAmount = self.lenElev - self.downAmount

    def runAlgo(self):
        up = 0
        down = 0
        for i in self.calls.index:
            if self.calls["src"][i] < self.calls["dst"][i]:
                up += 1
            else:
                down += 1

        for i in self.calls.index:
            c = {}
            for col in self.calls.columns:
                c[col] = self.calls[col][i]
            self.calls.loc[i, "state"] = 0
            self.calls.loc[i, "alc"] = self.allocateAnElevator(c)
            #print(self.calls["alc"][i])
        self.calls.to_csv(self.outFile, index=False, header=None)

    def allocateAnElevator(self, c):
        for eId in range(self.lenElev):
            self.perform(eId, c["dt"], self.direction[eId])

        ans = 0
        if self.lenElev > 1:
            if c["src"] < c["dst"]:
                ans = self.getBestIndexUp(c)
                self.upadeUp(ans)
            else:
                ans = self.getBestIndexDown(c)
                self.upadeDown(ans)
            self.setStops(ans, c)
        return ans

    def upadeUp(self, eId):
        self.direction[eId] = self.UP
        if eId in self.level:
            self.level.remove(eId)
        if eId not in self.up:
            self.up.append(eId)
            self.up.sort()

    def upadeDown(self, eId):
        self.direction[eId] = self.DOWN
        if eId in self.level:
            self.level.remove(eId)
        if eId not in self.down:
            self.down.append(eId)
            self.down.sort()

    def perform(self, eId, dt, dir):
        lenStop = len(self.stops[eId])
        i = 0
        while lenStop > 0:

            if  self.stops[eId][0]["et"] > dt:
                # add the check of status
                if self.stops[eId][0]["mode"] != Elevator.GOTO:
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"]

                else:
                    posGap = float(self.stops[eId][0]["et"] - dt)
                    ## position - (end_time - dt)*speed gets the curr position if in goto
                    posGap *= self.elevators[eId]._speed
                    if dir == self.DOWN:
                        posGap = 0 - posGap
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"] - posGap
                break

            if self.stops[eId][0]["mode"] == Elevator.GOTO:
                if self.stops[eId][0]["pos"] in self.stopsFlr[eId]:
                    self.stopsFlr[eId].remove(self.stops[eId][0]["pos"])
            self.elevators[eId]._pos = self.stops[eId][0]["pos"]
            del self.stops[eId][0]
            lenStop -= 1

        if lenStop == 0:
            if dir == self.UP and eId in self.up:
                self.up.remove(eId)
            elif dir == self.DOWN and eId in self.down:
                self.down.remove(eId)
            if eId not in self.level:
                self.level.append(eId)
                self.level.sort()
                self.direction[eId] = self.LEVEL

    def getBestIndexUp(self, c):
        if self.lenElev == 1:
            return 0
        if len(self.up) > 0:
            index = self.up[0]
        else:
            index = self.level[0]

        for i in range(self.lenElev):
            curr = self.elevators[i]
            if (self.direction[i] == self.DOWN or ((len(self.up) == self.upAmount) and self.direction[i] == self.LEVEL)):
                continue

            if curr._minFloor <= c["src"] and c["dst"] <= curr._maxFloor:
                if len(self.stopsFlr[i]) <= self.maxStops:
                    if self.getCalcTimeUp(curr, c["src"], c["dst"]) < self.getCalcTimeUp(self.elevators[index], c["src"], c["dst"]):
                        index = i
        return index

    def getBestIndexDown(self, c):
        if self.lenElev == 1:
            return 0
        if len(self.down) > 0:
            index = self.down[0]
        else:
            index = self.level[0]
        for i in range(self.lenElev):
            curr = self.elevators[i]
            if (self.direction[i] == self.UP or ((len(self.down) == self.downAmount) and self.direction[i] == self.LEVEL)):
                continue
            if curr._minFloor <= c["dst"] and c["src"] <= curr._maxFloor:
                if len(self.stopsFlr[i]) <= self.maxStops:
                    if self.getCalcTimeDown(curr, c["src"], c["dst"]) < self.getCalcTimeDown(self.elevators[index], c["src"], c["dst"]):
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
        return time

    def howManyStopsUp(self, eId, dst):
        count = 0
        for stop in self.stopsFlr[eId]:
            if dst <= stop:
                break
            count += 1
        return count

    def howManyStopsDown(self, eId, dst):
        count = 0
        for stop in self.stopsFlr[eId]:
            if dst >= stop:
                break
            count += 1
        return count

    def setStops(self, eId, c):
        if c["src"] not in self.stopsFlr[eId]:
            self.stopsFlr[eId] += [c["src"]]
        if c["dst"] not in self.stopsFlr[eId]:
            self.stopsFlr[eId] += [c["dst"]]

        self.stopsFlr[eId].sort(reverse=(c["src"] > c["dst"]))


        arrWay = []
        dt = c["dt"]
        if len(self.stops[eId]) == 0:
            arrWay = self.elevators[eId].arrayOfTime(c["src"], c["dst"], dt, True)
        else:
            for i in range(len(self.stopsFlr[eId]) - 1):
                flag = False
                if i == 0:
                    flag = True
                arrWay += self.elevators[eId].arrayOfTime(self.stopsFlr[eId][i], self.stopsFlr[eId][i + 1], dt, flag)
                dt = arrWay[len(arrWay) - 1]["et"]

        self.stops[eId] = arrWay

