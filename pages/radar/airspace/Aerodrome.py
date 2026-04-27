class Aerodrome:
    def __init__(
        self,
        rwy_01: int,
        rwy_02: int,
        limit_high: int,
        highest_alt: int,
    ):
        self.rwy_01 = rwy_01
        self.rwy_02 = rwy_02
        self.limit_high = limit_high
        self.highest_alt = highest_alt

