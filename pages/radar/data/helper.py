import math
from pages.radar.data.immovable_variable import scale_NM_to_su


def get_rad_angle(angle: int) -> float:
    return (angle - 90) * math.pi / 180

def get_cos_angle(angle: float) -> float:
    return math.cos(angle)

def get_sin_angle(angle: float) -> float:
    return math.sin(angle)

def get_wake_distance(preceding_wtc: str, trailing_wtc: str, standard_distance: int = 5) -> int:
    wtc_distance = standard_distance
    if isinstance(preceding_wtc, str) and isinstance(trailing_wtc, str):
        preceding_wtc = preceding_wtc.upper()
        trailing_wtc = trailing_wtc.upper()
        if preceding_wtc == 'J':
            if trailing_wtc == 'H': wtc_distance = 5
            if trailing_wtc == 'M': wtc_distance = 7
            if trailing_wtc == 'L': wtc_distance = 8
        if preceding_wtc == 'H':
            if trailing_wtc == 'H': wtc_distance = 4
            if trailing_wtc == 'M': wtc_distance = 5
        if preceding_wtc == 'M':
            if trailing_wtc == 'L': wtc_distance = 5
    if wtc_distance >= standard_distance:
        return wtc_distance
    else:
        return standard_distance

def can_be_converted_to_nmbr(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def convert_lat_long_to_nmbr(data: str):
    try:
        data = data.split('|')
        if len(data) != 2:
            raise ValueError
    except ValueError:
        print("More than 2 coordiantes passed to helper.convert_lat_long_to_nmbr function. Data was : {}".format(data))

    converted_coordinates = [None, None]
    for coord in data:
        is_north = False
        is_south = False
        is_east = False
        is_west = False
        # TODO : Handle N, S, W, E coordinates
        if coord.endswith('N'):
            coord = coord.removesuffix('N')
            is_north = True
        elif coord.endswith('S'):
            coord = coord.removesuffix('S')
            is_south = True
        elif coord.endswith('W'):
            coord = coord.removesuffix('W')
            is_west = True
        elif coord.endswith('E'):
            coord = coord.removesuffix('E')
            is_east = True
        try:
            if 'Â°' in coord:
                first_split = coord.split('Â°')
            elif 'Â' in coord:
                first_split = coord.split('Â')
            elif '°' in coord:
                first_split = coord.split('°')
            else:
                raise ValueError("Unable to convert {}".format(coord))
            second_split = first_split[-1].split("'")
            degree = int(first_split[0])
            if second_split[0] != '':
                minutes = int(second_split[0])
                if minutes >  60:
                    raise ValueError(" Invalid value for seconds, got {}".format(minutes))
            else:
                minutes = 0
            if len (second_split) == 2 and second_split[1] != '':
                seconds = int(second_split[1].removesuffix("''"))
                if seconds > 60:
                    raise ValueError(" Invalid value for seconds, got {}".format(seconds))
            else:
                seconds = 0

            foo = "{} {} {}".format(degree, minutes, seconds)

            if is_east:
                return_value = -1 * (degree + minutes / 60 + seconds / 60)
            else:
                return_value = degree + minutes / 60 + seconds / 3600

            if is_north or is_south:
                return_value = return_value * -1
                converted_coordinates[1] = return_value * scale_NM_to_su
            elif is_east or is_west:
                converted_coordinates[0] = return_value * scale_NM_to_su

        except ValueError as e:
            print("Error in the conversion of lat/long to decimal.{}".format(e))
            return False

    return converted_coordinates
