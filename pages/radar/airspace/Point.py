class Point:

    def __init__(
        self,
        name: str,
        abbreviation: str,
        pos_x: int|float = 0,
        pos_y: int|float = 0,
    ):
        self.name = name
        self.abbreviation = abbreviation
        self.pos_x = pos_x
        self.pos_y = pos_y
