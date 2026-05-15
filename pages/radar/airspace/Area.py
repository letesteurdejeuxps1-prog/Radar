class Area:
    def __init__(
            self,
            coordinates: tuple,
            coordinates_converted: list,
            limit_low: int,
            limit_high: int,
            highest_alt: int,
            lowest_alt: int
    ):
        self.coordinates = coordinates
        self.coordinates_converted = coordinates_converted
        self.limit_low = int(limit_low)
        self.limit_high = int(limit_high)
        self.highest_alt = int(highest_alt)
        self.lowest_alt = int(lowest_alt)

    def contains_point(self, x, y):

        inside = False
        points = self.coordinates_converted
        if len(points) < 3:
            return False
        n = len(points)
        p1x, p1y = points[0]
        for i in range(n + 1):
            p2x, p2y = points[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (
                                    (y - p1y)
                                    * (p2x - p1x)
                                    / (p2y - p1y)
                                    + p1x
                            )

                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def contains_acft(self, acft):

        # Horizontal check
        if not self.contains_point(
                acft.real_x,
                acft.real_y
        ):
            return False

        # Vertical check
        if self.limit_low <= acft.altitude_act:
            if acft.altitude_act <= self.limit_high:
                return True

        return False
