import math
import random

import pygame

from pages.radar.Airspace import Airspace
from pages.radar.Label import Label
from pages.radar.PerformanceData import PerformanceData
from pages.radar.data.helper import (
    convert_lat_and_long_to_radar,
    get_rad_angle,
    get_cos_angle,
    get_sin_angle,
    latlon_to_world,
    validate_ssr, ias_to_tas, speed_of_sound_knots, mach_to_tas
)


class Acft:
    act_speed_tas: int | float = 0
    act_speed_gs: int | float = 0

    d_acft_width: int = 11
    d_acft_height: int = 11
    d_acft_color_ident: tuple[int, int, int] = (255, 255, 255)
    d_acft_color_conflict: tuple[int, int, int] = (255, 255, 255)

    d_prl_color: tuple[int, int, int] = (255, 255, 255)
    d_prl_width: int = 1
    d_prl_length_in_sec: int | float = 60
    d_prl_has_custom: bool = False

    old_radar_blip_amount = 6

    prl_end_x: int | float = 0
    prl_end_y: int | float = 0

    pos_x: int | float = 0
    pos_y: int | float = 0

    real_x: int | float = 0
    real_y: int | float = 0

    lat: int | float = 0
    lon: int | float = 0

    default_rate_of_turn: int = 3
    expedite_rate_of_turn: int = 5

    acft_trail_radius: int = 2

    rate_of_climb: int = 0
    default_rate_of_climb: int = 1500

    wtc: str

    is_speed_locked: bool = False
    is_conflicting: bool = False

    msaw_warning: bool = False

    # Frozen heading snapshot for PRL
    prl_heading_snapshot: float = 0

    # Radar-frozen display values
    d_heading_act: float = 0
    d_heading_req: float = 0

    d_altitude_act: float = 0
    d_altitude_req: float = 0

    d_act_speed_ias: float = 0
    d_req_speed_ias: float = 0
    d_act_speed_gs: float = 0

    d_rate_of_climb: float = 0

    NAV_HEADING: int = 0
    NAV_ROUTE: int = 1
    NAV_ILS: int = 2

    SPEED_MODE_IAS = 0
    SPEED_MODE_MACH = 1

    ILS_INTERCEPT = 0
    ILS_TRACK = 1

    show_route: bool = False

    roc_acceleration = 200
    roc_deceleration = 300

    def __init__(
            self,
            airspace_center_lon: int | float,
            airspace_center_lat: int | float,
            perf_data: PerformanceData,
            identity: int,

            cs: str = '',
            icao_type: str = '',
            coord_x: str = '',
            coord_y: str = '',

            heading_act: int = 0,
            heading_req: int = 0,
            turn_direction: int = 1,

            altitude_act: int = 0,
            altitude_req: int = 0,

            req_speed_ias: int = 0,
            act_speed_ias: int = 0,
            speed_increment: int = 2,

            ssr: str = '7000',
            route: str = '',
            destination_icao: str = '',
            expected_rwy: str = '',

            color: tuple[int, int, int] = (255, 255, 255),
            color_selected_radius: tuple[int, int, int] = (255, 50, 50),
            color_wake_radius: tuple[int, int, int] = (255, 150, 150),

            selected_radius: int | float = 50,
            is_clicked: bool = False,
    ) -> None:

        self.transition_speed_mach = 24000
        self.color_conflict = (255, 0, 0)
        self.is_roc_locked = False
        self.climb_dir = 1
        self.rate_of_turn = self.default_rate_of_turn

        self.speed_mode = self.SPEED_MODE_IAS
        self.req_mach = 0.0
        self.act_mach = 0.0

        self.perf_data = perf_data

        self.identity = identity
        self.cs = cs
        self.icao_type = icao_type

        self.coord_x = coord_x
        self.coord_y = coord_y

        self.heading_act = heading_act
        self.heading_req = heading_req
        self.turn_direction = turn_direction

        self.altitude_act = altitude_act
        self.altitude_req = altitude_req

        self.req_speed_ias = req_speed_ias
        self.act_speed_ias = act_speed_ias
        self.speed_increment = speed_increment

        self.ssr = ssr
        self.route = route
        self.destination_icao = destination_icao
        self.expected_rwy = expected_rwy
        self.route_points = []

        self.color = color
        self.color_selected_radius = color_selected_radius
        self.color_wake_radius = color_wake_radius

        self.selected_radius = selected_radius
        self.is_clicked = is_clicked

        self.airspace_center_lon = airspace_center_lon
        self.airspace_center_lat = airspace_center_lat

        self.old_pos = []

        self.label = Label()

        self.update_data()
        self.after_load()
        self.nav_mode = self.NAV_HEADING
        self.ils_mode = self.ILS_INTERCEPT

        self.todo_list = []

        self.weight_factor = random.uniform(0.7, 1.0)
        self.target_rate_of_climb = 0
        self.locked_roc = 0

    def after_load(self):

        lon, lat = convert_lat_and_long_to_radar(
            f"{self.coord_x}|{self.coord_y}"
        )

        self.lon = lon
        self.lat = lat

        self.pos_x, self.pos_y = latlon_to_world(
            lat,
            lon,
            self.airspace_center_lat,
            self.airspace_center_lon
        )

        self.real_x = self.pos_x
        self.real_y = self.pos_y

        self.update_speed()

        # Initial PRL heading snapshot
        self.prl_heading_snapshot = self.heading_act

        self.prl_end_x, self.prl_end_y = self.get_prl_pos(
            self.d_prl_length_in_sec
        )

        for i in range(self.old_radar_blip_amount):
            self.old_pos.append((self.pos_x, self.pos_y))
        self.update_radar_data()

        try:

            self_data = self.perf_data.get_perf_by_icao(self.icao_type)
            self.roc_acceleration = self_data['roc_acceleration']
            self.roc_deceleration = self_data['roc_deceleration']
        except KeyError:
            self.roc_acceleration = 200
            self.roc_deceleration = 300

    def tick(self, identity: int | None, elapsed_sec: float, airspace: Airspace):

        if self.identity != identity:
            self.is_clicked = False

        if self.nav_mode == self.NAV_ROUTE:
            self.update_route_navigation()
        elif self.nav_mode == self.NAV_ILS:
            self.update_ils_navigation(airspace)

        self.check_heading()

        self.move_logic(elapsed_sec)

        self.check_heading()

    def check_heading(self):

        self.heading_act %= 360
        self.heading_req %= 360

        if self.heading_act == 0:
            self.heading_act = 360

        if self.heading_req == 0:
            self.heading_req = 360

    def move_logic(self, elapsed_sec: float):

        self.move_logic_heading(elapsed_sec)
        self.move_logic_speed(elapsed_sec)
        self.move_logic_roc(elapsed_sec)
        self.move_logic_alt(elapsed_sec)
        self.move_acft(elapsed_sec)

        # Recalculate PRL every frame
        # using frozen heading + live speed
        self.prl_end_x, self.prl_end_y = self.get_prl_pos(
            self.d_prl_length_in_sec
        )

    def update_pos_list(self):

        self.old_pos.append((self.real_x, self.real_y))

        new_list = self.old_pos[-self.old_radar_blip_amount:]

        self.old_pos = new_list

    def move_logic_heading(self, elapsed_sec: float):

        step = self.rate_of_turn * elapsed_sec
        diff = ((self.heading_req - self.heading_act + 180) % 360) - 180

        if abs(diff) <= step:
            self.heading_act = self.heading_req

            if self.rate_of_turn != self.default_rate_of_turn:
                self.rate_of_turn = self.default_rate_of_turn

            return

        # Turn towards target
        if diff > 0:
            self.heading_act += step
        else:
            self.heading_act -= step

        # Normalize heading to 0-360
        self.heading_act %= 360

        # Optional:
        # keep north displayed as 360 instead of 0
        if self.heading_act == 0:
            self.heading_act = 360

    def move_logic_speed(self, elapsed_sec: float):

        if self.altitude_act >= self.transition_speed_mach:
            if self.speed_mode == self.SPEED_MODE_IAS:
                self.req_mach = (
                        self.act_speed_tas
                        / speed_of_sound_knots(self.altitude_act)
                )
                self.act_mach = self.req_mach
                self.speed_mode = self.SPEED_MODE_MACH

        else:
            if self.speed_mode == self.SPEED_MODE_MACH:
                self.req_speed_ias = self.act_speed_ias
                self.speed_mode = self.SPEED_MODE_IAS

        if self.speed_mode == self.SPEED_MODE_IAS:

            diff = self.req_speed_ias - self.act_speed_ias

            if diff != 0:

                step = self.speed_increment * elapsed_sec

                if abs(diff) < step:
                    step = abs(diff)

                if diff > 0:
                    self.act_speed_ias += step
                else:
                    self.act_speed_ias -= step

        else:

            diff = self.req_mach - self.act_mach

            if abs(diff) > 0.001:

                step = 0.001 * elapsed_sec

                if abs(diff) < step:
                    step = abs(diff)

                if diff > 0:
                    self.act_mach += step
                else:
                    self.act_mach -= step

        self.update_speed()

    def move_logic_roc(self, elapsed_sec):
        diff = self.target_rate_of_climb - self.rate_of_climb
        if abs(diff) < 1:
            self.rate_of_climb = self.target_rate_of_climb
            return
        if abs(self.target_rate_of_climb) > abs(self.rate_of_climb):
            accel = self.roc_acceleration
        else:
            accel = self.roc_deceleration
        step = accel * elapsed_sec
        if abs(diff) < step:
            self.rate_of_climb = self.target_rate_of_climb
        else:
            self.rate_of_climb += step if diff > 0 else -step

    def move_logic_alt(self, elapsed_time):

        previous_alt = self.altitude_act

        # Level off
        if abs(self.altitude_req - self.altitude_act) < 10:
            self.altitude_act = self.altitude_req
            self.target_rate_of_climb = 0

            self.check_todo_list(previous_alt)
            return

        # Determine direction
        if self.altitude_req > self.altitude_act:
            self.climb_dir = 1
        else:
            self.climb_dir = -1

        # Calculate target ROC
        if self.is_roc_locked:
            target_roc = self.locked_roc
        else:
            target_roc = self.perf_data.get_rate_of_climb(
                self.icao_type,
                self.altitude_act,
                self.climb_dir
            )

            target_roc *= self.weight_factor

        self.target_rate_of_climb = (target_roc * self.climb_dir)

        # Move altitude using ACTUAL ROC
        self.altitude_act += (self.rate_of_climb / 60) * elapsed_time

        # Prevent overshoot
        if self.climb_dir == 1 and self.altitude_act >= self.altitude_req:

            self.altitude_act = self.altitude_req
            self.target_rate_of_climb = 0

        elif self.climb_dir == -1 and self.altitude_act <= self.altitude_req:

            self.altitude_act = self.altitude_req
            self.target_rate_of_climb = 0

        self.target_rate_of_climb = int(self.target_rate_of_climb)
        self.rate_of_climb = int(self.rate_of_climb)

        self.check_todo_list(previous_alt)

    def move_acft(self, elapsed_sec: float = 1):

        next_x, next_y = self.next_pos(
            get_rad_angle(self.heading_act),
            elapsed_sec
        )

        self.real_x = next_x
        self.real_y = next_y

    def get_gs_speed_per_sec(self) -> float:
        return self.act_speed_gs / 3600

    def next_pos(self, r_angle, amount_of_sec):

        next_x = (
                self.real_x
                + get_cos_angle(r_angle)
                * self.get_gs_speed_per_sec()
                * amount_of_sec
        )

        next_y = (
                self.real_y
                + get_sin_angle(r_angle)
                * self.get_gs_speed_per_sec()
                * amount_of_sec
        )

        return next_x, next_y

    def get_next_pos(self, amount_of_sec: int = 1):

        r_angle = get_rad_angle(self.heading_act)

        return self.next_pos(r_angle, amount_of_sec)

    def radar_refresh(self):

        self.update_pos_list()

        # Freeze radar position
        self.pos_x = self.real_x
        self.pos_y = self.real_y

        # Freeze PRL heading
        self.prl_heading_snapshot = self.heading_act

        self.update_radar_data()

    def get_prl_pos(self, amount_of_sec: int | float = 1):

        # Frozen heading
        r_angle = get_rad_angle(self.prl_heading_snapshot)

        # Frozen radar position
        next_x = self.pos_x + (
                get_cos_angle(r_angle)
                * self.get_gs_speed_per_sec()
                * amount_of_sec
        )

        next_y = self.pos_y + (
                get_sin_angle(r_angle)
                * self.get_gs_speed_per_sec()
                * amount_of_sec
        )

        return next_x, next_y

    def draw_label(self, surface: pygame.Surface, screen_x, screen_y):

        self.label.draw(
            surface,
            screen_x,
            screen_y,
            {
                "cs": self.cs,
                "icao_type": self.icao_type,
                "is_conflicting": self.is_conflicting,
                "msaw_warning": self.msaw_warning,
                "ssr": self.ssr,
                "wtc": self.wtc,
                "heading_act": self.heading_act,
                "heading_req": self.heading_req,
                "req_speed_ias": self.d_req_speed_ias,
                "act_speed_ias": self.d_act_speed_ias,
                "act_mach": self.act_mach,
                "req_mach": self.req_mach,
                "speed_mode": self.speed_mode,
                "act_speed_gs": self.d_act_speed_gs,
                "altitude_req": self.d_altitude_req,
                "altitude_act": self.d_altitude_act,
                "rate_of_climb": self.d_rate_of_climb,
                "route_points": self.route_points,
                "debug": self.rate_of_turn,
            }
        )

    def execute_command(self, data: dict):

        command = data.get("cmd")
        value = data.get("value")
        special = data.get("special", 0)
        return_str = ''

        # ==========================================
        # CLIMB / DESCEND
        # ==========================================
        if command in ["CLIMB", "DESCEND"]:
            if command == 'CLIMB':
                direction = 'climb'
            else:
                direction = 'descend'
            if special != 0:
                self.locked_roc = abs(special)
                self.is_roc_locked = True
                return_str = "{} {} to {} at {}".format(self.cs, direction, value, self.rate_of_climb)

            else:
                self.is_roc_locked = False
                return_str = "{} {} to {}".format(self.cs, direction, value)
            self.altitude_req = value * 100

        # ==========================================
        # TURN LEFT
        # ==========================================
        elif command == "TURN_LEFT":
            self.set_rate_of_turn(special)
            self.heading_req = value
            self.turn_direction = -1
            self.nav_mode = self.NAV_HEADING
            return_str = "{} turn left heading {}".format(self.cs, self.heading_req)


        # ==========================================
        # TURN RIGHT
        # ==========================================

        elif command == "TURN_RIGHT":
            self.set_rate_of_turn(special)
            self.heading_req = value
            self.turn_direction = 1
            self.nav_mode = self.NAV_HEADING
            return_str = "{} turn right heading {}".format(self.cs, self.heading_req)


        # ==========================================
        # HEADING
        # ==========================================

        elif command == "HEADING":
            self.set_rate_of_turn(special)
            self.heading_req = value
            diff = (value - self.heading_act) % 360
            if diff <= 180:
                self.turn_direction = 1
            else:
                self.turn_direction = -1
            self.nav_mode = self.NAV_HEADING
            return_str = "{} fly heading {}".format(self.cs, self.heading_req)


        # ==========================================
        # SPEED
        # ==========================================

        elif command == "SPEED":
            self.is_speed_locked = True
            new_speed = self.get_realistic_speed(value)
            self.req_speed_ias = new_speed
            return_str = "{} speed {} knots".format(self.cs, new_speed)


        # ==========================================
        # UNLOCK SPEED
        # ==========================================

        elif command == "UNLOCK_SPEED":
            self.is_speed_locked = False
            return_str = "{} resume own speed".format(self.cs)


        # ==========================================
        # MAKE SPEED
        # ==========================================

        elif command == "MAKE_SPEED":
            self.is_speed_locked = True
            new_speed = self.get_realistic_speed(value)
            self.act_speed_ias = new_speed
            self.req_speed_ias = new_speed
            return_str = "{} make speed {}".format(self.cs, self.req_speed_ias)


        # ==========================================
        # MAKE HEADING
        # ==========================================

        elif command == "MAKE_HEADING":
            self.heading_req = value
            self.heading_act = value
            self.nav_mode = self.NAV_HEADING
            return_str = "{} make speed {}".format(self.cs, self.req_speed_ias)


        # ==========================================
        # MAKE LEVEL
        # ==========================================

        elif command == "MAKE_LEVEL":
            self.altitude_req = value * 100
            self.altitude_act = value * 100
            return_str = "{} make level {}".format(self.cs, value)


        # ==========================================
        # SSR
        # ==========================================

        elif command == "SSR":
            ssr = validate_ssr(value)
            if ssr:
                self.ssr = ssr
                return_str = "{} SQUAWK {}".format(self.cs, self.ssr)


        # ==========================================
        # DIRECT
        # ==========================================

        elif command == "DIRECT":
            self.route_points = [value]
            self.nav_mode = self.NAV_ROUTE
            return_str = "{} proceed direct {}".format(self.cs, value.abbreviation)

        # ==========================================
        # ROUTE
        # ==========================================

        elif command == "ROUTE":
            if value == 0:
                self.nav_mode = self.NAV_ROUTE
                return_str = "{} resume own navigation direct {}".format(self.cs, self.route_points[0])

            else:
                self.route_points = value
                self.nav_mode = self.NAV_ROUTE
                if isinstance(self.route_points, list):
                    route = ''
                    for point in self.route_points:
                        route += point.abbreviation + ' '
                    return_str = "{} proceed {}".format(self.cs, route)


        # ==========================================
        # AT COMMAND
        # ==========================================

        elif command == "AT_COMMAND":
            try:
                target_type = value["limiter"][:1]
                target = str(value["limiter"]).replace(target_type, "")
                content = value["command"]
                self.todo_list.append({
                    "target_type": target_type,
                    "target": target,
                    "command": content[0]
                })
            except ValueError:
                return_str = "Unknown command : {} {}".format(command, value)

        elif command == "MACH":
            self.speed_mode = self.SPEED_MODE_MACH
            self.req_mach = value
            return_str = "{} speed Mach {}".format(self.cs, value)

        elif command == "ILS":
            self.nav_mode = self.NAV_ILS
            self.ils_mode = self.ILS_INTERCEPT
            return_str = "{} is cleared for ILS {}".format(self.cs, self.expected_rwy)

        return return_str

    def update_speed(self):

        if self.speed_mode == self.SPEED_MODE_IAS:

            self.act_speed_tas = ias_to_tas(self.act_speed_ias, self.altitude_act)

            self.act_mach = (self.act_speed_tas / speed_of_sound_knots(self.altitude_act))

        else:

            self.act_speed_tas = mach_to_tas(self.act_mach, self.altitude_act)

            # Optional reverse conversion
            self.act_speed_ias = ( self.act_speed_tas / (1 + 0.02 * self.altitude_act / 1000))

        self.act_speed_gs = self.act_speed_tas

    def update_data(self):

        self.wtc = self.perf_data.get_wtc(
            self.icao_type
        )

    def get_realistic_speed(self, value):

        # TODO:
        # Compare against aircraft max speed / mach

        return value

    def get_color(self):
        if self.is_conflicting:
            return self.color_conflict
        else:
            return self.color

    def set_rate_of_turn(self, special: int):
        if special == 1:
            self.rate_of_turn = self.expedite_rate_of_turn
        else:
            self.rate_of_turn = self.default_rate_of_turn

    def update_radar_data(self):
        self.d_heading_act = self.heading_act
        self.d_heading_req = self.heading_req
        self.d_altitude_act = self.altitude_act
        self.d_altitude_req = self.altitude_req
        self.d_act_speed_ias = self.act_speed_ias
        self.d_req_speed_ias = self.req_speed_ias
        self.d_act_speed_gs = self.act_speed_gs
        self.d_rate_of_climb = self.rate_of_climb

    def update_route_navigation(self):

        if len(self.route_points) == 0:
            return

        target = self.route_points[0]

        dx = target.pos_x - self.real_x
        dy = target.pos_y - self.real_y

        distance = math.hypot(dx, dy)

        # =========================
        # WAYPOINT PASSED
        # =========================

        capture_radius = max(
            2,
            self.get_gs_speed_per_sec() * 3
        )
        if distance < capture_radius:

            self.check_todo_list_point(self.route_points[0].abbreviation)
            self.route_points.pop(0)

            # Route finished
            if len(self.route_points) == 0:
                self.nav_mode = self.NAV_HEADING
                return

            target = self.route_points[0]

            dx = target.pos_x - self.real_x
            dy = target.pos_y - self.real_y

        # =========================
        # COMPUTE REQUIRED HEADING
        # =========================

        heading = math.degrees(
            math.atan2(dy, dx)
        )

        heading = (90 - heading) % 360

        self.heading_req = heading

        # Turn direction
        diff = (self.heading_req - self.heading_act) % 360

        if diff <= 180:
            self.turn_direction = 1
        else:
            self.turn_direction = -1

    def update_ils_navigation(self, airspace: Airspace):

        ad = airspace.get_aerodrome_by_icao(
            self.destination_icao
        )

        if not ad:
            return

        rwy = ad.get_active_rwy()

        if not rwy:
            return

        loc = rwy.get_active_localizer()

        if not loc:
            return

        error = loc.get_cross_track_error(
            self.real_x,
            self.real_y
        )

        # =================================
        # INTERCEPT PHASE
        # =================================

        if self.ils_mode == self.ILS_INTERCEPT:

            if abs(error) < 0.3:
                self.ils_mode = self.ILS_TRACK

            return

        # =================================
        # TRACK PHASE
        # =================================

        gain = 5

        desired_heading = (
                loc.runway_heading
                - error * gain
        )

        self.heading_req = desired_heading % 360

        diff = (
                       self.heading_req
                       - self.heading_act
               ) % 360

        self.turn_direction = (
            1 if diff <= 180 else -1
        )

    def check_todo_list(self, previous_alt):
        remove_items = []
        for item in self.todo_list:
            try:
                target_type = item["target_type"]
                target = int(item["target"]) * 100
                command = item["command"]

                if target_type != "l":
                    continue

                crossed = (
                        previous_alt < target <= self.altitude_act
                        or
                        previous_alt > target >= self.altitude_act
                )

                if crossed:
                    self.execute_command(command)
                    remove_items.append(item)

            except (ValueError, TypeError, KeyError):
                remove_items.append(item)

        for item in remove_items:
            self.todo_list.remove(item)

    def check_todo_list_point(self, abbr: str):
        remove_items = []
        for item in list(self.todo_list):
            if item["target_type"] == "f":
                target = str(item["target"]).upper()
                if target == abbr.upper():
                    self.execute_command(item["command"])
                    remove_items.append(item)

        for item in remove_items:
            self.todo_list.remove(item)