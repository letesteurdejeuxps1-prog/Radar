from pages.radar.airspace.Point import Point
from pages.radar.data.helper import convert_lat_and_long_to_radar, latlon_to_world


class Rwy:

    def __init__(
            self,
            rwy_id,
            name_1,
            name_2,
            threshold_1,
            threshold_2,
            magnetic_heading_1,
            magnetic_heading_2,
            as_center_x,
            as_center_y
    ):
        self.rwy_id = rwy_id
        self.name_1 = name_1
        self.name_2 = name_2
        self.threshold_1 = threshold_1
        self.threshold_2 = threshold_2
        self.magnetic_heading_1 = magnetic_heading_1
        self.magnetic_heading_2 = magnetic_heading_2
        self.as_center_x = as_center_x
        self.as_center_y = as_center_y
        self.threshold_1_pt = self.set_threshold_point(self.name_1, self.threshold_1)
        self.threshold_2_pt = self.set_threshold_point(self.name_2, self.threshold_2)

    def set_threshold_point(self, name, data):
        lon, lat = convert_lat_and_long_to_radar(data)
        x, y = latlon_to_world(
            lat,
            lon,
            self.as_center_y,
            self.as_center_x
        )
        return Point(
            name,
            name,
            'THRESHOLD',
            x,
            y,
        )

