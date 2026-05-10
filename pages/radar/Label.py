import pygame
from pygame import Rect


class Label:

    color_font: tuple[int, int, int] = (255, 255, 255)
    color_bg: tuple[int, int, int] = (0, 0, 0)

    height: int = 60
    width: int = 300

    rel_pos_x: int = 20
    rel_pos_y: int = -20

    padding: int = 2

    def __init__(self):
        self.font_height = 15
        self.rect_line_1 = None
        self.rect_line_2 = None
        self.font = pygame.font.SysFont("consolas", self.font_height)

        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.last_draw_x = 0
        self.last_draw_y = 0
        self.last_width = 0
        self.last_height = 0

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

        self.last_draw_x = calc_x
        self.last_draw_y = calc_y

        self.last_width = max(
            line_1.get_width(),
            line_2.get_width()
        )

        self.last_height = self.font_height * 2

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

        pygame.draw.rect(
            surface,
            (50, 50, 50),
            (
                calc_x - 2,
                calc_y - 2,
                self.last_width + 4,
                self.last_height + 4
            ),
            1
        )

        pygame.draw.line(
            surface,
            self.color_font,
            (pos_x, pos_y),
            (calc_x, calc_y + self.last_height // 2),
            1
        )

    def is_mouse_over(self, mouse_x, mouse_y):
        rect = pygame.Rect(
            self.last_draw_x,
            self.last_draw_y,
            self.last_width,
            self.last_height
        )

        return rect.collidepoint(mouse_x, mouse_y)

    def start_drag(self, mouse_x, mouse_y):
        self.dragging = True

        self.drag_offset_x = mouse_x - self.last_draw_x
        self.drag_offset_y = mouse_y - self.last_draw_y

    def stop_drag(self):
        self.dragging = False

    def drag(self, mouse_x, mouse_y, aircraft_screen_x, aircraft_screen_y):

        if not self.dragging:
            return

        new_x = mouse_x - self.drag_offset_x
        new_y = mouse_y - self.drag_offset_y

        self.rel_pos_x = new_x - aircraft_screen_x
        self.rel_pos_y = new_y - aircraft_screen_y

    def alt_to_label(self, value):
        level = value / 100
        return str(level)
