class Point:

    def __init__(
        self,
        name: str,
        abbreviation: str,
        type_of_point: str,
        pos_x: int|float = 0,
        pos_y: int|float = 0,
    ):
        self.name = name
        self.abbreviation = abbreviation
        self.type_of_point = type_of_point
        self.pos_x = pos_x
        self.pos_y = pos_y
