import pygame


class Command:

    pos_x: int = 0
    pos_y: int = 0
    width: int = 200
    height: int = 100

    color_bg: tuple[int, int, int] = (100, 100, 100)
    color_border: tuple[int, int, int] = (200, 200, 200)
    color_font: tuple[int, int, int] = (255, 255, 255)


    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.rect: pygame.Rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def draw(self):
        self.draw_bg()
        self.draw_acft_name_box()
        self.draw_command_input()
        self.draw_prl_box()

    def draw_bg(self):
        pygame.draw.rect(
            self.surface,
            self.color_bg,
            self.rect,
        )
        pygame.draw.rect(
            self.surface,
            self.color_border,
            self.rect,
            2  # border thickness
        )

    def draw_acft_name_box(self):
        pass

    def draw_command_input(self):
        pass

    def draw_prl_box(self):
        pass