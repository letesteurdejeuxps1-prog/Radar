from pages.radar.airspace.Area import Area
from pages.radar.airspace.Aerodrome import Aerodrome
from pages.radar.airspace.Point import Point


class Airspace:

    areas: list[Area]
    aerodrome: list[Aerodrome]
    points: list[Point]

    def __init__(
        self,
        center_x: int = 0,
        center_y: int = 0,
        limit_x: tuple[int, int] = (0, 0),
        limit_y: tuple[int, int] = (0, 0)
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.limit_x = limit_x
        self.limit_y = limit_y
