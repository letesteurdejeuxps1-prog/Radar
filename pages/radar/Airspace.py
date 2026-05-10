import json
from pages.radar.airspace.Area import Area
from pages.radar.airspace.Aerodrome import Aerodrome
from pages.radar.airspace.Point import Point
from pages.radar.data.helper import convert_lat_and_long_to_radar, latlon_to_world


class Airspace:
    areas: list[Area]
    aerodrome: list[Aerodrome]
    points: list[Point]

    center: int | float
    default_zoom: int | float
    limit_w: int | float
    limit_e: int | float
    limit_n: int | float
    limit_s: int | float
    name: str

    def __init__(
            self,
            file: str = "",
            airspace_center_x: int | float = 0,
            airspace_center_y: int | float = 0,
    ):
        self.file = file
        self.airspace_center_x = airspace_center_x
        self.airspace_center_y = airspace_center_y

    def load(self, file: str):
        with open(file, 'r') as raw_data:
            data = json.load(raw_data)

        try:
            self.name = data['name']
            self.center = data['center']
            self.default_zoom = data['default_zoom']

            center_lon = None
            center_lat = None

            for point_name in data['points']:
                pt = data['points'][point_name]

                lon, lat = convert_lat_and_long_to_radar(pt.get('coord'))

                if (
                        str(point_name).upper() == str(self.center).upper()
                        or
                        str(pt.get('ABBR')).upper() == str(self.center).upper()
                ):
                    center_lon = lon
                    center_lat = lat
                    break

            if center_lon is None or center_lat is None:
                raise ValueError("No airspace center found")

            self.airspace_center_x = center_lon
            self.airspace_center_y = center_lat

            points = []

            for point_name in data['points']:
                pt = data['points'][point_name]

                lon, lat = convert_lat_and_long_to_radar(pt.get('coord'))

                x, y = latlon_to_world(
                    lat,
                    lon,
                    center_lat,
                    center_lon
                )

                new_point = Point(
                    point_name,
                    pt.get('ABBR'),
                    pt.get('TYPE'),
                    x,
                    y
                )

                points.append(new_point)

            self.points = points

            areas = []

            for area_name in data['areas']:
                area = data['areas'][area_name]

                coordinates = []

                for item in area.get('coord'):
                    lon, lat = convert_lat_and_long_to_radar(item)

                    x, y = latlon_to_world(
                        lat,
                        lon,
                        center_lat,
                        center_lon
                    )

                    coordinates.append((x, y))

                new_area = Area(
                    area.get('coord'),
                    coordinates,
                    area.get('limit_low'),
                    area.get('limit_high'),
                    area.get('highest_alt'),
                    area.get('lowest_alt')
                )

                areas.append(new_area)

            self.areas = areas

            return center_lon, center_lat

        except KeyError as e:
            print(f"Could not load airspace. Key {e.args[0]} does not exist or is incorrect")
