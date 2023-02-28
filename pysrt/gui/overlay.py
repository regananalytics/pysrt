import win32api
import win32con
import win32gui
import pygame

from . import fuchsia
from .window import Window



class Overlay:
    """
    Overlay Class

        The Overlay class is used to draw on top of a window, given the window's handle.
        The Overlay class uses the pygame library to draw on the surfeen, and uses the win32api
        library to set the window's transparency and position.

        This class initializes a pygame instance upon creation, and quits the pygame instance
        when the quit() method is called.

        To use this class, create an instance of the Overlay class, and call the set_draw_func()
        method to set the function to be called when the overlay is updated. The function
        should take one argument, the overlay object, and should draw on the overlay's surfeen.

        To update the overlay, call the update() method. This will call the draw function
        and update the overlay's position on the surfeen.
        The update method should be called in a loop, and when the loop exits, the quit()
        method should be used to terminate the pygame instance.
    """

    def __init__(self, window:Window, colorkey=None):
        # Initialize pygame
        # TODO: This should eventually be pulled out of this class and into the main program
        pygame.init()
        # The window argument should be an instance of the Window class in pysrt.gui.window
        self.win = window
        # To make this an overlay,
        #   Initialize the overlay with the same dimensions as the window it will be overlaying
        #   Turn off the overlay's frame so it isn't just a window.
        self.surf = pygame.display.set_mode(self.win.xywh()[2:], pygame.NOFRAME)
        # Set the transparency color
        self.colorkey = fuchsia if colorkey is None else colorkey
        # And make the window transparent
        self.set_transparency()


    @property
    def h(self):
        """The overlay's window handle"""
        return pygame.display.get_wm_info()['window']


    def set_draw_func(self, func):
        """Set the function to be called when the overlay is updated"""
        if func:
            self.draw_func = func
        else:
            # Initially we can set this to a function that does nothing
            self.draw_func = lambda *_, **__: None


    def update(self, *args, **kwargs):
        """Update the overlay
        
        This method should be called in a loop to update the overlay each frame.
        """
        self.update_pos()
        self.fill(self.colorkey)
        self.draw_func(self, *args, **kwargs)
        pygame.display.update()
        

    def set_transparency(self, colorkey=None):
        """Set the transparency color and alpha value"""
        if colorkey:
            self.colorkey = colorkey
        # Using the colorkey, set the window to be transparent
        #   This is done using the win32api library by setting the window's extended style
        win32gui.SetWindowLong(self.h, 
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(self.h, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
        )
        win32gui.SetLayeredWindowAttributes(self.h, win32api.RGB(*self.colorkey), 0, win32con.LWA_COLORKEY)


    def update_pos(self):
        """Update the position of the overlay to match the main window's position"""
        win32gui.SetWindowPos(self.h, -1, self.win.rect()[0], self.win.rect()[1], 0, 0, 0x0001)


    def quit(self):
        """Quit the overlay and pygame instances"""
        pygame.quit()


    ## Low-Level Drawing Functions

    def fill(self, color):
        """Fill the overlay with a color"""
        self.surf.fill(color)

    def draw_vline(self, x, h, color=(255, 255, 255)):
        """Draw a vertical line at some x coordinate
            Lines are drawn relative to the window's top left corner.
        """
        pygame.draw.line(self.surf, color, (x, 0), (x, h))

    def draw_hline(self, y, w, color=(255, 255, 255)):
        """Draw a horizontal line at some y coordinate
            Lines are drawn relative to the window's top left corner.
        """
        pygame.draw.line(self.surf, color, (0, y), (w, y))

    def draw_rect(self, rect, color=(255, 255, 255)):
        """Draw a rectangle
            Rectangles are drawn relative to the window's top left corner.
        """
        pygame.draw.rect(self.surf, rect, color)

    def draw_text(self, text, pos, color=(255, 255, 255)):
        """Draw text
            Text is drawn relative to the window's top left corner.
        """
        self.surf.blit(self.font.render(text, True, color), pos)
        
    def draw_arc(self, rect, start, end, color=(255, 255, 255)):
        """Draw an arc
            Arcs are drawn relative to the window's top left corner.
        """
        pygame.draw.arc(self.surf, color, rect, start, end)

