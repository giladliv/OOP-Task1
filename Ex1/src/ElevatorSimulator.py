import time
import tkinter as tk
from tkinter import *

from AlgoBest import AlgoBest
from Ex1 import checkIfArgsCorrect


class SimulatorElev(AlgoBest):

    def __init__(self, build, calls, outFile):
        super().__init__(build, calls, outFile)
        self.min = self.building._minFloor
        self.max = self.building._maxFloor
        self.initSim()

    """
        the heart of the Simulator's visuals 
    """
    def initSim(self):
        self.slides = []
        self.root = tk.Tk()
        self.high = Frame(self.root)
        self.high.pack()
        self.mid = Frame(self.root)
        self.mid.pack(side=TOP)
        self.low = Frame(self.root)
        self.low.pack(side=TOP)

        self.root.title('Gilad Livshitz & Batel Cohen\'s Simulator')
        self.root.state('zoomed')

        for i in range(self.lenElev):
            s = Scale(self.high, orient='vertical', tickinterval=1, from_=self.max, to=self.min, showvalue=True, resolution=2,
                      length=650, width=30, sliderlength=40, background='white', label=str(i),
                      foreground='black', font=10)
            s.set(0)
            self.slides.append(s)

        self.label = Label(self.mid, text=" ", font=10)     # the label of the current dt time
        self.label.pack(side=LEFT)

        self.cpr = Label(self.low, text="Gilad Livshitz & Batel Cohen\'s Simulator", font=10)
        self.cpr.pack(side=LEFT)

        self.B = tk.Button(self.low, text="start simulator", command=self.runAlgo, font=10)
        for i in range(self.lenElev):
            self.slides[i].pack(side=LEFT)
        self.B.pack(side=BOTTOM)


    def runAlgo(self):
        for i in self.calls.index:
            c = {}
            for col in self.calls.columns:
                c[col] = self.calls[col][i]
            self.calls.loc[i, "state"] = -1
            self.calls.loc[i, "alc"] = self.allocateAnElevator(c)
            # print(self.calls["alc"][i])
            for ind in range(self.lenElev):
                self.slides[ind].set(self.elevators[ind]._pos)      # the only change - after every simulation set to scale the position
            self.label['text'] = str(self.calls["dt"][i])
            time.sleep(0.1)
            self.root.update()

        self.calls.to_csv(self.outFile, index=False, header=None)

    def simulate(self):
        self.root.mainloop()

#self.root.mainloop()

def main(argc, argv):
    try:
        checkIfArgsCorrect(argc, argv)
        alg = SimulatorElev(argv[1], argv[2], argv[3])
        alg.simulate()
    except:
        print("thanks for simulating with us!")


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)