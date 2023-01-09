from .overlay import Overlay


def draw_cross(overlay:Overlay, x, y, w, h, color=(255, 255, 255)):
    """Draw cross lines centered at x, y"""
    # Vertical line at x
    overlay.draw_vline(x, h, color)
    # Horizontal line at y
    overlay.draw_hline(y, w, color)


# Draw a grid centered at x, y, with a given spacings dh, dv
def draw_grid(overlay:Overlay, nh, nv, x, y, w, h, dh, dv=None, color=(255, 255, 255)):
    """Draw a grid centered at x, y, with a given spacings dh, dv"""
    if dv is None:
        dv = dh
    # Central lines
    draw_cross(overlay, x, y, w, h, color)
    # Horizontal lines around y
    for i in range(1, nv // 2 + 1):
        overlay.draw_hline(y + i * dv, w, color)
        overlay.draw_hline(y - i * dv, w, color)
    # Vertical lines around x
    for i in range(1, nh // 2 + 1):
        overlay.draw_vline(x + i * dh, h, color)
        overlay.draw_vline(x - i * dh, h, color)


