from tkinter import *
from tkinter.ttk import *
from asyncio import new_event_loop, run_coroutine_threadsafe, sleep, set_event_loop
from threading import Thread


def clone(widget):
    parent = widget.nametowidget(widget.winfo_parent())
    cls = widget.__class__

    clone_widget = cls(parent)
    for key in widget.configure():
        clone_widget.configure({key: widget.cget(key)})
    return clone_widget


class MainWindow(Tk):

    class SideWindow(Toplevel):
        def __init__(self):
            super().__init__()
            self.title('1')
            self.loop = None
            self.w = 400
            self.h = 300
            self.x = 250
            self.y = 150
            self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')

            self.Button = Button(self, text='点击监测轮抽\n否则关闭小窗', width=13, command=self.side_start)
            self.Button.pack()
            self.Button.place(x=0, y=0)

            self.mainloop()

        def side_start(self):
            self.Button.destroy()
            coroutine1 = self.checking()
            new_loop = new_event_loop()
            t = Thread(target=self.get_loop, args=(new_loop,))
            t.daemon = True
            t.start()
            run_coroutine_threadsafe(coroutine1, new_loop)

        def get_loop(self, loop):
            self.loop = loop
            set_event_loop(self.loop)
            self.loop.run_forever()

        async def checking(self):
            while True:
                await sleep(1)

    def __init__(self):
        super().__init__()
        self.title('佣兵模拟器')
        self.loop = None
        # 主窗口放使用教程
        self.w = 900
        self.h = 400
        self.x = 200
        self.y = 100
        self.geometry(f'{str(self.w)}x{str(self.h)}+{str(self.x)}+{str(self.y)}')

        self.Button = Button(self, text='开始监测', width=9, command=self.main_start)
        self.Button.pack()
        self.Button.place(x=70, y=335)

        self.side = []
        self.side.append(self.SideWindow())
        self.mainloop()

    def get_loop(self, loop):
        self.loop = loop
        set_event_loop(self.loop)
        self.loop.run_forever()

    async def co_run(self):
        await sleep(0.005)
        while True:
            await sleep(1)
            print('啊')


    def main_start(self):
        coroutine1 = self.co_run()
        new_loop = new_event_loop()
        t = Thread(target=self.get_loop, args=(new_loop,))
        t.daemon = True
        t.start()
        run_coroutine_threadsafe(coroutine1, new_loop)


if __name__ == '__main__':
    main = MainWindow()
