from tkinter import *
import time


class StopWatch(Frame):

    def __init__(self, parent=None, **kw):
        Frame.__init__(self, parent, kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.e = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())

    def makeWidgets(self):
        l1 = Label(self, text='Stopwatch', font = ("Helvetica", 15))
        l1.pack(fill=X, expand=NO, pady=1, padx=2)

        self.e = Entry(self)
        self.e.pack(pady=2, padx=2)

        l = Label(self, textvariable=self.timestr, font = ("Helvetica", 15))
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=3, padx=2)

        l2 = Label(self, text='Splits/Laps', font = ("Helvetica", 15))
        l2.pack(fill=X, expand=NO, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.m = Listbox(self, selectmode=EXTENDED, height=14,
                         yscrollcommand=scrollbar.set)
        self.m.pack(side=LEFT, fill=BOTH, expand=10, pady=10, padx=10)
        scrollbar.config(command=self.m.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

    def _update(self):
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        hseconds = int((elap - minutes * 60.0 - seconds) * 100)
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)

    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self.laps = []
        self._setTime(self._elapsedtime)

    def Lap(self):
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.laps.append(self._setLapTime(tempo))
            self.m.insert(END, self.laps[-1])
            self.m.yview_moveto(1)
            self.lapmod2 = self._elapsedtime


def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)
    root.title("STOPWATCH")
    root.geometry("300x400")
    root['bg'] = "red"
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Start', font = ("Helvetica", 18), command=sw.Start).pack(side = LEFT)
    Button(root, text='Stop', font = ("Helvetica", 18),command=sw.Stop).pack(side=LEFT)
    Button(root, text='Lap', font = ("Helvetica", 18),command=sw.Lap).pack(side=RIGHT)
    Button(root, text='Reset', font = ("Helvetica", 18),command=sw.Reset).pack(side=RIGHT)

    root.mainloop()


if __name__ == '__main__':
    main()