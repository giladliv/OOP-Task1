import os
from time import time

from AlgoBest import AlgoBest

buildList = {"1": "B1.json", "2": "B2.json", "3": "B3.json", "4":"B4.json", "5":"B5.json"}
pathBld = "..\\data\\Ex1_input\\Ex1_Buildings\\"
callsList = {"a": "Calls_a.csv", "b": "Calls_b.csv", "c": "Calls_c.csv", "d": "Calls_d.csv"}
pathCall = "..\\data\\Ex1_input\\Ex1_Calls\\"

id = "206768962,316320282"

for build in buildList:
    for call in callsList:
        outName = "..\\data\\Ex1_output\\Ex1_Calls_case_{:s}_{:s}.csv".format(build, call)
        buildFile = pathBld + buildList[build]
        callFile = pathCall + callsList[call]
        alg = AlgoBest(buildFile, callFile, outName)
        alg.runAlgo()
        print()
        milliseconds = int(time() * 1000)
        logFile = "../data/Ex1_output/Ex1_report_case_{:s}_{:s}_{}_ID.log".format(build, call, milliseconds)
        os.system("java -jar ../libs/Ex1_checker_V1.2_obf.jar {:s} {:s} {:s} {:s}".format(id, buildFile, outName, logFile))
        print("java -jar ../libs/Ex1_checker_V1.2_obf.jar {:s} {:s} {:s} {:s}".format(id, buildFile, outName, logFile))

