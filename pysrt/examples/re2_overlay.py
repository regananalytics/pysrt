from pysrt.gui.widget import Widget, gauge_plot

class RE2ROverlay:

    c_fg = (251, 255, 254)
    c_bg = (0, 0, 0, 0)
    c_fine = (39, 145, 92)
    c_caution = (234, 160, 31)
    c_danger = (174, 12, 9)
    c_poison = (91, 15, 149)

    pad = 10
    height = 180
    l_width = 285
    r_width = 485


    def __init__(self):
        self.last_data = {}
        self.stats_widget = Widget(
            self.l_width + self.r_width + self.pad, self.height, 
            bg_color=self.c_bg, fg_color=self.c_fg
        )
        self.da_widget = Widget(
            self.l_width, self.height, 
            bg_color=self.c_bg, fg_color=self.c_fg
        )
        self.igt_widget = Widget(
            self.r_width, self.height/3, 
            bg_color=self.c_bg, fg_color=self.c_fg
        )
        self.hp_widget = Widget(
            self.r_width, self.height/3*2, 
            bg_color=self.c_bg, fg_color=self.c_fg
        )


    def update(self, data):
        # Calculate stats
        da = (data['da'] - 4000)/4000

        # draw update
        self.stats_widget.init_surf()

        # da widget
        self.da_widget.init_surf()
        da_gauge = gauge_plot(da, self.l_width, bar_color=self._da_color(da))
        write_text(self.da_widget.surface, 'DA', 0, 15, size=20)
        
        

    def _hp_color(self, hp, poisoned=False):
        if poisoned:
            return self.c_poison
        if hp > 800:
            return self.c_fine
        elif hp > 360:
            return self.c_caution
        else:
            return self.c_danger
        

    def _da_color(self, da):
        da_rank = self._da_rank(da)
        if da_rank > 7:
            return self.c_danger
        elif da_rank > 5:
            return self.c_caution
        else:
            return self.c_fine


    def _da_rank(self, da):
        return int(da/1000)