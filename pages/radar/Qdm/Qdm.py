import math
from pages.radar.Qdm.QdmAnchor import QdmAnchor


class Qdm:
    color = (200, 200, 50)
    width = 1

    def __init__(
            self,
            start_anchor: QdmAnchor
    ):
        self.start_anchor = start_anchor
        self.end_anchor: QdmAnchor | None = None
        self.active = True

    def finalize(self, end_anchor: QdmAnchor):
        self.end_anchor = end_anchor
        self.active = False

    def get_positions(self):
        start = self.start_anchor.get_position()
        if self.end_anchor is not None:
            end = self.end_anchor.get_position()
        else:
            end = None

        return start, end

    def get_distance_between(self, start, end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        return math.hypot(dx, dy)

    def get_heading_between(self, start, end):

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        angle = math.degrees(
            math.atan2(dy, dx)
        )
        heading = (90 - angle) % 360

        return round(heading)

    def get_distance(self):

        start, end = self.get_positions()

        if end is None:
            return 0

        return self.get_distance_between(start, end)

    def get_heading(self):
        start, end = self.get_positions()
        if end is None:
            return 0

        return self.get_heading_between(start, end)

    def get_reciprocal_heading(self):
        return (self.get_heading() + 180) % 360


    def get_active_distance(self, temp_end_pos):
        start = self.start_anchor.get_position()
        return self.get_distance_between(start, temp_end_pos)

    def get_active_heading(self, temp_end_pos):
        start = self.start_anchor.get_position()
        return self.get_heading_between(start, temp_end_pos)

    def get_active_reciprocal_heading(self, temp_end_pos):

        return (self.get_active_heading(temp_end_pos) + 180) % 360
