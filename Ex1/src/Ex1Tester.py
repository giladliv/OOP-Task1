import unittest
from Ex1 import checkIfArgsCorrect
from AlgoBest import AlgoBest


class MyTestCase(unittest.TestCase):
    argv = ["Ex1.py", "sup_test_files/B1.json", "sup_test_files/out.csv", "sup_test_files/outTest.csv"]
    def resetAlgo(self):
        self.algo = AlgoBest(self.argv[1], self.argv[2], self.argv[3])

    def test_checkFilesMissing(self):
        self.assertEqual(True, checkIfArgsCorrect(len(self.argv), self.argv))


    def test_allocation(self):
        self.resetAlgo()
        for i in self.algo.calls.index:
            c = {}
            for col in self.algo.calls.columns:
                c[col] = self.algo.calls[col][i]     # using pandas generate each row to dictionary
            self.assertEqual(self.algo.calls.loc[i, "alc"], self.algo.allocateAnElevator(c))
    
    def test_arrayOfTime(self):
        self.resetAlgo()
        timeWay = [{'pos': 0, 'et': 2.2, 'mode': 0},
                   {'pos': 0, 'et': 3.2, 'mode': 1},
                   {'pos': 0, 'et': 4.2, 'mode': 2},
                   {'pos': 100, 'et': 29.2, 'mode': 3},
                   {'pos': 100, 'et': 30.2, 'mode': 4}]
        self.assertEqual(timeWay, self.algo.elevators[6].arrayOfTime(0, 100, 1.2))

        timeWay = [{'pos': 0, 'et': 124.456789, 'mode': 0},
                   {'pos': 0, 'et': 125.456789, 'mode': 1},
                   {'pos': 0, 'et': 126.456789, 'mode': 2},
                   {'pos': 8, 'et': 127.256789, 'mode': 3},
                   {'pos': 8, 'et': 128.256789, 'mode': 4}]
        self.assertEqual(timeWay, self.algo.elevators[1].arrayOfTime(0, 8, 123.456789, True))

        
    def test_setStops(self):
        self.resetAlgo()
        self.algo.stopsFlr[2] = [2, 5, 3]
        c = {"src": 4, "dst": 9, "dt": 10.12588521}
        self.algo.setStops(2, c)
        self.assertEqual([2, 3, 4, 5, 9], self.algo.stopsFlr[2])
        testArr =[{'pos': 2, 'et': 11.12588521, 'mode': 3}, {'pos': 2, 'et': 12.12588521, 'mode': 4},
                  {'pos': 2, 'et': 13.12588521, 'mode': 0}, {'pos': 2, 'et': 14.12588521, 'mode': 1},
                  {'pos': 2, 'et': 15.12588521, 'mode': 2}, {'pos': 3, 'et': 15.62588521, 'mode': 3},
                  {'pos': 3, 'et': 16.62588521, 'mode': 4}, {'pos': 3, 'et': 17.62588521, 'mode': 0},
                  {'pos': 3, 'et': 18.62588521, 'mode': 1}, {'pos': 3, 'et': 19.62588521, 'mode': 2},
                  {'pos': 4, 'et': 20.12588521, 'mode': 3}, {'pos': 4, 'et': 21.12588521, 'mode': 4},
                  {'pos': 4, 'et': 22.12588521, 'mode': 0}, {'pos': 4, 'et': 23.12588521, 'mode': 1},
                  {'pos': 4, 'et': 24.12588521, 'mode': 2}, {'pos': 5, 'et': 24.62588521, 'mode': 3},
                  {'pos': 5, 'et': 25.62588521, 'mode': 4}, {'pos': 5, 'et': 26.62588521, 'mode': 0},
                  {'pos': 5, 'et': 27.62588521, 'mode': 1}, {'pos': 5, 'et': 28.62588521, 'mode': 2},
                  {'pos': 9, 'et': 30.62588521, 'mode': 3}, {'pos': 9, 'et': 31.62588521, 'mode': 4}]
        self.assertEqual(testArr, self.algo.stops[2])

    def test_perform(self):
        self.resetAlgo()
        dt = 0
        for i in range(4):
            c = {}
            for col in self.algo.calls.columns:
                c[col] = self.algo.calls[col][i]
            if i < 3:
                self.algo.allocateAnElevator(c)
            dt = self.algo.calls["dt"][i]

        for i in range(3):
            self.algo.perform(i, dt, self.algo.direction[i])

        self.assertEqual([], self.algo.stops[0])
        testArr = [{'pos': -5, 'et': 25.73592412, 'mode': 0}, {'pos': -5, 'et': 26.73592412, 'mode': 1},
                   {'pos': -5, 'et': 27.73592412, 'mode': 2}, {'pos': -3, 'et': 27.93592412, 'mode': 3},
                   {'pos': -3, 'et': 28.93592412, 'mode': 4}]
        self.assertEqual(testArr, self.algo.stops[1])
        self.assertEqual([], self.algo.stops[2])

        self.assertEqual(0, self.algo.elevators[0]._pos)
        self.assertEqual(-5, self.algo.elevators[1]._pos)
        self.assertEqual(0, self.algo.elevators[2]._pos)


if __name__ == '__main__':
    unittest.main()
