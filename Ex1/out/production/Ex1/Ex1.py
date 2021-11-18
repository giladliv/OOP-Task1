import os
import sys
import pandas as pd

from Building import Building
from AlgoBest import AlgoBest

def main(argc, argv):
    print(argc, argv)
    if (argc >=4):
        alg = AlgoBest(argv[1], argv[2], argv[3])
        alg.runAlgo()
        print()
    # if (argc == 4):


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
