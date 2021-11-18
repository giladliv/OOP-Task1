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
        self.initCalls(calls)
        self.up = []
        self.down = []
        self.level = []
        self.stops = [0] * self.lenElev         # array of time travel through stops that can be tracked via offline mode
        self.stopsFlr = [0] * self.lenElev      # array that contains only the stops
        self.direction = [0] * self.lenElev     # array of directions
        self.outFile = outFile                  #the name of the output file
        self.maxStops = int(self.building.getRange())   #maximal sops will be the number of floors
        self.upDownElevators()                  #set the ratio of up and down elevators

        for i in range(self.lenElev):           #set all the arrays to be valid
            self.level.append(i)                #at the start all the follrs not moving
            self.stops[i] = []
            self.stopsFlr[i] = []

    """
    cerate the calls avialable through dictioneries
    if it would be completed due to error then catch the exception and then exit the program
    """
    def initCalls(self, calls):
        try:
            self.column_names = ["str", "dt", "src", "dst", "state", "alc"]
            self.calls = pd.read_csv(calls, names=self.column_names)
        except:
            print("error with the calls.csv file, please try again and make sure he exists")
            exit(1)

    """
    generates the ratio of the up and down elevators, and saves it, to next usage
    """
    def upDownElevators(self):
        up = 0
        down = 0
        for i in self.calls.index:                          #counting how many up or down
            if self.calls["src"][i] < self.calls["dst"][i]:
                up += 1
            else:
                down += 1
        sum = up + down
        if down <= up:       # if up has more calls then set the numbers acording to him
            self.upAmount = int((up / sum) * self.lenElev)  # precentage calculations
            self.downAmount = self.lenElev - self.upAmount
        else:               # do the same way for dow (if bigger)
            self.downAmount = int((down / sum) * self.lenElev)
            self.upAmount = self.lenElev - self.downAmount

    """
    the shell of the algorithm - runs all the calls and sets the allocation to the proper elevator
    """
    def runAlgo(self):
        for i in self.calls.index:
            c = {}
            for col in self.calls.columns:
                c[col] = self.calls[col][i]     # using pandas generate each row to dictionary
            self.calls.loc[i, "state"] = -1     #set the state coll to be -1 (irrelevant to our run)
            self.calls.loc[i, "alc"] = self.allocateAnElevator(c)   # after getting the best allocation, save it at the table of the calls
        self.calls.to_csv(self.outFile, index=False, header=None)   # save the table to csv file

    """
    the main target of this task - allocate the best elevator to current call
    """
    def allocateAnElevator(self, c):
        # for every elevator run simulation of prevoius calls and determine the current position
        for eId in range(self.lenElev):
            self.perform(eId, c["dt"], self.direction[eId])

        ans = 0
        if self.lenElev > 1: # only if there are more that 1 elevators run the functions that get the best index
            if c["src"] < c["dst"]:             # UP call
                ans = self.getBestIndexUp(c)
                self.upadeUp(ans)               # according to the chosen elevator set it to be up
            else:                               # DOWN call
                ans = self.getBestIndexDown(c)
                self.upadeDown(ans)             # according to the chosen elevator set it to be down
            self.setStops(ans, c)               # ad the call to the simulated way, and also set the stop regularly
        return ans

    """
    when elevator index is given - set it to the the up array and remove from resting
    """
    def upadeUp(self, eId):
        self.direction[eId] = self.UP
        if eId in self.level:   # remove from level if exists
            self.level.remove(eId)
        if eId not in self.up:  # add to up if not exists
            self.up.append(eId)
            self.up.sort()      # sort after add

    """
        when elevator index is given - set it to the the down array and remove from resting
    """
    def upadeDown(self, eId):
        self.direction[eId] = self.DOWN
        if eId in self.level:   # remove from level if exists
            self.level.remove(eId)
        if eId not in self.down:  # add to up if not exists
            self.down.append(eId)
            self.down.sort()      # sort after add

    """
    the main core of the simulation - for every elevator perform the stops according to the times
    while checking if the call has been completed, the position will be updated 
    """
    def perform(self, eId, dt, dir):
        lenStop = len(self.stops[eId])  # how many actions needed to be done by the coursethe
        i = 0
        while lenStop > 0:
            if  self.stops[eId][0]["et"] > dt:  # if tackeled with action that is above the time then the rest hadn't been completed since
                if self.stops[eId][0]["mode"] != Elevator.GOTO:     #if the elevator is not in actual moving state the the position is the curr pos
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"]

                else:       # if in actual moving and hadn't been completed
                    posGap = float(self.stops[eId][0]["et"] - dt)
                    ## position - (end_time - curr_time)*speed gets the curr position
                    posGap *= self.elevators[eId]._speed
                    if dir == self.DOWN:    # if the direction is down then it has to be added not subed
                        posGap = 0 - posGap
                    self.elevators[eId]._pos = self.stops[eId][0]["pos"] - posGap
                break       # escape from loop

            # when end the elevator completed the whole moving - remove the floor from list of stops
            if self.stops[eId][0]["mode"] == Elevator.GOTO:
                if self.stops[eId][0]["pos"] in self.stopsFlr[eId]:
                    self.stopsFlr[eId].remove(self.stops[eId][0]["pos"])
            self.elevators[eId]._pos = self.stops[eId][0]["pos"]        #after finishing the pos is the end of task potision
            del self.stops[eId][0]      # remove it from the course
            lenStop -= 1

        if lenStop == 0:    # if have no other stops then it is in rest mode
            if dir == self.UP and eId in self.up:
                self.up.remove(eId)
            elif dir == self.DOWN and eId in self.down:
                self.down.remove(eId)
            if eId not in self.level:
                self.level.append(eId)
                self.level.sort()
                self.direction[eId] = self.LEVEL

    """
    when the call is up - get the avialable elevator with the lowest time of completing the call 
    """
    def getBestIndexUp(self, c):
        if self.lenElev == 1:
            return 0
        if len(self.up) > 0:     #if any up elevators exists it is more suitable to take it from there
            index = self.up[0]
        else:
            index = self.level[0]

        for i in range(self.lenElev):
            curr = self.elevators[i]
            # if the direction is down or the max usage of up elev's (and resting mode) - skip this elevator
            if (self.direction[i] == self.DOWN or ((len(self.up) == self.upAmount) and self.direction[i] == self.LEVEL)):
                continue

            if curr._minFloor <= c["src"] and c["dst"] <= curr._maxFloor:   # if in bouderies
                if len(self.stopsFlr[i]) <= self.maxStops:
                    # if the time of the current elev is lower then its the best fore us
                    if self.getCalcTimeUp(i, c["src"], c["dst"]) < self.getCalcTimeUp(index, c["src"], c["dst"]):
                        index = i
        return index

    """
        when the call is down - get the avialable elevator with the lowest time of completing the call 
    """
    def getBestIndexDown(self, c):
        if self.lenElev == 1:
            return 0
        if len(self.down) > 0:     #if any down elevators exists it is more suitable to take it from there
            index = self.down[0]
        else:
            index = self.level[0]
        for i in range(self.lenElev):
            curr = self.elevators[i]
            # if the direction is up or the max usage of down elev's (and resting mode) - skip this elevator
            if (self.direction[i] == self.UP or ((len(self.down) == self.downAmount) and self.direction[i] == self.LEVEL)):
                continue
            if curr._minFloor <= c["dst"] and c["src"] <= curr._maxFloor:
                if len(self.stopsFlr[i]) <= self.maxStops:
                    # if the time of the current elev is lower then its the best fore us
                    if self.getCalcTimeDown(i, c["src"], c["dst"]) < self.getCalcTimeDown(index, c["src"], c["dst"]):
                        index = i
        return index

    """
    when given index of elevator and source and destination find the time of moving in up direction
    """
    def getCalcTimeUp(self, i, src, dst):
        curr = self.elevators[i]
        stopsNum = self.howManyStopsUp(i, dst)      # how many stops before the src
        time = stopsNum * curr.getTimeOverall()     # open,close,start,stop time in total
        time += (abs(dst - src) + abs(curr._pos - src)) / curr._speed   # add the time for gong from pos yo src and then to dest
        return time

    def getCalcTimeDown(self, i, src, dst):
        curr = self.elevators[i]
        stopsNum = self.howManyStopsDown(i, dst)    # how many stops before the src
        time = stopsNum * curr.getTimeOverall()     # open,close,start,stop time in total
        time += (abs(dst - src) + abs(curr._pos - src)) / curr._speed  # add the time for gong from pos yo src and then to dest
        return time

    """
    counts how many stops before src - check num until grater
    """
    def howManyStopsUp(self, eId, dst):
        count = 0
        for stop in self.stopsFlr[eId]:
            if dst < stop:
                break
            count += 1
        return count

    """
        counts how many stops before src - check num until lower
    """
    def howManyStopsDown(self, eId, dst):
        count = 0
        for stop in self.stopsFlr[eId]:
            if dst > stop:
                break
            count += 1
        return count

    """
    after choosing the best elevator to allocate the function sets the src and dest floor to the relevant array stop
    after that it will demonstrate all the action fron the first floor to the last 
    """
    def setStops(self, eId, c):
        if c["src"] not in self.stopsFlr[eId]:  #add the src and dest if not in arrays
            self.stopsFlr[eId] += [c["src"]]
        if c["dst"] not in self.stopsFlr[eId]:
            self.stopsFlr[eId] += [c["dst"]]

        # (relies that the elevator has the same direction)
        self.stopsFlr[eId].sort(reverse=(c["src"] > c["dst"])) # if call is for down then the sort needs to be in reverse

        arrWay = []
        dt = c["dt"]
        for i in range(len(self.stopsFlr[eId]) - 1):  # for each two floors generate the action dictionaries (with end times)
            flag = False
            if i == 0:      # if it is the first in call, must go from current position to the src
                flag = True
            # adds the action to helper array
            arrWay += self.elevators[eId].arrayOfTime(self.stopsFlr[eId][i], self.stopsFlr[eId][i + 1], dt, flag)
            dt = arrWay[len(arrWay) - 1]["et"]  # saves the end time of the last action - allows continuety
        self.stops[eId] = arrWay

