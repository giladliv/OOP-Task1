import sys
import pandas as pd

from Building import Building
from AlgoBest import AlgoBest

def main(argc, argv):
    print(argc, argv)
    if (argc >=4):
        building = Building(argv[1])
        print(building._elevators)
        alg = AlgoBest(building, argv[2], argv[3])
        alg.runAlgo()
    # if (argc == 4):


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
