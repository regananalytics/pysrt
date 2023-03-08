# Main application of pysrt
import keyboard
import time

from pysrt.srt import SRT
from pysrt.memcore.receiver import MemReceiver

from pysrt.games.re2r import draw


QUIT_STR = 'ctrl+shift+o'


def main():
    """Main function of pysrt"""
    srt = SRT(MemReceiver(host='localhost', port=5556, subs=''), 'Resident Evil 2', draw)
    srt.start()
    print(f'Press "{QUIT_STR}" to quit...')
    while True:
        if keyboard.is_pressed(QUIT_STR):
            break
    srt.stop()
    srt.join()


if __name__ == '__main__':
    main()