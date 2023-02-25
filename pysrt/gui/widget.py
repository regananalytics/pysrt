from math import pi, tan
import pygame


def outline(surface, w, h, x=0, y=0,
    line_color=(0, 0, 0), line_thick=2
):
    c = line_color; s = surface; t = line_thick
    pygame.draw.line(s, c, (x, y+h-t), (x+w-t, y+h-t), t)
    pygame.draw.line(s, c, (x,     y), (x,     y+h-t), t)
    pygame.draw.line(s, c, (x+w-t, y), (x+w-t, y+h-t), t)
    pygame.draw.line(s, c, (x,     y), (x+w-t,     y), t)
    return s


def bar_plot(val, max=100, 
    w=700, h=50,
    line_thick=2,
    bar_color=(255, 0, 0), 
    line_color=(0, 0, 0), 
    bg_color=(255, 255, 255)
):
    widget = pygame.Surface((w, h))
    widget.fill(bg_color)
    pygame.draw.rect(widget, bar_color, (0, 0, int(w*val/max), h))
    outline(widget, w, h, line_color=line_color, line_thick=line_thick)
    return widget


def arc_line(surface, w, h, x=0, y=0,
    line_color=(0, 0, 0), line_thick=2
):
    c = line_color; s = surface; t = line_thick
    pygame.draw.arc(s, c, (x, y, w, h), 0, pi, t)


def arc_filled(surface, w, h, x=0, y=0,
    ratio=0.2, color=(255, 0, 0), bg_color=(255, 255, 255),
    start=0, end=pi
):
    start = max(min(start, pi), 0)
    end = max(min(end, pi), 0)
    if start > end:
        start, end = end, start
    r = ratio
    pygame.draw.circle(surface, 
        color, 
        (int(w/2), int(w/2)), int(w/2), 
        draw_top_right=True if start > pi/2 else False, 
        draw_top_left=True if end < pi/2 else False
    )
    pygame.draw.circle(surface,
        bg_color,
        (int(w/2), int(w/2)), int(w/2*(1-r*2)),
        draw_top_right=True if start > pi/2 else False,
        draw_top_left=True if end < pi/2 else False
    )
    if start > 0 and start < pi/2:
        pygame.draw.polygon(surface, 
            bg_color,
            (
                (w/2, 0), 
                (w, 0), 
                (w, int(w/2*tan(start)))
            )
        )
    elif start > pi/2:
        pygame.draw.polygon(surface,
            bg_color,
            (
                (w/2, 0), 
                (0, 0), 
                (0, int(w/2*tan(start)))
            )
        )
    if end > 0 and end < pi/2:
        pygame.draw.polygon(surface,
            bg_color,
            (
                (w/2, 0), 
                (w/2, int(w/2*tan(end))), 
                (w, int(w/2*tan(end)))
            )
        )
    elif end > pi/2:
        pygame.draw.polygon(surface,
            bg_color,
            (
                (w/2, 0), 
                (w/2, int(w/2*tan(end))), 
                (0, int(w/2*tan(end)))
            )
        )


def gauge_plot(val, max=100,
    w=200, h=200, ratio=0.15,
    line_thick=4,
    bar_color=(255, 0, 0),
    line_color=(0, 0, 0),
    bg_color=(255, 255, 255)
):
    widget = pygame.Surface((w, h))
    widget.fill(bg_color)
    arc_filled(widget, w=w, h=w, ratio=ratio,
        color=bar_color, bg_color=bg_color,
        start=pi, end=pi - pi*(val/max)
    )
    arc_line(widget, w=w, h=w, 
        line_color=line_color, 
        line_thick=line_thick
    )
    arc_line(widget, 
        w=int(w*(1-2*ratio)), h=int(w*(1-2*ratio)),
        x=int(w*ratio), y=int(w*ratio),
        line_color=line_color, 
        line_thick=line_thick
    )
    pygame.draw.line(widget, line_color, 
        (0, int(w/2)), (int(w*ratio), int(w/2)), 
        line_thick
    )
    pygame.draw.line(widget, line_color, 
        (int(w*(1-ratio)), int(w/2)), (w, int(w/2)), 
        line_thick
    )
    return widget



pygame.init()
display = pygame.display.set_mode((1000, 200), pygame.NOFRAME)
display.fill((0, 0, 0))
display.blit(
    bar_plot(65, w=550, h=50, 
        line_color=(255, 255, 255), 
        bg_color=(0, 0, 0)), 
    (440, 70)
)
display.blit(
    bar_plot(82, w=550, h=50, 
        line_color=(255, 255, 255), 
        bg_color=(0, 0, 0)), 
    (440, 140)
)
display.blit(
    gauge_plot(82, w=300, h=200,
        line_color=(255, 255, 255),
        bg_color=(0, 0, 0)),
    (10, 40)
)


while True:
    pygame.display.update()