from pages.radar.airspace.Localizer import Localizer
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

        self.magnetic_heading_1 = int(magnetic_heading_1)
        self.magnetic_heading_2 = int(magnetic_heading_2)

        self.as_center_x = as_center_x
        self.as_center_y = as_center_y

        # ==================================================
        # THRESHOLDS
        # ==================================================

        self.threshold_1_pt = self.set_threshold_point(self.name_1, self.threshold_1)
        self.threshold_2_pt = self.set_threshold_point(self.name_2, self.threshold_2)

        # ==================================================
        # LOCALIZERS
        # ==================================================

        self.localizer_1 = Localizer(self.name_1, self.threshold_1_pt, self.magnetic_heading_1)
        self.localizer_2 = Localizer(self.name_2, self.threshold_2_pt, self.magnetic_heading_2)

        # Active runway
        self.active = self.name_1

    # ==================================================
    # THRESHOLD CREATION
    # ==================================================

    def set_threshold_point(
            self,
            name,
            data
    ):

        lon, lat = convert_lat_and_long_to_radar(data)

        x, y = latlon_to_world(lat, lon, self.as_center_y, self.as_center_x)

        return Point(name, name, 'THRESHOLD', x, y,)

    # ==================================================
    # ACTIVE RWY
    # ==================================================

    def get_active_rwy_name(self):
        if self.active == self.name_1:
            return self.name_1
        return self.name_2

    def get_active_heading(self):
        if self.active == self.name_1:
            return self.magnetic_heading_1
        return self.magnetic_heading_2

    def get_active_threshold(self):
        if self.active == self.name_1:
            return self.threshold_1_pt
        return self.threshold_2_pt

    def get_opposite_threshold(self):
        if self.active == self.name_1:
            return self.threshold_2_pt
        return self.threshold_1_pt

    # ==================================================
    # ACTIVE LOCALIZER
    # ==================================================

    def get_active_localizer(self):
        if self.active == self.name_1:
            return self.localizer_1
        return self.localizer_2

    # ==================================================
    # DRAWER CENTERLINE VECTOR
    # ==================================================

    def get_vector_for_drawer(self):
        localizer = self.get_active_localizer()
        return localizer.get_centerline_vector()

    # ==================================================
    # COMPATIBILITY
    # ==================================================

    def get_rwy_heading_for_centerline(self):
        return (self.get_active_heading() + 180) % 360