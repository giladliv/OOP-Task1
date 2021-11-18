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

    def getTimeOverall(self):
        return self._closeTime + self._openTime + self._startTime + self._stopTime


    def arrayOfTime(self, src, dst, dt, isFirst=False):
        retModes = []
        et = dt
        if isFirst and src != self._pos :
            et += abs(self._pos - src) / self._speed
            retModes.append({"pos": src, "et": et, "mode": self.GOTO})
            et += self._stopTime
            retModes.append({"pos": src, "et": et, "mode": self.STOP})
        et += self._openTime
        retModes.append({"pos": src, "et": et, "mode": self.OPEN})
        et += self._closeTime
        retModes.append({"pos": src, "et": et, "mode": self.CLOSE})
        et += self._startTime
        retModes.append({"pos": src, "et": et, "mode": self.START})
        et += abs(dst - src) / self._speed
        retModes.append({"pos": dst, "et": et, "mode": self.GOTO})
        et += self._stopTime
        retModes.append({"pos": dst, "et": et, "mode": self.STOP})
        return retModes