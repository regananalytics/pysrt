import pygame

from pysrt.gui.widget import gauge_plot, bar_plot, box_outline, write_text


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


def time_conv(nanoseconds):
    seconds = nanoseconds / 1e6
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))



def draw(data=None, igt=0, da=None, hp=None, hp_max=None, poisoned=None, ehp=None, ehp_max=None):

    # Parse Data
    if data:
        igt = time_conv(float(data['IGT']['IGT_Running_Timer'] 
            - data['IGT']['IGT_Cutscene_Timer'] 
            - data['IGT']['IGT_Pause_Timer']
        ))
        da = int(data['DA']['DA_Score'])
        hp = int(data['Player_HP']['Current_HP'])
        hp_max = int(data['Player_HP']['Max_HP'])
        poisoned = data['Player']['Poisoned']
        ehp = 0
        ehp_max = 100

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
    widget = pygame.Surface((da_width + hp_width + pad*3, height-pad*2))
    widget.fill(bg_color)
    # display.blit(bkgd, (0, 0))

    # DA Region
    da_region = pygame.Surface((da_width-2, _height-2))

    da_region.blit(gauge_plot(da_val, da_width-2, bar_color=da_color, bg_color=bg_color), (0, _height-(da_width/2+pad)))
    write_text(da_region, 'DA', 0, pad*1.5, size=_md_font)
    write_text(da_region, f'{da}', da_width/2+1, _height-_sm_font-pad/2, size=_sm_font, justify='center')
    write_text(da_region, f'{da/1000:.0f}', da_width/2+1, _height/2-pad*1.5, size=_lg_font, justify='center', color=caution, bold=True)

    widget.blit(da_region, (pad+1, 1))

    if GRID:
        box_outline(widget, da_width, height-pad*3, pad, pad, fg_color, 1)
        pygame.draw.line(widget, fg_color, (da_width/2+pad, pad), (da_width/2+pad, height-pad*2), 1)
        pygame.draw.line(widget, fg_color, (pad, (height-pad)/2), (da_width+pad-1, (height-pad)/2), 1)

    # HP Region
    hp_left = da_width+pad*2
    bar_width = hp_width/5*4 - pad
    bar_height = _height/3-pad*2
 
    hp_region = pygame.Surface((hp_width-2, _height-2))

    write_text(hp_region, 'IGT', hp_width/5-pad*1.5, pad*1.5, size=_md_font, justify='right')
    write_text(hp_region, f'{igt}', hp_width/5+pad/2.5, pad*1.5, size=_md_font, justify='left')
    # write_text(hp_region, f'00:00', hp_width-pad*1.5, pad*2, size=_md_font-pad/2, justify='right', bold=False)

    # delta
    # write_text(hp_region, '▲', hp_width/2+pad*4.5, pad*2.25, size=_sm_font, justify='right', color=danger)
    # write_text(hp_region, '▼', hp_width/2+pad*4.5, pad*2.25, size=_sm_font, justify='right', color=fine)
    # write_text(hp_region, f'00:00', hp_width/2+pad*5, pad*2.25, size=_sm_font, justify=' ', color=fine)

    hp_region.blit(
        bar_plot(
            hp, max=1200, w=bar_width, h=bar_height, 
            bar_color=hp_color, bg_color=bg_color,
            ticks=hp_ticks
        ), 
        (hp_width/5, bar_height+pad*3)
    )
    write_text(hp_region, 'CHP', hp_width/5-pad, bar_height+pad*3.5, size=_md_font, justify='right')
    write_text(hp_region, f'{hp} / {hp_max}', hp_width-pad*2, bar_height+pad*3.75-2, size=_sm_font, justify='right')

    ehp_val = ehp/ehp_max*100 if ehp and ehp_max else 0
    hp_region.blit(
        bar_plot(
            ehp_val, w=bar_width, h=bar_height, 
            bar_color=danger, bg_color=bg_color,
            ticks=[25, 50, 75]
        ), 
        (hp_width/5, bar_height*2+pad*5)
        )
    write_text(hp_region, 'EHP', hp_width/5-pad, bar_height*2+pad*5.5, size=_md_font, justify='right')
    write_text(hp_region, f'{ehp or 0} / {ehp_max or 100}', hp_width-pad*2, bar_height*2+pad*5.75-2, size=_sm_font, justify='right')

    widget.blit(hp_region, (hp_left+1, 1))

    if GRID:
        box_outline(widget, hp_width, height-pad*3, pad*2+da_width, pad, fg_color, 1)
        pygame.draw.line(widget, fg_color, (hp_left+hp_width/2, pad), (hp_left+hp_width/2, height-pad*2), 1)
        pygame.draw.line(widget, fg_color, (hp_left, (height-pad)/2), (hp_left+hp_width+1, (height-pad)/2), 1)

    return widget



if __name__ == '__main__':
    import keyboard

    DATA = True

    pygame.init()
    display = pygame.display.set_mode((da_width + hp_width + pad*3, height-pad*2))#, pygame.NOFRAME)
    display.fill(bg_color)

    if DATA:
        from pysrt.memcore.receiver import MemReceiver
        data_provider = MemReceiver()
        data_provider.start()

    while True:
        pygame.event.pump()
        data = data_provider.data if DATA else None
        if keyboard.is_pressed('ctrl+q'):
            break
        w = draw(
            data if DATA else None, 
            0, 4000, 1200, 1200, False, 100, 100
        )
        display.blit(w, (0, 0))
        pygame.display.flip()

    print('Done!')
