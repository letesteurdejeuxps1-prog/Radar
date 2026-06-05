import math

from pages.radar.airspace.Point import Point


class Localizer:
    def __init__(
            self,
            runway_name: str,
            threshold: Point,
            runway_heading: int,
            intercept_angle: int = 30,
            localizer_capture_distance_nm: int = 30
    ):

        self.runway_name = runway_name

        self.threshold = threshold

        self.runway_heading = runway_heading

        # Aircraft approach direction
        self.approach_heading = (
            runway_heading + 180
        ) % 360

        self.intercept_angle = intercept_angle
        self.localizer_capture_distance_nm = localizer_capture_distance_nm

        # Geometry
        self.centerline_fixes = (self.create_centerline_fixes())
        self.intercept_area = (self.create_intercept_area())


    # ==================================================
    # VECTOR HELPERS
    # ==================================================

    @staticmethod
    def heading_to_vector(heading):

        rad = math.radians(90 - heading)
        dx = math.cos(rad)
        dy = math.sin(rad)
        return dx, dy

    # ==================================================
    # CENTERLINE FIXES
    # ==================================================

    def create_centerline_fixes(self):

        dx, dy = self.heading_to_vector(self.approach_heading)

        fixes = {}

        for dist in [10, 8, 6, 4, 2]:

            x = self.threshold.pos_x + dx * dist
            y = self.threshold.pos_y + dy * dist

            fixes[dist] = Point(
                f"{self.runway_name}_{dist}NM",
                f"{dist}NM",
                "ILS_FIX",
                x,
                y
            )
        return fixes

    # ==================================================
    # INTERCEPT AREA
    # ==================================================

    @staticmethod
    def get_intercept_hypotenuse_length(intercept_angle, intercept_range_nm):
        return intercept_range_nm / math.cos(math.radians(intercept_angle))

    def create_intercept_area(self):

        left_heading = (self.approach_heading - self.intercept_angle) % 360
        right_heading = (self.approach_heading + self.intercept_angle) % 360
        dx_left, dy_left = self.heading_to_vector(left_heading)
        dx_right, dy_right = self.heading_to_vector(right_heading)
        hypotenuse = self.get_intercept_hypotenuse_length(self.intercept_angle, self.localizer_capture_distance_nm)
        left_x = self.threshold.pos_x + dx_left * hypotenuse
        left_y = self.threshold.pos_y + dy_left * hypotenuse
        right_x = self.threshold.pos_x + dx_right * hypotenuse
        right_y = self.threshold.pos_y + dy_right * hypotenuse

        return [
            (
                self.threshold.pos_x,
                self.threshold.pos_y
            ),
            (
                left_x,
                left_y
            ),
            (
                right_x,
                right_y
            ),
        ]

    # ==================================================
    # CENTERLINE VECTOR
    # ==================================================

    def get_centerline_vector(self):
        return self.heading_to_vector(
            self.approach_heading
        )

    # ==================================================
    # POINT INSIDE INTERCEPT AREA
    # ==================================================

    def is_inside_intercept_area(
            self,
            px,
            py
    ):

        (x1, y1), (x2, y2), (x3, y3) = self.intercept_area
        denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

        if denominator == 0:
            return False

        a = ((y2 - y3) * (px - x3) + (x3 - x2) * (py - y3)) / denominator
        b = ((y3 - y1) * (px - x3) + (x1 - x3) * (py - y3)) / denominator
        c = 1 - a - b

        return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1

    def get_cross_track_error(self, px, py):

        dx, dy = self.heading_to_vector(self.approach_heading)
        rel_x = px - self.threshold.pos_x
        rel_y = py - self.threshold.pos_y
        # signed lateral distance
        return rel_x * (-dy) + rel_y * dx
