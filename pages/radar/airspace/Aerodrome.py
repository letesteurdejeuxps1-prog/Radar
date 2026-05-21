from pages.radar.airspace.Rwy import Rwy
from pages.radar.data.helper import convert_lat_and_long_to_radar, latlon_to_world


class Aerodrome:
    def __init__(self, name, icao, rwy_list, as_center_x, as_center_y):
        self.name: str = name
        self.icao: str = icao
        self.rwy: list[Rwy] = []
        self.set_rwy(rwy_list, as_center_x, as_center_y)

    def set_rwy(self, rwy_list, as_center_x, as_center_y):
        for item in rwy_list:
            runway = Rwy(
                item['id'],
                item['name_1'],
                item['name_2'],
                item['threshold_1'],
                item['threshold_2'],
                item['magnetic_heading_1'],
                item['magnetic_heading_2'],
                as_center_x,
                as_center_y
            )
            self.rwy.append(runway)
