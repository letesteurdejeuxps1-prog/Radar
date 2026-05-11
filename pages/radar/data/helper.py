import math


def get_rad_angle(angle: int) -> float:
    return math.radians(90 - angle)


def get_cos_angle(angle: float) -> float:
    return math.cos(angle)


def get_sin_angle(angle: float) -> float:
    return math.sin(angle)


def split_lat_long_to_single_coordinate(data: str) -> list:
    if '|' in data:
        return_data = data.split('|')
    else:
        return_data = [data]
    if len(return_data) > 2:
        raise ValueError(f"Too many info passed to get_single_coordinates: {data}")
    return return_data


def separate_axis_from_coord(coord: str) -> tuple['str', 'str']:
    if coord.endswith('N'):
        coord = coord.removesuffix('N')
        direction = 'N'
    elif coord.endswith('S'):
        coord = coord.removesuffix('S')
        direction = 'S'
    elif coord.endswith('W'):
        coord = coord.removesuffix('W')
        direction = 'W'
    elif coord.endswith('E'):
        coord = coord.removesuffix('E')
        direction = 'E'
    else:
        raise ValueError(f"Missing direction in {coord}")
    return coord, direction


def extract_deg_min_sec_from_str(coord: str) -> tuple[int, int, int]:
    coord = coord.replace("Â", "")
    if '°' in coord:
        first_split = coord.split('°')
    else:
        raise ValueError(f"Unable to convert {coord}")

    second_split = first_split[-1].split("'")
    degree = int(first_split[0])
    if second_split[0] != '':
        minutes = int(second_split[0])
        if minutes > 60:
            raise ValueError(f"Invalid value for seconds, got {minutes}")
    else:
        minutes = 0
    if len(second_split) == 2 and second_split[1] != '':
        seconds = int(second_split[1].removesuffix("''"))
        if seconds > 60:
            raise ValueError(f"Invalid value for seconds, got {seconds}")
    else:
        seconds = 0

    return degree, minutes, seconds


def convert_deg_min_sec_to_sim(data: tuple[int, int, int], axis: str):
    value = data[0] + data[1] / 60 + data[2] / 3600
    if axis == 'W' or axis == 'S':
        value *= -1
    return value


def convert_lat_and_long_to_radar(data: str) -> tuple[float, float]:
    lat = None
    lon = None

    coordinates = split_lat_long_to_single_coordinate(data)

    for coord in coordinates:
        coord_val, direction = separate_axis_from_coord(coord)
        deg_min_sec = extract_deg_min_sec_from_str(coord_val)
        value = convert_deg_min_sec_to_sim(deg_min_sec, direction)

        if direction in ('N', 'S'):
            lat = value
        elif direction in ('E', 'W'):
            lon = value

    if lat is None or lon is None:
        raise ValueError("Missing lat or lon")

    return lon, lat


def world_to_screen_x(pos, offset, zoom):
    return (pos * zoom) - offset


def world_to_screen_y(pos, offset, zoom):
    return (-pos * zoom) - offset


def latlon_to_world(lat, lon, origin_lat, origin_lon):
    x = (lon - origin_lon) * 60 * math.cos(math.radians(origin_lat))
    y = (lat - origin_lat) * 60
    return x, y

def validate_ssr(ssr):
    checker = str(ssr)
    if len(checker) == 4:
        for nmbr in checker:
            if 0 <= int(nmbr) <= 7:
                pass
            else:
                return False
        return ssr
    return False
