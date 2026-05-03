import pygame


class Drawer:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface

    def draw_rect(
            self,
            pos_x: int | float,
            pos_y: int | float,
            width: int | float,
            height: int | float,
            color: tuple[int, int, int],
            offset_x: int | float = 0,
            offset_y: int | float = 0,
            zoom: int | float = 0,
    ):
        pygame.draw.rect(
            self.surface,
            color,
            (
                (pos_x * zoom) - offset_x,
                (pos_y * zoom) - offset_y,
                width * zoom,
                height * zoom
            )
        )

    def draw_rect_centered(
            self,
            pos_x: int | float,
            pos_y: int | float,
            width: int | float,
            height: int | float,
            color: tuple[int, int, int],
            offset_x: int | float = 0,
            offset_y: int | float = 0,
            zoom: int | float = 0,
    ):
        print("TODO : update this function (Drawer draw_rect_centered to take zoom and offset into account")
        self.draw_rect(
            pos_x - width / 2,
            pos_y - height / 2,
            width,
            height,
            color
        )

    def draw_circle(
            self,
            pos_x: int | float,
            pos_y: int | float,
            color: tuple[int, int, int],
            radius: int | float,
            offset_x: int | float = 0,
            offset_y: int | float = 0,
            zoom: int | float = 0,
            width: int = 3
    ):
        pygame.draw.circle(
            self.surface,
            color,
            (
                (pos_x * zoom) - offset_x,
                (pos_y * zoom) - offset_y
            ),
            radius,
            int(width * zoom)
        )

    def draw_line(
            self,
            start_x: int | float,
            start_y: int | float,
            end_x: int | float,
            end_y: int | float,
            color: tuple[int, int, int],
            offset_x: int | float = 0,
            offset_y: int | float = 0,
            zoom: int | float = 0,
            width: int = 2
    ):
        sx = (start_x * zoom) - offset_x
        sy = (start_y * zoom) - offset_y
        ex = (end_x * zoom) - offset_x
        ey = (end_y * zoom) - offset_y
        pygame.draw.line(
            self.surface,
            color,
            (sx, sy),
            (ex, ey),
            width
        )
