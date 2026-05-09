import json
import math
import pathlib
import pygame

from pages.Variables import Variables
from pages.radar.Acft import Acft
from pages.radar.Airspace import Airspace
from pages.radar.Drawer import Drawer
from pages.radar.data.helper import world_to_screen_x, world_to_screen_y


class Main:
    acft_list: list[Acft] = []
    acft_detect_buffer: int = 20

    font = None

    game_acft_id_counter: int = 1
    game_acft_selected_id: int = 0

    main_clock: pygame.time.Clock = pygame.time.Clock()
    main_running: bool = False
    radar_acft_refresh_rate_counter: int = 1

    left_click_on: bool = False
    middle_click_on: bool = False
    right_click_on: bool = False

    path_airspace_file: str = 'horn.json'
    path_airspace_folder: str = 'airspaces'
    path_root: str = ''

    radar_color_bg: tuple[int, int, int] = (0, 0, 0)
    radar_center_lon: int|float = 0
    radar_center_lat: int|float = 0

    radar_show_navaids_name: bool = True
    radar_refresh_rate: int = 5
    radar_selected: Acft | None = None

    default_zoom: int | float = 1
    zoom: int | float = 1
    zoom_increment: float = 0.1
    cam_offset_x: int | float = 0
    cam_offset_y: int | float = 0
    cam_center_x: int | float = 0
    cam_center_y: int | float = 0
    cam_offset_increment: int = 10

    def __init__(self, v: Variables, working_dir: str) -> None:
        self.root_directory = working_dir
        self.main_running = True
        self.main_counter = 0
        self.variables = v
        self.airspace = Airspace()
        self.path_root = str(pathlib.Path().resolve())
        self.init()
        info = pygame.display.Info()
        self.variables.display_width = info.current_w
        self.variables.display_height = info.current_h
        self.main_surface = pygame.display.set_mode((self.variables.display_width, self.variables.display_height))
        self.drawer = Drawer(self.main_surface, self.root_directory)
        self.after_init()

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption(self.variables.game_caption)
        center = self.airspace.load("{}\\{}\\{}".format(
            self.path_root,
            self.path_airspace_folder,
            self.path_airspace_file
        ))
        self.radar_center_lon = center[0]
        self.radar_center_lat = center[1]
        self.variables.display_width_half = self.variables.display_width // 2
        self.variables.display_height_half = self.variables.display_height // 2
        self.font = pygame.font.SysFont("consolas", 14)
        self.test_init()

    def after_init(self):
        match_center: tuple[int | float, int | float] | bool = False
        search_data = str(self.airspace.center)
        for point in self.airspace.points:
            if search_data.lower() == point.name.lower() or search_data.lower() == point.abbreviation.lower():
                match_center = (point.pos_x, point.pos_y)
        if isinstance(match_center, tuple):
            self.cam_center_x = match_center[0]
            self.cam_center_y = match_center[1]
            self.default_zoom = self.airspace.default_zoom
            self.zoom = self.default_zoom
        else:
            self.cam_offset_x = 0
            self.cam_offset_y = 0
            self.zoom = self.default_zoom
        self.reset_camera()

    def test_init(self):
        file = "{}\\airspaces\\test_acft_loader_2.json".format(self.root_directory)
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)
            for acft in data["acft"]:
                new_acft = Acft(
                    self.radar_center_lon,
                    self.radar_center_lat,
                    acft['identity'],
                    acft['cs'],
                    acft['coord_x'],
                    acft['coord_y'],
                    acft['heading_act'],
                    acft['heading_req'],
                    acft['turn_direction'],
                    acft['altitude_act'],
                    acft['altitude_req'],
                    acft['req_speed_kts'],
                    acft['act_speed_kts'],
                    acft['speed_increment'],
                    acft['ssr'],
                    acft['route'],
                    (acft['color'], acft['color'], acft['color']),
                    (acft['color_selected_radius'], acft['color_selected_radius'], acft['color_selected_radius']),
                    acft['color_wake_radius'],
                    acft['wtc'],
                    acft['selected_radius'],
                    acft['is_clicked'],
                )
                self.acft_list.append(new_acft)

    def test(self):
        pass

    def draw(self):
        self.draw_airspace()
        self.draw_acft()

    def draw_airspace(self):
        for area in self.airspace.areas:
            old_coord = ()
            new_coord = ()
            origin = ()
            for coord in area.coordinates_converted:
                if len(old_coord) == 0:
                    origin = coord
                    old_coord = coord
                else:
                    new_coord = coord
                    self.drawer.draw_line(
                        old_coord[0],
                        old_coord[1],
                        new_coord[0],
                        new_coord[1],
                        (155, 155, 155),
                        self.cam_offset_x,
                        self.cam_offset_y,
                        self.zoom
                    )
                    old_coord = new_coord
            self.drawer.draw_line(
                origin[0],
                origin[1],
                new_coord[0],
                new_coord[1],
                (155, 155, 155),
                self.cam_offset_x,
                self.cam_offset_y,
                self.zoom
            )

        for point in self.airspace.points:
            self.drawer.draw_icon(
                point,
                self.cam_offset_x,
                self.cam_offset_y,
                self.zoom
            )
            if self.radar_show_navaids_name:
                self.drawer.write_navaids_name(
                    point,
                    self.cam_offset_x,
                    self.cam_offset_y,
                    self.zoom,
                    self.font
                )

    def draw_acft(self):
        for acft in self.acft_list:
            self.drawer.draw_acft(
                acft,
                self.cam_offset_x,
                self.cam_offset_y,
                self.zoom
            )

    def test_draw(self):
        pass

    def run(self) -> None:
        while self.main_running:
            self.update_counter()
            self.main_surface.fill(self.radar_color_bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_event_key_down(event.key)
                elif event.type == pygame.MOUSEWHEEL:
                    self.handle_event_scroll(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_event_mouseclick(event)
                elif event.type == pygame.MOUSEMOTION:
                    if self.middle_click_on or self.right_click_on:
                        self.handle_event_mouse_middle_click_drag(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_event_mouseclick_off()

            # TODO REMOVE TEST FUNCTION
            self.test()
            self.test_draw()
            if self.radar_acft_refresh_rate_counter == 0:
                self.move_acft()
            self.draw()
            pygame.display.flip()
            self.main_clock.tick(self.variables.display_fps)

        pygame.quit()

    def handle_event_scroll(self, event):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # 2. Convert mouse position to world coordinates BEFORE zoom
        world_x = (mouse_x + self.cam_offset_x) / self.zoom
        world_y = (mouse_y + self.cam_offset_y) / self.zoom

        # 3. Apply zoom
        zoom_factor = 1.1 if event.y > 0 else 0.9
        self.zoom *= zoom_factor

        # Optional: clamp zoom
        self.zoom = max(0.1, min(self.zoom, 600000000))

        # 4. Recalculate offset so the world point stays under the mouse
        self.cam_offset_x = world_x * self.zoom - mouse_x
        self.cam_offset_y = world_y * self.zoom - mouse_y

    def handle_event_mouseclick(self, event):
        if event.button == 1:
            # Left click
            self.left_click_on = True
            mouse_x, mouse_y = pygame.mouse.get_pos()

            matches = []

            for acft in self.acft_list:

                screen_x = world_to_screen_x(acft.pos_x, self.cam_offset_x, self.zoom)

                screen_y = world_to_screen_y(acft.pos_y, self.cam_offset_y, self.zoom)

                if screen_x - self.acft_detect_buffer <= mouse_x <= screen_x + self.acft_detect_buffer:
                    if screen_y - self.acft_detect_buffer <= mouse_y <= screen_y + self.acft_detect_buffer:
                        matches.append((acft, screen_x, screen_y))

            if len(matches) == 0:
                self.radar_selected = None
            elif len(matches) == 1 and isinstance(matches[0][0], Acft):
                self.radar_selected = matches[0][0]
                matches[0][0].is_clicked = True
            elif len(matches) >= 2:
                match_dist = self.acft_detect_buffer * 10
                found = None
                for acft in matches:
                    distance = math.hypot(mouse_x - acft[1], mouse_y - acft[2])
                    if distance < match_dist:
                        found = acft[0]
                        match_dist = distance
                self.radar_selected = found
                found.is_clicked = True

        if event.button == 2:
            # Middle click
            self.middle_click_on = True
        if event.button == 3:
            # Right click
            print("Right click")
            self.right_click_on = True

    def handle_event_mouseclick_off(self):
        self.left_click_on = False
        self.middle_click_on = False
        self.right_click_on = False

    def handle_event_mouse_middle_click_drag(self, event):
        if isinstance(event.rel, tuple) and len(event.rel) == 2:
            self.cam_offset_x -= event.rel[0]
            self.cam_offset_y -= event.rel[1]

    def handle_event_key_down(self, key_pressed):
        if key_pressed == pygame.K_q:
            self.main_running = False
        elif key_pressed == pygame.K_KP_PLUS:
            self.zoom += self.zoom_increment
        elif key_pressed == pygame.K_KP_MINUS:
            self.zoom -= self.zoom_increment
        elif key_pressed == pygame.K_DOWN:
            self.cam_offset_y -= self.cam_offset_increment
        elif key_pressed == pygame.K_UP:
            self.cam_offset_y += self.cam_offset_increment
        elif key_pressed == pygame.K_LEFT:
            self.cam_offset_x -= self.cam_offset_increment
        elif key_pressed == pygame.K_RIGHT:
            self.cam_offset_x += self.cam_offset_increment
        elif key_pressed == pygame.K_c:
            self.reset_camera()

    def reset_camera(self):
        self.zoom = self.default_zoom
        self.cam_offset_x = self.cam_center_x * self.zoom - self.variables.display_width_half
        self.cam_offset_y = -self.cam_center_y * self.zoom - self.variables.display_height_half

    def update_counter(self) -> None:
        self.radar_acft_refresh_rate_counter += 1
        # TODO remove to prevent update on every tick
        if True: #self.main_second_counter >= self.variables.display_fps * self.radar_refresh_rate:
            self.radar_acft_refresh_rate_counter = 0

    def move_acft(self):
        if self.radar_selected is not None:
            identity = self.radar_selected.identity
        else:
            identity = None
        for acft in self.acft_list:
            acft.tick(identity)
