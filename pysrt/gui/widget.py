from math import pi, tan
import pygame
import pygame.gfxdraw

fg_color = (251, 255, 254)
bg_color = (0, 0, 0)

fine = (39, 145, 92)
caution = (234, 160, 31)
danger = (174, 12, 9)
poison = (91, 15, 149)

def write_text(surface, text, x, y, font='arial', size=12, justify='left', color=fg_color, bold=False):
    font = pygame.font.SysFont(font, size, bold)
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
    bar_color=(255, 0, 0), line_color=fg_color, bg_color=(0, 0, 0, 0)
):
    widget = pygame.Surface((w, h))
    widget.fill(bg_color)
    pygame.draw.rect(widget, bar_color, (0, 0, w*val/max, h))
    box_outline(widget, w, h, 0, 0, line_color, thickness)
    return widget


def gauge_plot(val, width=100, 
    ratio=0.25, thickness=2,
    bar_color=(255, 0, 0),
    line_color=fg_color,
    bg_color=(0, 0, 0)
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
        draw_aaarc(bar, r, r, r-thickness, bar_color, (0, 0, 0, 0), r*ratio-thickness-1)
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


pygame.init()
display = pygame.display.set_mode((1000, 200), pygame.NOFRAME)
display.fill(bg_color)

def update(da, hp, hp_max, poisoned=False, ehp=None, ehp_max=None):

    blank = pygame.Surface((1000, 200))
    blank.fill(bg_color)
    display.blit(blank, (0, 0))

    # DA
    da_ticks = [7000, 6000, 5000]
    if da > 7000:
        da_color = danger
    elif da > 5000:
        da_color = caution
    else:
        da_color = fine

    display.blit(gauge_plot((da-4000)/4000*100, 300, bar_color=da_color), (20, 30))
    write_text(display, 'DA', 20, 15, size=30)
    write_text(display, f'{da}', 170, 150, size=30, justify='center')
    write_text(display, f'{da/1000:.0f}', 170, 90, size=60, justify='center', color=caution, bold=True)

    write_text(display, 'IGT', 410, 15, size=30, justify='right')
    write_text(display, f'00:00:00', 535, 15, size=30, justify='right')
    # write_text(display, '▲', 610, 22, size=20, justify='right', color=danger)
    write_text(display, '▼', 610, 22, size=20, justify='right', color=fine)
    write_text(display, f'00:00', 675, 15, size=30, justify='right')
    write_text(display, f'00:00', 820, 15, size=30, justify='right', bold=False)

    # HP
    hp_ticks = [800, 360]
    if poisoned:
        hp_color = poison
    elif hp > hp_ticks[0]:
        hp_color = fine
    elif hp > hp_ticks[1]:
        hp_color = caution
    else:
        hp_color = danger

    display.blit(bar_plot(76, w=400, h=40 if ehp else 90, bar_color=hp_color, bg_color=bg_color), (430, 75))
    write_text(display, 'CHP', 410, 78 if ehp else 103, size=30, justify='right')
    write_text(display, f'{hp} / {hp_max}', 820, 78 if ehp else 103, size=30, justify='right')

    # EHP
    if ehp:
        display.blit(bar_plot(82, w=550, h=40, bar_color=danger, bg_color=bg_color), (430, 140))
        write_text(display, 'EHP', 410, 143, size=30, justify='right')
        write_text(display, f'{ehp} / {ehp_max}', 820, 143, size=30, justify='right')


while True:
    update(5230, 765, 1500, None, None)
    pygame.display.flip()
