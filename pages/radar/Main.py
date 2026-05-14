import json
import math
import pathlib
import pygame

from pages.Variables import Variables
from pages.radar.Acft import Acft
from pages.radar.Airspace import Airspace
from pages.radar.Command import Command
from pages.radar.Drawer import Drawer
from pages.radar.PerformanceData import PerformanceData
from pages.radar.Qdm.Qdm import Qdm
from pages.radar.Qdm.QdmAnchor import QdmAnchor
from pages.radar.data.command_helper import get_command
from pages.radar.data.helper import world_to_screen_x, world_to_screen_y, get_wake_sep


class Main:
    acft_list: list[Acft] = []
    acft_detect_buffer: int = 20
    acft_conflict_list = []

    command_box: Command

    font = None

    game_acft_id_counter: int = 1
    game_acft_selected_id: int = 0

    last_acft_update_time: int = 0
    acft_update_interval_ms: int = 4000

    main_clock: pygame.time.Clock = pygame.time.Clock()
    main_running: bool = False

    left_click_on: bool = False
    middle_click_on: bool = False
    right_click_on: bool = False

    path_airspace_file: str = 'horn.json'
    path_airspace_folder: str = 'airspaces'
    path_root: str = ''

    qdm_list: list[Qdm] = []

    radar_color_bg: tuple[int, int, int] = (0, 0, 0)
    radar_center_lon: int | float = 0
    radar_center_lat: int | float = 0

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
        pygame.init()
        self.root_directory = working_dir
        self.main_running = True
        self.main_counter = 0
        self.variables = v
        self.airspace = Airspace()
        self.path_root = str(pathlib.Path().resolve())
        info = pygame.display.Info()
        self.variables.display_width = info.current_w
        self.variables.display_height = info.current_h
        self.perf_data = PerformanceData(self.root_directory)
        self.init()
        self.main_surface = pygame.display.set_mode((self.variables.display_width, self.variables.display_height))
        self.drawer = Drawer(self.main_surface, self.root_directory)
        self.command_box = Command(self.main_surface)
        self.after_init()

    def init(self) -> None:
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
                    self.perf_data,
                    acft['identity'],
                    acft['cs'],
                    acft['type'],
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
                    acft['selected_radius'],
                    acft['is_clicked'],
                )
                self.acft_list.append(new_acft)

    def test(self):
        pass

    def draw(self):
        self.draw_airspace()
        self.draw_conflicts()
        self.draw_acft()
        self.draw_qdm()
        self.command_box.draw()

    def draw_conflicts(self):
        for conflict in self.acft_conflict_list:
            self.drawer.draw_conflict(
                conflict,
                self.cam_offset_x,
                self.cam_offset_y,
                self.zoom
            )

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

            if not acft.d_prl_has_custom:
                acft.d_prl_length_in_sec = self.command_box.global_prl_length

            self.drawer.draw_acft(
                acft,
                self.cam_offset_x,
                self.cam_offset_y,
                self.zoom
            )
            screen_x = world_to_screen_x(
                acft.pos_x,
                self.cam_offset_x,
                self.zoom
            )

            screen_y = world_to_screen_y(
                acft.pos_y,
                self.cam_offset_y,
                self.zoom
            )

            acft.draw_label(
                self.main_surface,
                screen_x,
                screen_y
            )

    def test_draw(self):
        pass

    def run(self) -> None:
        while self.main_running:
            self.main_surface.fill(self.radar_color_bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_event_key_down(event)
                elif event.type == pygame.MOUSEWHEEL:
                    self.handle_event_scroll(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_event_mouseclick(event)
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_event_mouseclick_off()
                    self.command_box.handle_mouse_release()

            # TODO REMOVE TEST FUNCTION
            self.test()
            self.test_draw()
            dt = self.main_clock.get_time() / 1000
            self.move_acft(dt)
            ct = pygame.time.get_ticks()
            if ct - self.last_acft_update_time >= self.acft_update_interval_ms:
                self.detect_conflicts()
                for acft in self.acft_list:
                    acft.radar_refresh()
                self.last_acft_update_time = ct
            self.draw()
            pygame.display.flip()
            self.main_clock.tick(self.variables.display_fps)

        pygame.quit()

    def handle_event_scroll(self, event):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        world_x = (mouse_x + self.cam_offset_x) / self.zoom
        world_y = -(mouse_y + self.cam_offset_y) / self.zoom

        zoom_factor = 1.1 if event.y > 0 else 0.9

        self.zoom *= zoom_factor

        self.zoom = max(0.1, min(self.zoom, 500))

        self.cam_offset_x = world_x * self.zoom - mouse_x
        self.cam_offset_y = -world_y * self.zoom - mouse_y

    def handle_event_mouseclick(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        handle_mouse_result = self.command_box.handle_mouse_click((mouse_x, mouse_y), self.acft_list)
        if handle_mouse_result:
            return
        if event.button == 1:
            # Left click
            self.left_click_on = True

            matches = []

            qdm, endpoint = self.get_qdm_endpoint_at_mouse(
                mouse_x,
                mouse_y
            )
            if qdm is not None:
                if endpoint == "start":
                    qdm.pickup_start()
                elif endpoint == "end":
                    qdm.pickup_end()
                return

            for qdm in self.qdm_list:
                if qdm.active:
                    anchor = self.get_anchor_from_mouse(
                        mouse_x,
                        mouse_y
                    )
                    qdm.place_anchor(anchor)

                    return

            for acft in self.acft_list:

                if acft.label.is_mouse_over(mouse_x, mouse_y):
                    acft.label.start_drag(mouse_x, mouse_y)
                    return

                screen_x = world_to_screen_x(acft.pos_x, self.cam_offset_x, self.zoom)

                screen_y = world_to_screen_y(acft.pos_y, self.cam_offset_y, self.zoom)

                if screen_x - self.acft_detect_buffer <= mouse_x <= screen_x + self.acft_detect_buffer:
                    if screen_y - self.acft_detect_buffer <= mouse_y <= screen_y + self.acft_detect_buffer:
                        matches.append((acft, screen_x, screen_y))

            if len(matches) == 0:
                self.radar_selected = None
                self.command_box.set_selected_acft(
                    self.radar_selected
                )
            elif len(matches) == 1 and isinstance(matches[0][0], Acft):
                self.radar_selected = matches[0][0]
                self.command_box.set_selected_acft(
                    self.radar_selected
                )
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
                self.command_box.set_selected_acft(
                    self.radar_selected
                )
                found.is_clicked = True

        if event.button == 2:
            # Middle click
            self.middle_click_on = True
        if event.button == 3:
            # Right click
            print("Right click")
            self.right_click_on = True

            # =========================
            # REMOVE QDM
            # =========================
            qdm = self.get_qdm_at_mouse(
                mouse_x,
                mouse_y
            )
            if qdm is not None:
                self.qdm_list.remove(qdm)
                return

            # =========================
            # LABEL STATE CHANGE
            # =========================
            for acft in self.acft_list:
                if acft.label.is_mouse_over(
                        mouse_x,
                        mouse_y
                ):
                    acft.label.next_state()
                    return

    def handle_event_mouseclick_off(self):
        self.left_click_on = False
        self.middle_click_on = False
        self.right_click_on = False
        for acft in self.acft_list:
            acft.label.stop_drag()

    def handle_event_mouse_middle_click_drag(self, event):
        if isinstance(event.rel, tuple) and len(event.rel) == 2:
            self.cam_offset_x -= event.rel[0]
            self.cam_offset_y -= event.rel[1]

    def handle_event_key_down(self, event):

        key_pressed = event.key

        # ==================================================
        # AIRCRAFT COMMAND MODE
        # ==================================================

        if self.radar_selected is not None:

            # ENTER = execute command
            if key_pressed == pygame.K_RETURN or key_pressed == pygame.K_KP_ENTER:

                self.execute_command()

                self.command_box.input_text = ""
                return

            # BACKSPACE
            elif key_pressed == pygame.K_BACKSPACE:

                self.command_box.input_text = (
                    self.command_box.input_text[:-1]
                )
                return

            elif key_pressed == pygame.K_ESCAPE:
                self.command_box.input_text = ""

            elif self.command_box.input_text == "" or self.command_box.input_text.endswith(" "):

                if event.key == pygame.K_UP or event.key == pygame.K_KP_8:
                    self.command_box.input_text += "↑"
                elif event.key == pygame.K_DOWN or event.key == pygame.K_KP_2:
                    self.command_box.input_text += "↓"
                elif event.key == pygame.K_LEFT or event.key == pygame.K_KP_4:
                    self.command_box.input_text += "←"
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP_6:
                    self.command_box.input_text += "→"
                elif event.key == pygame.K_KP_MULTIPLY:
                    self.command_box.input_text += "*"
                elif event.key == pygame.K_KP_DIVIDE:
                    self.command_box.input_text += "/"
                elif event.key == pygame.K_m:
                    self.command_box.input_text += "m"
                elif event.key == pygame.K_s:
                    self.command_box.input_text += "s"

            # =========================
            # NORMAL TEXT INPUT
            # =========================

            else:

                if event.unicode.isprintable():
                    self.command_box.input_text += event.unicode

                return

        # ==================================================
        # NORMAL GAME MODE
        # ==================================================

        if key_pressed == pygame.K_q:

            self.main_running = False

        elif key_pressed == pygame.K_c:

            self.reset_camera()


        elif key_pressed == pygame.K_a:

            # Do not allow multiple active QDMs
            for qdm in self.qdm_list:
                if qdm.active:
                    return

            mouse_x, mouse_y = pygame.mouse.get_pos()
            anchor = self.get_anchor_from_mouse(mouse_x, mouse_y)
            new_qdm = Qdm(anchor)

            self.qdm_list.append(new_qdm)

    def reset_camera(self):
        self.zoom = self.default_zoom
        self.cam_offset_x = self.cam_center_x * self.zoom - self.variables.display_width_half
        self.cam_offset_y = -self.cam_center_y * self.zoom - self.variables.display_height_half

    def move_acft(self, elapsed_sec: float):
        if self.radar_selected is not None:
            identity = self.radar_selected.identity
        else:
            identity = None
        for acft in self.acft_list:
            acft.tick(identity, elapsed_sec)

    def handle_mouse_motion(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.command_box.handle_mouse_motion(
            (mouse_x, mouse_y)
        )

        for acft in self.acft_list:
            screen_x = world_to_screen_x(
                acft.pos_x,
                self.cam_offset_x,
                self.zoom
            )

            screen_y = world_to_screen_y(
                acft.pos_y,
                self.cam_offset_y,
                self.zoom
            )

            acft.label.drag(
                mouse_x,
                mouse_y,
                screen_x,
                screen_y
            )

        if self.middle_click_on or self.right_click_on:
            self.handle_event_mouse_middle_click_drag(event)

    def execute_command(self):
        if isinstance(self.radar_selected, Acft):
            results = get_command(self.command_box.input_text)
            for result in results:
                if result[0]:
                    self.radar_selected.execute_command(result[1], result[2], result[3])

    def detect_conflicts(self):

        self.acft_conflict_list = []
        for acft in self.acft_list:
            acft.is_conflicting = False

        for i in range(len(self.acft_list)):

            acft_1 = self.acft_list[i]

            for j in range(i + 1, len(self.acft_list)):

                acft_2 = self.acft_list[j]

                dist = math.hypot(
                    acft_1.real_x - acft_2.real_x,
                    acft_1.real_y - acft_2.real_y
                )

                wtc_dist_1 = get_wake_sep(
                    acft_1.wtc,
                    acft_2.wtc
                )

                wtc_dist_2 = get_wake_sep(
                    acft_2.wtc,
                    acft_1.wtc
                )

                rw = max(wtc_dist_1, wtc_dist_2)

                vert_dist = abs(
                    acft_1.altitude_act
                    - acft_2.altitude_act
                )

                if dist < rw and vert_dist < 1000:
                    self.acft_conflict_list.append((
                        (acft_1.pos_x, acft_1.pos_y),
                        (acft_2.pos_x, acft_2.pos_y),
                    ))
                    acft_1.is_conflicting = True
                    acft_2.is_conflicting = True

    def get_anchor_from_mouse(
            self,
            mouse_x,
            mouse_y,
            buffer_px=20
    ):
        # =========================
        # AIRCRAFT
        # =========================

        for acft in self.acft_list:

            screen_x = world_to_screen_x(
                acft.pos_x,
                self.cam_offset_x,
                self.zoom
            )

            screen_y = world_to_screen_y(
                acft.pos_y,
                self.cam_offset_y,
                self.zoom
            )

            dist = math.hypot(mouse_x - screen_x, mouse_y - screen_y)

            if dist <= buffer_px:
                return QdmAnchor(
                    acft.pos_x,
                    acft.pos_y,
                    acft
                )

            # =====================================
            # AIRCRAFT LABEL HITBOX
            # =====================================

            if acft.label.is_mouse_over(mouse_x, mouse_y):
                return QdmAnchor(
                    acft.pos_x,
                    acft.pos_y,
                    acft
                )

        # =========================
        # POINTS
        # =========================

        for point in self.airspace.points:

            screen_x = world_to_screen_x(
                point.pos_x,
                self.cam_offset_x,
                self.zoom
            )

            screen_y = world_to_screen_y(
                point.pos_y,
                self.cam_offset_y,
                self.zoom
            )

            dist = math.hypot(
                mouse_x - screen_x,
                mouse_y - screen_y
            )

            if dist <= buffer_px:
                return QdmAnchor(
                    point.pos_x,
                    point.pos_y,
                    point
                )

        # =========================
        # WORLD POSITION
        # =========================

        world_x = (mouse_x + self.cam_offset_x) / self.zoom

        world_y = -(mouse_y + self.cam_offset_y) / self.zoom

        return QdmAnchor(
            world_x,
            world_y
        )

    def draw_qdm(self):
        for qdm in self.qdm_list:
            self.drawer.draw_qdm(qdm, self.cam_offset_x, self.cam_offset_y, self.zoom)

    def get_qdm_at_mouse(
            self,
            mouse_x,
            mouse_y,
            buffer_px=10
    ):

        for qdm in reversed(self.qdm_list):

            start_pos, end_pos = qdm.get_positions()

            start_x = world_to_screen_x(
                start_pos[0],
                self.cam_offset_x,
                self.zoom
            )

            start_y = world_to_screen_y(
                start_pos[1],
                self.cam_offset_y,
                self.zoom
            )

            if qdm.active:

                end_x, end_y = pygame.mouse.get_pos()

            else:

                end_x = world_to_screen_x(
                    end_pos[0],
                    self.cam_offset_x,
                    self.zoom
                )

                end_y = world_to_screen_y(
                    end_pos[1],
                    self.cam_offset_y,
                    self.zoom
                )

            # ======================================
            # Distance from point to line segment
            # ======================================

            dx = end_x - start_x
            dy = end_y - start_y

            length_sq = dx * dx + dy * dy

            if length_sq == 0:
                continue

            t = (((mouse_x - start_x) * dx + (mouse_y - start_y) * dy) / length_sq)

            t = max(0, min(1, t))

            proj_x = start_x + t * dx
            proj_y = start_y + t * dy

            dist = math.hypot(
                mouse_x - proj_x,
                mouse_y - proj_y
            )

            if dist <= buffer_px:
                return qdm

        return None

    def get_qdm_endpoint_at_mouse(
            self,
            mouse_x,
            mouse_y,
            buffer_px=12
    ):

        for qdm in reversed(self.qdm_list):

            start_pos, end_pos = qdm.get_positions()

            # =========================
            # START
            # =========================
            sx = world_to_screen_x(
                start_pos[0],
                self.cam_offset_x,
                self.zoom
            )
            sy = world_to_screen_y(
                start_pos[1],
                self.cam_offset_y,
                self.zoom
            )

            if math.hypot(mouse_x - sx, mouse_y - sy) <= buffer_px:
                return qdm, "start"

            # =========================
            # END
            # =========================

            if end_pos is not None:
                ex = world_to_screen_x(
                    end_pos[0],
                    self.cam_offset_x,
                    self.zoom
                )
                ey = world_to_screen_y(
                    end_pos[1],
                    self.cam_offset_y,
                    self.zoom
                )
                if math.hypot(mouse_x - ex, mouse_y - ey) <= buffer_px:
                    return qdm, "end"

        return None, None
