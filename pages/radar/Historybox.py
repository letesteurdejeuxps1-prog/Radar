import pygame
from pygame import Surface

from pages.Variables import Variables


class Historybox:
    padding_x: int = 20
    padding_y: int = 5
    max_lines: int = 5

    color_text = (255, 255, 255)

    def __init__(self, surface: Surface, variables: Variables):
        self.command_list = []
        self.surface = surface
        self.variables = variables
        self.font = pygame.font.SysFont("consolas", 18)

    def draw(self):
        lines = self.command_list[-self.max_lines:]
        y = self.variables.display_height - self.padding_y

        for line in reversed(lines):
            if not isinstance(line, str):
                continue
            txt_surface = self.font.render(
                line,
                True,
                self.color_text
            )
            text_width = txt_surface.get_width()
            text_height = txt_surface.get_height()

            y -= text_height

            self.surface.blit(
                txt_surface,
                (
                    self.variables.display_width - text_width - self.padding_x,
                    y
                )
            )

            y -= self.padding_y

    def add_content(self, data: str):
        self.command_list.append(data)
        self.command_list = self.command_list[-self.max_lines:]