from pages.radar.data.helper import get_rad_angle, get_cos_angle, get_sin_angle
from pages.radar.data.immovable_variable import scale_NM_to_su


class Acft:

    d_acft_width: int = 11
    d_acft_height: int = 11
    d_acft_color_ident: tuple[int, int, int] = (255, 255, 255)
    d_acft_color_conflict: tuple[int, int, int] = (255, 255, 255)
    d_prl_color: tuple[int, int, int] = (255, 255, 255)
    d_prl_width: int = 1
    d_prl_length: int = 60

    turn_by_sec: int = 3

    def __init__(
            self,
            identity: int,
            cs: str = '',
            pos_x: int = 0,
            pos_y: int = 0,

            heading_act: int = 0,
            heading_req: int = 0,
            heading_turn: str = '',

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
            selected_radius: float = 1.5,
            is_clicked: bool = False,
            draw_wtc_circle: bool = False
    ) -> None:
        self.identity = identity
        self.cs = cs
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.heading_act = heading_act
        self.heading_req = heading_req
        self.heading_turn = heading_turn
        self.altitude_act = altitude_act
        self.altitude_req = altitude_req
        self.req_speed_kts = req_speed_ias
        self.act_speed_kts = act_speed_ias
        self.speed_increment = speed_increment
        self.ssr = ssr
        self.route = route
        self.color = color
        self.color_selected_radius = color_selected_radius
        self.color_wake_radius = color_wake_radius
        self.wtc = wtc
        self.selected_radius = selected_radius * scale_NM_to_su
        self.is_clicked = is_clicked
        self.draw_wtc_circle = draw_wtc_circle

    def get_next_pos(self, amount_of_sec: int = 1):
        r_angle = get_rad_angle(self.heading_act)
        return self.next_pos(r_angle, amount_of_sec)

    def get_speed_per_sec(self) -> float:
        return self.act_speed_kts / 3600

    def next_pos(self, r_angle, amount_of_sec):
        next_x = self.pos_x + get_cos_angle(r_angle) * self.get_speed_per_sec() * amount_of_sec * scale_NM_to_su
        next_y = self.pos_y + get_sin_angle(r_angle) * self.get_speed_per_sec() * amount_of_sec * scale_NM_to_su
        return next_x, next_y

    def move_logic(self):
        self.move_logic_heading()
        self.move_logic_speed()

    def move_logic_heading(self):
        if self.heading_act != self.heading_turn:
            diff_of_degree = self.heading_req - self.heading_act
            if -3 <= diff_of_degree <= 3:
                self.heading_act = self.heading_req
            else:
                if self.heading_turn == 'r':
                    self.heading_act += self.turn_by_sec
                if self.heading_turn == 'l':
                    self.heading_act -= self.turn_by_sec

    def move_logic_speed(self):
        if self.req_speed_kts != self.act_speed_kts:
            if self.req_speed_kts > self.act_speed_kts:
                self.act_speed_kts += self.speed_increment
            else:
                self.act_speed_kts -= self.speed_increment

    def check_is_selected(self, ident: int):
        if self.identity == ident:
            self.is_clicked = True
        else:
            self.is_clicked = False

    def move_acft(self):
        self.check_heading()
        self.move_logic()
        pos = self.next_pos(get_rad_angle(self.heading_act), 1)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    def check_heading(self):
        if self.heading_act > 360:
            self.heading_act = self.heading_act - 360
            self.check_heading()
        if self.heading_act < 0:
            self.heading_act = self.heading_act + 360
            self.check_heading()
        if self.heading_req > 360:
            self.heading_req = self.heading_req - 360
            self.check_heading()
        if self.heading_req < 0:
            self.heading_req = self.heading_req + 360
            self.check_heading()

    def set_requested_heading(self, heading: int):
        while heading < 0:
            heading = heading + 360
        while heading > 360:
            heading = heading - 360
        self.heading_req = heading
