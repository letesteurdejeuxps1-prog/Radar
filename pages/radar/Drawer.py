import pygame

from pages.radar.Acft import Acft
from pages.radar.Qdm.Qdm import Qdm
from pages.radar.airspace.Point import Point
from pages.radar.data.helper import world_to_screen_x, world_to_screen_y


class Drawer:
    point_color: str = "W"

    color_default: tuple[int, int, int] = (255, 255, 255)

    font_size: int = 14

    icon_file_folder = "pages\\radar\\images"
    icon_file_format = ".png"

    icons_names: tuple = (
        'DME',
        'GNSS',
        'VOR/DME',
    )

    icon_default: str = 'UNKNOWN'

    label_offset_y = 2

    def __init__(self, surface: pygame.Surface, root_directory: str) -> None:
        self.conflict_color = (255, 0, 0)
        self.surface = surface
        self.root_directory = root_directory
        self.font = pygame.font.SysFont("consolas", self.font_size)

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
        start_x = int(world_to_screen_x(pos_x, offset_x, zoom))
        start_y = int(world_to_screen_y(pos_y, offset_y, zoom))
        pygame.draw.rect(
            self.surface,
            color,
            (start_x, start_y, width, height)
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
            border: int = 1
    ):
        start_x = int(world_to_screen_x(pos_x, offset_x, zoom))
        start_y = int(world_to_screen_y(pos_y, offset_y, zoom))

        rect = pygame.Rect(0, 0, width, height)
        rect.center = start_x, start_y
        pygame.draw.rect(
            self.surface,
            color,
            rect,
            border
        )

    def draw_circle_no_scale(
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
                int(world_to_screen_x(pos_x, offset_x, zoom)),
                int(world_to_screen_y(pos_y, offset_y, zoom))
            ),
            int(radius),
            width
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
        sx = int(world_to_screen_x(start_x, offset_x, zoom))
        sy = int(world_to_screen_y(start_y, offset_y, zoom))
        ex = int(world_to_screen_x(end_x, offset_x, zoom))
        ey = int(world_to_screen_y(end_y, offset_y, zoom))

        pygame.draw.line(
            self.surface,
            color,
            (sx, sy),
            (ex, ey),
            width
        )

    def draw_text(self, text, x, y, color=(255, 255, 255)):

        surf = self.font.render(
            str(text),
            True,
            color
        )

        rect = surf.get_rect(
            center=(x, y)
        )

        self.surface.blit(
            surf,
            rect
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
            pos_x = int(world_to_screen_x(point.pos_x, offset_x, zoom))
            pos_y = int(world_to_screen_y(point.pos_y, offset_y, zoom))
            rect = point.pygame_img.get_rect(center=(pos_x, pos_y))
            self.surface.blit(point.pygame_img, rect)

    def write_navaids_name(self, point: Point, offset_x: int | float, offset_y: int | float, zoom: int | float, font):
        txt = point.abbreviation.upper()
        if self.point_color == 'W':
            color = (255, 255, 255)
        elif self.point_color == 'B':
            color = (0, 0, 0)
        else:
            color = self.color_default
        pos_x = int(world_to_screen_x(point.pos_x, offset_x, zoom))
        pos_y = int(world_to_screen_y(point.pos_y, offset_y, zoom))
        txt_surface = font.render(txt, True, color)
        txt_rect = txt_surface.get_rect()
        txt_rect.centerx = pos_x
        txt_rect.top = pos_y + point.pygame_img.get_height() // 2 + self.label_offset_y

        self.surface.blit(txt_surface, txt_rect)

    def draw_acft(self, acft: Acft, offset_x: int | float, offset_y: int | float, zoom: int | float):

        self.draw_rect_centered(
            acft.pos_x,
            acft.pos_y,
            acft.d_acft_width,
            acft.d_acft_height,
            acft.get_color(),
            offset_x,
            offset_y,
            zoom
        )

        if acft.is_clicked:
            self.draw_circle_no_scale(
                acft.pos_x,
                acft.pos_y,
                acft.color_selected_radius,
                acft.selected_radius,
                offset_x,
                offset_y,
                zoom
            )

        self.draw_line(
            acft.pos_x,
            acft.pos_y,
            acft.prl_end_x,
            acft.prl_end_y,
            acft.get_color(),
            offset_x,
            offset_y,
            zoom
        )
        for pos in acft.old_pos[:-1]:
            self.draw_circle_no_scale(
                pos[0],
                pos[1],
                acft.color,
                acft.acft_trail_radius,
                offset_x,
                offset_y,
                zoom,
                0
            )

    def draw_conflict(
            self,
            conflict,
            offset_x,
            offset_y,
            zoom
    ):
        acft_1 = conflict[0]
        acft_2 = conflict[1]
        self.draw_line(
            acft_1[0],
            acft_1[1],
            acft_2[0],
            acft_2[1],
            self.conflict_color,
            offset_x,
            offset_y,
            zoom
        )

    def draw_qdm(self, qdm: Qdm, offset_x, offset_y, zoom):

        start_pos, end_pos = qdm.get_positions()

        start_x = start_pos[0]
        start_y = start_pos[1]

        if qdm.active:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            end_x = (
                            mouse_x + offset_x
                    ) / zoom

            end_y = -(
                    mouse_y + offset_y
            ) / zoom

        else:

            end_x = end_pos[0]
            end_y = end_pos[1]

        # =====================================
        # DRAW LINE
        # =====================================

        self.draw_line(
            start_x,
            start_y,
            end_x,
            end_y,
            qdm.color,
            offset_x,
            offset_y,
            zoom
        )

        # =====================================
        # SCREEN POSITIONS
        # =====================================

        sx = int(world_to_screen_x(
            start_x,
            offset_x,
            zoom
        ))

        sy = int(world_to_screen_y(
            start_y,
            offset_y,
            zoom
        ))

        ex = int(world_to_screen_x(
            end_x,
            offset_x,
            zoom
        ))

        ey = int(world_to_screen_y(
            end_y,
            offset_y,
            zoom
        ))

        # =====================================
        # CALCULATIONS
        # =====================================

        heading = qdm.get_heading()

        reciprocal = qdm.get_reciprocal_heading()

        distance = qdm.get_distance()

        # =====================================
        # MIDPOINT
        # =====================================

        mx = (sx + ex) // 2
        my = (sy + ey) // 2

        # =====================================
        # DRAW DISTANCE
        # =====================================

        self.draw_text(
            f"{distance:.1f}",
            mx,
            my - 10,
            qdm.color
        )

        # =====================================
        # DRAW HEADINGS
        # =====================================

        self.draw_text(
            f"{heading:03}",
            sx,
            sy - 15,
            qdm.color
        )

        self.draw_text(
            f"{reciprocal:03}",
            ex,
            ey - 15,
            qdm.color
        )
