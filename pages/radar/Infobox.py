import pygame
from pygame import Rect, Surface

from pages.Variables import Variables


class Infobox:

    padding_x: int = 20
    padding_y: int = 5

    color_bg = (25, 25, 25)
    color_border = (255, 255, 255)

    color_text = (255, 255, 255)

    def __init__(self, surface: Surface, variables: Variables):

        self.font_size = 16
        self.color_font_conflict = (255, 0, 0)
        self.content = []
        self.surface = surface
        self.variables = variables
        self.font = pygame.font.SysFont("consolas", 18)

        self.pos_x: int = self.variables.display_width
        self.pos_y: int = 0

    def draw(self):

        height = self.pos_y
        width = 0
        content = []
        for line in self.content:

            txt_surface = self.font.render(
                line,
                True,
                self.color_font_conflict
            )

            content.append((txt_surface, height))
            height += txt_surface.get_height() + self.padding_y
            if txt_surface.get_width() > width:
                width = txt_surface.get_width()

        for item in content:
            data, height = item
            self.surface.blit(
                data,
                (self.variables.display_width - width, height)
            )

    def add_conflicts(self, data: tuple[str, str, float, float]):
        acft_1_cs, acft_2_cs, h_dist, v_dist = data
        self.content.append(f"{acft_1_cs} {acft_2_cs} : {round(h_dist, 2)}NM | {round(v_dist)}ft")

    def reset_conflicts(self):
        self.content = []
