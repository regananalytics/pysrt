# Main application of pysrt
from pysrt.gui.window import Window
from pysrt.gui.overlay import Overlay
from pysrt.memcore.receiver import MemReceiver

from pysrt.games.re2r import draw





def main():
    """Main function of pysrt"""
    # Create data producer thread
    receiver = MemReceiver(host='localhost', port=5556, subs='')
    receiver.start()

    # Create overlay application
    win = Window.from_title('Resident Evil 2', partial=True)
    overlay = Overlay(win)
    overlay.set_transparency(colorkey=(0, 0, 0))

    # Set the function to be called when the overlay is updated
    overlay.set_draw_func(draw)

    while True:
        start = time.time()



if __name__ == '__main__':
    main()