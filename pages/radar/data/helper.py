import math


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
    # TODO : Handle N, S, W, E coordinates
    if data.endswith('N'):
        data = data.removesuffix('N')
    elif data.endswith('S'):
        data = data.removesuffix('S')
    elif data.endswith('W'):
        data = data.removesuffix('W')
    elif data.endswith('E'):
        data = data.removesuffix('E')
    try:
        if 'Â°' in data:
            first_split = data.split('Â°')
        elif 'Â' in data:
            first_split = data.split('Â')
        elif '°' in data:
            first_split = data.split('°')
        else:
            raise ValueError("Unable to convert {}".format(data))
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
        return degree + minutes / 60 + seconds / 60
    except ValueError as e:
        print("Error in the conversion of lat/long to decimal.{}".format(e))
        return False


