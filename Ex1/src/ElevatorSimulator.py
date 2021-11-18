import time
from threading import Thread

from ttkwidgets import TickScale
import tkinter as tk
from tkinter import ttk
from tkinter import *

from AlgoBest import AlgoBest


class SimulatorElev(AlgoBest):
    def __init__(self, build, calls, outFile):
        super().__init__(build, calls, outFile)
        self.min = self.building._minFloor
        self.max = self.building._maxFloor
        self.initSim()


    def initSim(self):
        self.slides = []
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        self.high = Frame(self.root)
        self.high.pack()
        self.low = Frame(self.root)
        self.low.pack(side=BOTTOM)
        self.mid = Frame(self.root)
        self.mid.pack(side=BOTTOM)

        self.style.configure('Vertical.TScale', sliderlength=60, background='white',
                        foreground='black', sliderwidth=50, font=11)
        for i in range(self.lenElev):
            s = TickScale(self.high, orient='vertical', style='Vertical.TScale',
                           tickinterval=1, from_=self.max, to=self.min, showvalue=True,
                           length=500, labelpos='e')
            s.set(0)
            label = Label(self.mid, text=str(i), width=5, font=10)
            label.pack(side=LEFT)
            self.slides.append(s)

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
                self.slides[ind].set(self.elevators[ind]._pos)
            time.sleep(0.015)
            self.root.update()

        self.calls.to_csv(self.outFile, index=False, header=None)

    def simulate(self):
        self.root.mainloop()

#self.root.mainloop()

def main(argc, argv):
    print(argc, argv)
    if (argc >=4):
        alg = SimulatorElev(argv[1], argv[2], argv[3])
        alg.simulate()
    # if (argc == 4):


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)