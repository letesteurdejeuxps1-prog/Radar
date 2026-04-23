import pygame


class Drawer:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    def draw_rect(
        self,
        pos_x: int|float,
        pos_y: int|float,
        width: int|float,
        height: int|float,
        color: tuple[int, int, int],
        offset_x: int|float = 0,
        offset_y: int|float = 0,
        zoom: int|float = 0,
    ):
        pygame.draw.rect(
            self.surface,
            color,
            (
                (pos_x * zoom) + offset_x,
                (pos_y * zoom) + offset_y,
                width * zoom,
                height * zoom
            )
        )

    def draw_rect_centered(
        self,
        pos_x: int|float,
        pos_y: int|float,
        width: int|float,
        height: int|float,
        color: tuple[int, int, int]
    ):
        self.draw_rect(
            pos_x - width/2,
            pos_y - height/2,
            width,
            height,
            color
        )

    def draw_circle(
        self,
        pos_x: int|float,
        pos_y: int|float,
        color: tuple[int, int, int],
        radius: int|float,
        width: int = 3
    ):
        pygame.draw.circle(
            self.surface,
            color,
            (pos_x, pos_y),
            radius,
            width
        )

    def draw_line(
            self,
            start_x: int|float,
            start_y: int|float,
            end_x: int|float,
            end_y: int|float,
            color: tuple[int, int, int],
            width: int = 2
    ):
        pygame.draw.line(
            self.surface,
            color,
            (start_x, end_x),
            (start_y, end_y),
            width
        )

