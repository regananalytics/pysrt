import win32gui


class Window:
    """
    Window Class

        The Window class is used to get information about a window, given the window's handle.
        The Window class uses the win32gui library to get information about the window.

        A Window instance can be generated from a window handle, 
        or from a window title using the from_title() class method.
    """

    def __init__(self, h):
        """Initialize the Window instance with a window handle"""
        self.h = h

    def rect(self):
        """Get the window's rectangle"""
        return win32gui.GetWindowRect(self.h)

    def center(self):
        """Get the window's center coordinates"""
        x, y, w, h = self.xywh()
        return x + w // 2, y + h // 2

    def xywh(self):
        """Get the window's x, y, width, and height"""
        rect = self.rect()
        x = rect[0]
        y = rect[1]
        return x, y, rect[2] - x, rect[3] - y

    @classmethod
    def from_title(cls, title:str, partial=False):
        """Get window instance by title
        
            The "partial" keyword argument can be used to match a substring of the window title 
            instead of the entire title. This is useful for matching windows with a title that
            includes a version number, such as "My Program v1.0.0" or changes during runtime.
        """
        return cls(cls.get_window_by_title(title, partial=partial))

    @classmethod
    def get_window_by_title(cls, title:str, partial=False):
        """Get window handle by title"""
        title = title.lower()
        # Callback to check window title
        def callback(hwin, hwins):
            if _title := win32gui.GetWindowText(hwin).lower():
                if partial and title in _title:
                    # Partial match, i.e. title arg is a substring
                    hwins.append(hwin)
                elif title == _title:
                    # Exact match
                    hwins.append(hwin)
        hwins = []
        win32gui.EnumWindows(callback, hwins)
        return hwins[0]
