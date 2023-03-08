import keyboard
import subprocess
import time
import zmq

from pysrt.gui.overlay import Overlay
from pysrt.gui.window import Window
from pysrt.gui import fuchsia, widget

# Write a function to draw a grid on the overlay screen
def draw_func(ovly, data=None):
    if data:
        da = data['DA']['DA_Score']
        hp = data['Player_HP']['Current_HP']
        hp_max = data['Player_HP']['Max_HP']
        poisoned = False#data['player_hp']['poisoned']
        ehp = None#data['enemy_hp'][0]['current_hp']
        ehp_max = None#data['enemy_hp'][0]['max_hp']
    else:
        da = 5250
        hp = 0
        hp_max = 0
        poisoned = False
        ehp = None
        ehp_max = None
    w = widget.update(
        da, hp, hp_max, 
        poisoned=poisoned, ehp=ehp, ehp_max=ehp_max,
        bg_color=(0, 0, 0)
    )
    ovly.surf.blit(w, (0, 0))


if __name__ == '__main__':

    framerate = 1/10
    title = 'resident evil 2'

    # Use the window title to create a window object
    win = Window.from_title(title, partial=True)
    # Create an overlay object for the window
    overlay = Overlay(win)
    # Set the transparency color to fuchsia
    overlay.set_transparency(colorkey=(0, 0, 0))

    # Set the function to be called when the overlay is updated
    overlay.set_draw_func(draw_func)

    print('Press "ctrl+shift+o" to quit...')


    # Finally, write the main loop to update the overlay each frame
    # until the user presses the 'q' key
    while True:
        start = time.time()
        # string = socket.recv_string()
        # data = json.loads(string)
        overlay.update()#data)
        if keyboard.is_pressed('ctrl+shift+o'):
            overlay.quit()
            break
        time.sleep(max(0, framerate - (time.time() - start)))
