from pages.radar.data.helper import convert_lat_and_long_to_radar, get_rad_angle, get_cos_angle, get_sin_angle, \
    latlon_to_world


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

    old_radar_blip_amount = 5

    pos_x: int | float = 0
    pos_y: int | float = 0
    real_x: int | float = 0
    real_y: int | float = 0
    lat: int | float = 0
    lon: int | float = 0

    default_rate_of_turn: int = 3
    rate_of_turn: int = 3
    acft_trail_radius: int = 2

    def __init__(
            self,
            airspace_center_lon: int | float,
            airspace_center_lat: int | float,
            identity: int,
            cs: str = '',
            coord_x: str = '',
            coord_y: str = '',

            heading_act: int = 0,
            heading_req: int = 0,
            turn_direction: int = 1,

            altitude_act: int = 0,
            altitude_req: int = 0,

            req_speed_ias: int = 0,
            act_speed_ias: int = 0,
            speed_increment: int = 1,

            ssr: str = '7000',
            route: str = '',

            color: tuple[int, int, int] = (255, 255, 255),
            color_selected_radius: tuple[int, int, int] = (255, 50, 50),
            color_wake_radius: tuple[int, int, int] = (255, 150, 150),

            wtc: str = 'M',
            selected_radius: int | float = 50,
            is_clicked: bool = False,
    ) -> None:
        self.identity = identity
        self.cs = cs
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
        self.color = color
        self.color_selected_radius = color_selected_radius
        self.color_wake_radius = color_wake_radius
        self.wtc = wtc
        self.selected_radius = selected_radius
        self.is_clicked = is_clicked
        self.airspace_center_lon = airspace_center_lon
        self.airspace_center_lat = airspace_center_lat
        self.old_pos = []
        self.after_load()

    def after_load(self):
        lon, lat = convert_lat_and_long_to_radar(f"{self.coord_x}|{self.coord_y}")
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
        for i in range(self.old_radar_blip_amount):
            self.old_pos.append((self.pos_x, self.pos_y))

    def tick(self, identity: int | None, elapsed_sec: float):
        if self.identity != identity:
            self.is_clicked = False
        self.check_heading()
        self.move_logic(elapsed_sec)
        self.check_heading()

    def check_heading(self):
        if self.heading_act <= 0:
            self.heading_act += 360
            self.check_heading()
        elif self.heading_act > 360:
            self.heading_act -= 360
            self.check_heading()
        elif self.heading_req <= 0:
            self.heading_req += 360
            self.check_heading()
        elif self.heading_req > 360:
            self.heading_req -= 360
            self.check_heading()

    def move_logic(self, elapsed_sec: float):
        self.move_logic_heading(elapsed_sec)
        self.move_logic_speed()
        self.move_logic_alt()
        self.move_acft(elapsed_sec)

    def update_pos_list(self):
        self.old_pos.append((self.real_x, self.real_y))
        new_list = self.old_pos[-self.old_radar_blip_amount:]
        self.old_pos = new_list

    def move_logic_heading(self, elapsed_sec: float):
        if self.turn_direction == 1 or self.turn_direction == -1:
            if self.heading_act != self.heading_req:
                next_move_p = self.heading_act + 3
                next_move_m = self.heading_act - 3
                if next_move_m <= self.heading_req < next_move_p:
                    self.heading_act = self.heading_req
                else:
                    self.heading_act += self.turn_direction * self.rate_of_turn * elapsed_sec

    def move_logic_speed(self):
        diff = self.req_speed_ias - self.act_speed_ias
        if diff != 0:
            step = self.speed_increment if abs(diff) > self.speed_increment else abs(diff)
            self.act_speed_ias += step if diff > 0 else -step

        self.act_speed_tas = self.act_speed_ias + (self.act_speed_ias * 0.02 * self.altitude_req / 1000)
        # TODO calculate gs when wind is implemented
        self.act_speed_gs = self.act_speed_tas

    def move_logic_alt(self):
        pass

    def move_acft(self, elapsed_sec: float = 1):
        next_x, next_y = self.next_pos(get_rad_angle(self.heading_act), elapsed_sec)
        self.real_x = next_x
        self.real_y = next_y

    def get_gs_speed_per_sec(self) -> float:
        return self.act_speed_gs / 3600

    def next_pos(self, r_angle, amount_of_sec):
        next_x = self.real_x + get_cos_angle(r_angle) * self.get_gs_speed_per_sec() * amount_of_sec
        next_y = self.real_y + get_sin_angle(r_angle) * self.get_gs_speed_per_sec() * amount_of_sec
        return next_x, next_y

    def get_next_pos(self, amount_of_sec: int = 1):
        r_angle = get_rad_angle(self.heading_act)
        return self.next_pos(r_angle, amount_of_sec)

    def radar_refresh(self):
        self.update_pos_list()

        self.pos_x = self.real_x
        self.pos_y = self.real_y

    def get_prl_pos(self, amount_of_sec: int | float = 1):
        r_angle = get_rad_angle(self.heading_act)
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
