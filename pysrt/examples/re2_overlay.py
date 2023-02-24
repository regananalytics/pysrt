from functools import wraps
import keyboard
import pygame
import sys
import time

from pysrt.gui.widget import Widget
from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay
from pysrt.gui.grid import draw_grid

# fuschsia will serve as our colorkey for transparency
fuchsia = (255, 0, 128) 

def time_draw(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'Draw took {time.time() - start} seconds')
        return result
    return wrapper


def init_widget(w, h, color=fuchsia):
    widget = pygame.Surface((w, h))
    widget.fill(color)
    return widget


def draw_bar_plot(surface, x, y, w, h, val, max, 
    bar_color=(255, 0, 0), line_color=(255, 255, 255), bg_color=fuchsia
):
    # Draw a bar plot
    # Bar
    pygame.draw.rect(surface, bar_color, (x, y, 100, 20))
    # Outline
    pygame.draw.line(surface, line_color, (x, y+h), (x+w, y+h))
    pygame.draw.line(surface, line_color, (x, y), (x, y+h))
    pygame.draw.line(surface, line_color, (x+w, y), (x+w, y+h))
    pygame.draw.line(surface, line_color, (x, y), (x+w, y))
    

@time_draw
def draw_func(overlay):
    draw_bar_plot(overlay.surf, 100, 50, 150, 20, 650, 1000)


def main(title:str, draw_func):
    # Use the window title to create a window object
    win = Window.from_title(title, partial=True)
    # Create an overlay object for the window
    overlay = Overlay(win)
    # Set the transparency color to fuchsia
    overlay.set_transparency(colorkey=fuchsia)

    # Create widget
    overlay.set_draw_func(draw_func)

    # Blit to overlay
    print('Press "q" to quit...')

    # Finally, write the main loop to update the overlay each frame
    # until the user presses the 'q' key
    while True:
        start = time.time()
        overlay.update()
        if keyboard.is_pressed('q'):
            overlay.quit()
            break
        time.sleep(max(0, 1/10 - (time.time() - start)))


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        title = 'Visual Studio Code'
    else:
        title = args[0]
    main(title, draw_func)
