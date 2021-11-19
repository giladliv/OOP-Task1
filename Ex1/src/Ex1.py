import os
import sys
from pathlib import Path

import pandas as pd

from Building import Building
from AlgoBest import AlgoBest

def checkIfArgsCorrect(argc, argv):
    check = True
    if argc < 4:
        print("some files are missing")
        check = False
    else:
        if not argv[1].endswith(".json"):
            print("ending does not match to the building file (1)")
            check = False
        if not argv[2].endswith(".csv"):
            print("ending does not match to the calls file (2)")
            check = False
        if not argv[3].endswith(".csv"):
            print("ending does not match to the output file (3)")
            check = False

    if not check:
        print("please note that it must be as the same as the following Syntax:")
        print("{:s} <*.json> <*.csv> <*.csv>".format(Path(__file__).name))
        print("(1: Building file, 2: calls file, 3: output file)")
        exit(1)
    return True


def main(argc, argv):
    checkIfArgsCorrect(argc, argv)              # thats make sure that there are 4 or more arguments
    alg = AlgoBest(argv[1], argv[2], argv[3])
    alg.runAlgo()


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
