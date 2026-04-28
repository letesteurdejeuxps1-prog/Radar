import json
from pages.radar.airspace.Area import Area
from pages.radar.airspace.Aerodrome import Aerodrome
from pages.radar.airspace.Point import Point
from pages.radar.data.helper import convert_lat_long_to_nmbr


class Airspace:

    areas: list[Area]
    aerodrome: list[Aerodrome]
    points: list[Point]

    center_x: int|float
    center_y: int|float
    limit_w: int|float
    limit_e: int|float
    limit_n: int|float
    limit_s: int|float
    name: str

    def __init__(
        self,
        file: str = ""
    ):
        self.file = file

    def load(self, file: str):
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)
            try:
                self.name = data['name']
                self.center_x = data['center_x']
                self.center_y = data['center_y']
                self.limit_w = data['limit_w']
                self.limit_e = data['limit_e']
                self.limit_n = data['limit_n']
                self.limit_s = data['limit_s']

                points = []
                for point in data['points']:
                    pt = data['points'][point]
                    new_point = Point(
                        point,
                        pt.get('ABBR'),
                        pt.get('type'),
                        convert_lat_long_to_nmbr(pt.get('pos_x')),
                        convert_lat_long_to_nmbr(pt.get('pos_y'))
                    )
                    points.append(new_point)
                self.points = points
                areas = []
                for area in data['areas']:
                    area = data['areas'][area]
                    new_area = Area(
                        area.get('coord'),
                        area.get('limit_low'),
                        area.get('limit_high'),
                        area.get('highest_alt'),
                        area.get('lowest_alt')
                    )
                    areas.append(new_area)
                self.areas = areas
            except KeyError as e:
                print("Could not load airspace. Key {} does not exist or is incorrect".format(e.args[0]))

