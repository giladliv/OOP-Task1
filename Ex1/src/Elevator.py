class Elevator:
    OPEN = 0
    CLOSE = 1
    START = 2
    GOTO = 3
    STOP = 4
    def __init__(self, elev):
        self._id = elev["_id"]
        self._speed = elev["_speed"]
        self._minFloor = elev["_minFloor"]
        self._maxFloor = elev["_maxFloor"]
        self._closeTime = elev["_closeTime"]
        self._openTime = elev["_openTime"]
        self._startTime = elev["_startTime"]
        self._stopTime = elev["_stopTime"]
        self._pos = 0

    def calcPos(self):
        return  0

    """
    returns the overall time of close,open,start and stop times - they are fixeted
    """
    def getTimeOverall(self):
        return self._closeTime + self._openTime + self._startTime + self._stopTime


    """
        by given one floor and another generate all the end times for every action in move
        dt is the current time the calculation must be from
        isFirst - sets if the currnt src is the first in stops floor list 
    """
    def arrayOfTime(self, src, dst, dt, isFirst=False):
        retModes = []
        et = dt
        if isFirst and src != self._pos :       # if first and has diffrent positions the elevator needs to go from src to dst
            et += abs(self._pos - src) / self._speed        # calc how many time it takes
            retModes.append({"pos": src, "et": et, "mode": self.GOTO})  # goto action has been ended
            et += self._stopTime
            retModes.append({"pos": src, "et": et, "mode": self.STOP})  # stop action has been ended
        et += self._openTime
        retModes.append({"pos": src, "et": et, "mode": self.OPEN})      # open doors action has been ended
        et += self._closeTime
        retModes.append({"pos": src, "et": et, "mode": self.CLOSE})     # close doors action has been ended
        et += self._startTime
        retModes.append({"pos": src, "et": et, "mode": self.START})     # start moving action has been ended
        et += abs(dst - src) / self._speed
        retModes.append({"pos": dst, "et": et, "mode": self.GOTO})      # reached the destination by et time
        et += self._stopTime
        retModes.append({"pos": dst, "et": et, "mode": self.STOP})      # stop moving action has been ended
        return retModes