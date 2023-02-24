import pygame
from pygame.surface import Surface

from . import fuchsia


class Widget(Surface):

    def __init__(self, w, h, color=fuchsia):
        self.w = w
        self.h = h
        self.color = color


