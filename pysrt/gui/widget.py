from math import pi, tan
import pygame
import pygame.gfxdraw

GRID = False

pad = 10
height = 200
da_width = 285
hp_width = 485

fg_color = (251, 255, 254)
bg_color = (0, 0, 0)

fine = (39, 145, 92)
caution = (234, 160, 31)
danger = (174, 12, 9)
poison = (91, 15, 149)


class Widget:

    def __init__(self, width, height, pad=10, bg_color=(0, 0, 0), fg_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.pad = pad
        self.bg_color = bg_color
        self.fg_color = fg_color

    
    def init_surf(self):
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.bg_color)
        return self.surface


    def blit(self, surface, x, y):
        surface.blit(self.surface, (x, y))
        return surface


    




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


pygame.init()
display = pygame.display.set_mode((da_width + hp_width + pad*3, height-pad*2), pygame.NOFRAME)
display.fill(bg_color)

def update(da, hp, hp_max, poisoned=False, ehp=None, ehp_max=None):

    _height = height-pad*2
    _lg_font = _height/2.414
    _md_font = _height/5
    _sm_font = _height/5-pad
    

    # DA Calculations
    da_ticks = [7000, 6000, 5000]
    if da > 7000:
        da_color = danger
    elif da > 5000:
        da_color = caution
    else:
        da_color = fine
    da_val = (da-4000)/4000*100

    # HP Calculations
    hp_ticks = [800, 360]
    if poisoned:
        hp_color = poison
    elif hp > hp_ticks[0]:
        hp_color = fine
    elif hp > hp_ticks[1]:
        hp_color = caution
    else:
        hp_color = danger


    # Background
    bkgd = pygame.Surface((da_width + hp_width + pad*3, height-pad*2))
    bkgd.fill(bg_color)
    display.blit(bkgd, (0, 0))

    # DA Region
    da_region = pygame.Surface((da_width-2, _height-2))

    da_region.blit(gauge_plot(da_val, da_width-2, bar_color=da_color), (0, _height-(da_width/2+pad)))
    write_text(da_region, 'DA', 0, pad*1.5, size=_md_font)
    write_text(da_region, f'{da}', da_width/2+1, _height-_sm_font-pad/2, size=_sm_font, justify='center')
    write_text(da_region, f'{da/1000:.0f}', da_width/2+1, _height/2-pad*1.5, size=_lg_font, justify='center', color=caution, bold=True)

    display.blit(da_region, (pad+1, 1))

    if GRID:
        box_outline(display, da_width, height-pad*3, pad, pad, fg_color, 1)
        pygame.draw.line(display, fg_color, (da_width/2+pad, pad), (da_width/2+pad, height-pad*2), 1)
        pygame.draw.line(display, fg_color, (pad, (height-pad)/2), (da_width+pad-1, (height-pad)/2), 1)

    # HP Region
    hp_left = da_width+pad*2
    bar_width = hp_width/5*4 - pad
    bar_height = _height/3-pad*2
 
    hp_region = pygame.Surface((hp_width-2, _height-2))

    write_text(hp_region, 'IGT', hp_width/5-pad*1.5, pad*1.5, size=_md_font, justify='right')
    write_text(hp_region, f'00:00:00', hp_width/5+pad/2.5, pad*2, size=_md_font-pad/2, justify='left')
    write_text(hp_region, f'00:00', hp_width-pad*1.5, pad*2, size=_md_font-pad/2, justify='right', bold=False)

    # delta
    # write_text(hp_region, '▲', hp_width/2+pad*4.5, pad*2.25, size=_sm_font, justify='right', color=danger)
    write_text(hp_region, '▼', hp_width/2+pad*4.5, pad*2.25, size=_sm_font, justify='right', color=fine)
    write_text(hp_region, f'00:00', hp_width/2+pad*5, pad*2.25, size=_sm_font, justify=' ', color=fine)

    hp_region.blit(bar_plot(76, w=bar_width, h=bar_height, bar_color=hp_color, bg_color=bg_color), (hp_width/5, bar_height+pad*3))
    write_text(hp_region, 'CHP', hp_width/5-pad, bar_height+pad*3.5, size=_md_font, justify='right')
    write_text(hp_region, f'{hp} / {hp_max}', hp_width-pad*2, bar_height+pad*3.75+1, size=_sm_font, justify='right')

    hp_region.blit(bar_plot(82, w=bar_width, h=bar_height, bar_color=danger, bg_color=bg_color), (hp_width/5, bar_height*2+pad*5))
    write_text(hp_region, 'EHP', hp_width/5-pad, bar_height*2+pad*5.5, size=_md_font, justify='right')
    write_text(hp_region, f'{ehp} / {ehp_max}', hp_width-pad*2, bar_height*2+pad*5.75+1, size=_sm_font, justify='right')

    display.blit(hp_region, (hp_left+1, 1))

    if GRID:
        box_outline(display, hp_width, height-pad*3, pad*2+da_width, pad, fg_color, 1)
        pygame.draw.line(display, fg_color, (hp_left+hp_width/2, pad), (hp_left+hp_width/2, height-pad*2), 1)
        pygame.draw.line(display, fg_color, (hp_left, (height-pad)/2), (hp_left+hp_width+1, (height-pad)/2), 1)


while True:
    update(5230, 765, 1200, False, 855, 3500)
    pygame.display.flip()
