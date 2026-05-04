from pages.radar.data.helper import convert_lat_and_long_to_radar
from pages.radar.data.immovable_variable import scale_NM_to_su


class Acft:
    d_acft_width: int = 11
    d_acft_height: int = 11
    d_acft_color_ident: tuple[int, int, int] = (255, 255, 255)
    d_acft_color_conflict: tuple[int, int, int] = (255, 255, 255)
    d_prl_color: tuple[int, int, int] = (255, 255, 255)
    d_prl_width: int = 1
    d_prl_length: int = 60

    pos_x: int | float = 0
    pos_y: int | float = 0

    turn_by_sec: int = 3

    def __init__(
            self,
            identity: int,
            cs: str = '',
            coord_x: str = '',
            coord_y: str = '',

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
    ) -> None:
        self.identity = identity
        self.cs = cs
        self.coord_x = coord_x
        self.coord_y = coord_y
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
        self.after_load()

    def after_load(self):
        lon, lat =  convert_lat_and_long_to_radar(f"{self.coord_x}|{self.coord_y}")
        self.pos_x = lon
        self.pos_y = lat

    def tick(self):
        self.check_heading()
        self.move_logic()

    def check_heading(self):
        pass

    def move_logic(self):
        self.move_logic_heading()
        self.move_logic_speed()

    def move_logic_heading(self):
        pass

    def move_logic_speed(self):
        pass
