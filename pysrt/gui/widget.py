from math import pi, tan
import pygame
import pygame.gfxdraw

fg_color = (255, 255, 255)
bg_color = (0, 0, 0)


def write_text(surface, text, x, y, font='arial', size=12, justify='left', color=fg_color, bold=False):
    font = pygame.font.SysFont(font, int(round(size)), bold)
    text = font.render(text, True, color)
    if justify == 'center':
        x -= text.get_width() // 2
    elif justify == 'right':
        x -= text.get_width()
    surface.blit(text, (x, y))
    return surface


def box_outline(surface, w, h, x=0, y=0, line_color=fg_color, thickness=2):
    c = line_color; s = surface; t = thickness
    pygame.draw.line(s, c, (x, y+h-t), (x+w-t, y+h-t), t)
    pygame.draw.line(s, c, (x,     y), (x,     y+h-t), t)
    pygame.draw.line(s, c, (x+w-t, y), (x+w-t, y+h-t), t)
    pygame.draw.line(s, c, (x,     y), (x+w-t,     y), t)
    return s


def draw_aapolygon(surf, points, color):
    i = lambda x: int(round(x))
    points = [(i(x), i(y)) for x, y in points]
    pygame.gfxdraw.aapolygon(surf, points, color)
    pygame.gfxdraw.filled_polygon(surf, points, color)


def draw_aacircle(surf, x, y, r, color):
    i = lambda x: int(round(x))
    pygame.gfxdraw.aacircle(surf, i(x), i(y), i(r), color)
    pygame.gfxdraw.filled_circle(surf, i(x), i(y), i(r), color)


def draw_aaarc(surf, x, y, r, color, bg_color, thickness=2):
    i = lambda x: int(round(x))
    draw_aacircle(surf, x, y, r, color)
    draw_aacircle(surf, x, y, r-thickness, bg_color)
    pygame.gfxdraw.filled_polygon(surf, 
        ((0, y), (2*x, y), (2*x, 2*y), (0, 2*y)), # Correct for angle
        bg_color
    )


def bar_plot(val, max=100, w=700, h=50, thickness=2,
    bar_color=(255, 0, 0), line_color=fg_color, bg_color=(0, 0, 0, 0),
    ticks=[], tick_ratio=0.2
):
    widget = pygame.Surface((w, h))
    widget.fill(bg_color)
    pygame.draw.rect(widget, bar_color, (0, 0, w*val/max, h))
    box_outline(widget, w, h, 0, 0, line_color, thickness)
    for t in ticks:
        pygame.draw.line(widget, line_color, (w*t/max, 0), (w*t/max, h*tick_ratio), thickness)
        pygame.draw.line(widget, line_color, (w*t/max, h), (w*t/max, h*(1-tick_ratio)-1), thickness)
    return widget


def gauge_plot(val, width=100, 
    ratio=0.25, thickness=2,
    bar_color=(255, 0, 0),
    line_color=fg_color,
    bg_color=(0, 0, 0),
    ticks=[]
):
    r = int(width/2)
    widget = pygame.Surface((width+1, width))
    widget.fill(bg_color)
    # Draw outline
    draw_aaarc(widget, r, r, r, line_color, bg_color, thickness)
    draw_aaarc(widget, r, r, r*(1-ratio), line_color, bg_color, thickness)
    pygame.draw.line(widget, line_color, (0, r), (r*ratio, r), thickness)
    pygame.draw.line(widget, line_color, (r*2, r), (r*(2-ratio), r), thickness)
    # Draw bar
    if val > 0:
        bar = pygame.Surface((width+1, width), pygame.SRCALPHA)
        draw_aaarc(bar, r, r, r-thickness, bar_color, (0, 0, 0, 0), r*ratio-thickness)
        bg_poly = lambda points: draw_aapolygon(bar, points, (0, 0, 0, 0))
        t = pi*(1-val/100)
        if val >= 100:
            pass
        elif val >= 75:
            bg_poly(((r, r), (2*r, r), (2*r, r*(1-tan(t)))))
        elif val > 50:
            t = pi/2-t
            bg_poly(((r, r), (2*r, r), (2*r, 0)))
            bg_poly(((r, r), (2*r, 0), (r*(1+tan(t)), 0)))
        else:
            bg_poly(((r, r), (2*r, r), (2*r, 0), (r, 0)))
            if val > 25:
                t = pi/2-t
                bg_poly(((r, r), (r, 0), (r*(1+tan(t)), 0)))
            else:
                t = pi-t
                bg_poly(((r, r), (r, 0), (0, 0)))
                bg_poly(((r, r), (0, 0), (0, r*(1-tan(t)))))
    widget.blit(bar, (0, 0))
    # Draw ticks
    return widget
