import pygame

from pages.radar.airspace.Point import Point
from pages.radar.data.helper import world_to_screen


class Drawer:

    point_color:str = "W"

    icon_file_folder = "pages\\radar\\images"
    icon_file_format = ".png"

    icons_names: tuple = (
        'DME',
        'GNSS',
        'VOR/DME',
    )

    icon_default: str = 'UNKNOWN'

    def __init__(self, surface: pygame.Surface, root_directory: str) -> None:
        self.surface = surface
        self.root_directory = root_directory

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
                world_to_screen(pos_x, offset_x, zoom),
                world_to_screen(pos_y, offset_y, zoom),
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
                world_to_screen(pos_x, offset_x, zoom),
                world_to_screen(pos_y, offset_y, zoom)
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
        sx = world_to_screen(start_x, offset_x, zoom)
        sy = world_to_screen(start_y, offset_y, zoom)
        ex = world_to_screen(end_x, offset_x, zoom)
        ey = world_to_screen(end_y, offset_y, zoom)

        pygame.draw.line(
            self.surface,
            color,
            (sx, sy),
            (ex, ey),
            width
        )

    def draw_icon(self, point: Point, offset_x: int | float, offset_y: int | float, zoom: int | float):
        if point.pygame_img is None:
            point.set_image_file(
                self.root_directory,
                self.icon_file_folder,
                self.point_color,
                self.icon_file_format,
            )

        if isinstance(point.pygame_img, pygame.Surface):
            pos_x = (point.pos_x * zoom) - offset_x
            pos_y = (point.pos_y * zoom) - offset_y
            self.surface.blit(point.pygame_img, (pos_x, pos_y))



        self.draw_circle(
            point.pos_x,
            point.pos_y,
            (255, 255, 255),
            5,
            offset_x,
            offset_y,
            zoom
        )
