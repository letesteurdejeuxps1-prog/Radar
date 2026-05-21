from pages.radar.airspace.Rwy import Rwy
from pages.radar.data.helper import convert_lat_and_long_to_radar, latlon_to_world


class Aerodrome:
    def __init__(
            self,
            name,
            icao,
            rwy_list,
            ctr,
            limit_low,
            limit_high,
            as_center_x,
            as_center_y
    ):

        self.name = name
        self.icao = icao
        self.ctr = ctr
        self.limit_low = limit_low
        self.limit_high = limit_high

        self.ctr_coordinates = []
        self.rwy = []

        self.set_coordinates(
            as_center_x,
            as_center_y
        )

        self.set_rwy(
            rwy_list,
            as_center_x,
            as_center_y
        )

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

    def set_coordinates(self, as_center_x, as_center_y):
        self.ctr_coordinates = []
        for coords in self.ctr:
            lon, lat = convert_lat_and_long_to_radar(coords)
            x, y = latlon_to_world(
                lat,
                lon,
                as_center_y,
                as_center_x
            )
            self.ctr_coordinates.append((x, y))

