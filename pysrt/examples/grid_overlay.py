import sys
import keyboard

from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay
from pysrt.gui.grid import draw_grid

# fuschsia will serve as our colorkey for transparency
fuchsia = (255, 0, 128) 



def main(title:str):
    # Use the window title to create a window object
    win = Window.from_title(title, partial=True)
    # Create an overlay object for the window
    overlay = Overlay(win)
    # Set the transparency color to fuchsia
    overlay.set_transparency(colorkey=fuchsia)

    # Write a function to draw a grid on the overlay screen
    def draw_func(ovly):
        # Draw a 5x5 grid centered at the window's center
        w, h = win.xywh()[2:]
        draw_grid(ovly, 5, 5, w // 2, h // 2, w, h, 100, color=(255, 255, 255))

    # Set the function to be called when the overlay is updated
    overlay.set_draw_func(draw_func)

    print('Press "q" to quit...')

    # Finally, write the main loop to update the overlay each frame
    # until the user presses the 'q' key
    while True:
        overlay.update()
        if keyboard.is_pressed('q'):
            overlay.quit()
            break



if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        title = 'Visual Studio Code'
    else:
        title = args[0]
    main(title)