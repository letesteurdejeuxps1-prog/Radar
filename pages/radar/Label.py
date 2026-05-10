import pygame
from pygame import Rect


class Label:

    color_font: tuple[int, int, int] = (255, 255, 255)
    color_bg: tuple[int, int, int] = (0, 0, 0)

    height: int = 60
    width: int = 300

    rel_pos_x: int = 0
    rel_pos_y: int = 0

    padding: int = 2

    def __init__(self):
        self.font_height = 15
        self.rect_line_1 = None
        self.rect_line_2 = None
        self.font = pygame.font.SysFont("consolas", self.font_height)
        self.dragging = False
        self.build()

    def build(self):
        self.rect_line_1 = Rect(
            self.rel_pos_x + self.padding,
            self.rel_pos_y + self.padding,
            self.width - self.padding * 2,
            30
        )
        self.rect_line_2 = Rect(
            self.rel_pos_x + self.padding,
            self.rel_pos_y + self.padding,
            self.width - self.padding * 2,
            30
        )

    def update_data(self):
        pass

    def draw(self, surface: pygame.Surface, pos_x, pos_y, vals: dict):
        if not isinstance(self.rect_line_1, Rect):
            return

        spacer = "  "
        txt_1 = vals["cs"] + spacer + vals["wtc"]
        txt_2 = self.alt_to_label(vals["altitude_act"]) + spacer + str(vals["act_speed_gs"])

        line_1 = self.font.render(
            txt_1,
            True,
            self.color_font
        )
        line_2 = self.font.render(
            txt_2,
            True,
            self.color_font
        )

        calc_x = pos_x + self.rel_pos_x
        calc_y = pos_y + self.rel_pos_y

        surface.blit(
            line_1,
            (
                calc_x,
                calc_y
            )
        )

        surface.blit(
            line_2,
            (
                calc_x,
                calc_y + self.font_height
            )
        )

    def alt_to_label(self, value):
        level = value / 100
        return str(level)
