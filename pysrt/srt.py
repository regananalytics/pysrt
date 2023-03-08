import keyboard
import pygame
from time import sleep, time
from threading import Thread, Lock
from typing import Callable

from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay
from pysrt.memcore.receiver import MemReceiver



class SRT(Thread):

    def __init__(self, 
        data_provider:MemReceiver, 
        window_title:str, 
        draw_func:Callable, 
        fps=1, colorkey=(0, 0, 0), partial_window_title=True
    ):
        super().__init__()
        self.data_provider = data_provider

        self.win_title = window_title
        self.draw_func = draw_func
        self.colorkey = colorkey
        self.fps = fps

        self.lock = Lock()
        self.stop_flag = False

        # self.window = Window.from_title(window_title, partial=partial_window_title)
        # self.overlay = Overlay(self.window, colorkey=colorkey)

        # self.overlay.set_draw_func(draw_func)
        self.display = pygame.display.set_mode((800, 600))

    
    def run(self):
        self.data_provider.start()
        while not self.stop_flag:
            frame_start = time()
            for event in pygame.event.get(pump=True, exclude=(pygame.AUDIODEVICEADDED)):
                print(event.type)
                if event.type == pygame.QUIT:
                    self.stop_flag = True
            self.overlay.update(self.data_provider.data)
            print(f'{frame_start} -- {time() - frame_start}s')# -- {self.data_provider.data}')
            sleep(max(0, 1/self.fps - (time() - frame_start)))
        self._stop()

    
    def stop(self):
        self.stop_flag = True


    def _stop(self):
        self.data_provider.stop()
        self.data_provider.join()



if __name__ == '__main__':
    quitstr = 'ctrl+shift+o'

    from pysrt.games.re2r import draw
    srt = SRT(MemReceiver(), 'Resident Evil 2', draw)
    srt.start()
    print(f'Press "{quitstr}" to quit...')
    while True:
        if keyboard.is_pressed(quitstr):
            break
    srt.stop()
    srt.join()
    print('Done!')
