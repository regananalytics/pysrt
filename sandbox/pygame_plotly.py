import sys
import time
import keyboard

import pygame

from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay

from re2plot import main as plot_bytes

# fuschsia will serve as our colorkey for transparency
fuchsia = (255, 0, 128) 



def main(title:str):
    # Use the window title to create a window object
    win = Window.from_title(title, partial=True)
    # Create an overlay object for the window
    overlay = Overlay(win)
    # Set the transparency color to fuchsia
    overlay.set_transparency(colorkey=fuchsia)

    # Draw the plot on the screen
    def draw_func(ovly):
        # Draw a 5x5 grid centered at the window's center
        img = plot_bytes()
        # img = pygame.image.fromstring(img_bytes, (width, height), 'RGBA')
        img = pygame.image.load('./overlay.png')
        ovly.scr.blit(img, (0, 0))

    # Set the function to be called when the overlay is updated
    overlay.set_draw_func(draw_func)

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
    main(title)