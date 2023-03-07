from time import time
from threading import Thread, Lock

from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay



class SRT(Thread):

    def __init__(self, window_title, draw_func, 
        fps=10, colorkey=(0, 0, 0), partial_window_title=True
    ):
        super().__init__()
        self.win_title = window_title
        self.draw_func = draw_func
        self.colorkey = colorkey
        self.lock = Lock()
        self.stop_flag = False

        self.window = Window.from_title(window_title, partial=True)
        self.overlay = Overlay(self.window)
        self.overlay.set_transparency(colorkey=colorkey)

        self.overlay.set_draw_func(draw_func)

    
    def run(self):
        while not self.stop_flag:
