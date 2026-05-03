import math


def get_rad_angle(angle: int) -> float:
    return math.radians(angle - 90)


def get_cos_angle(angle: float) -> float:
    return math.cos(angle)


def get_sin_angle(angle: float) -> float:
    return math.sin(angle)


def convert_lat_long_to_nmbr(data: str):
    # TODO : improve the code of this function
    # This function should be improved. It does way too much, and is probably error-prone.
    # It flips value all the time but it works so far
    # Might be better to split it in different parts and make sure those part are simple
    try:
        data = data.split('|')
        if len(data) != 2:
            raise ValueError
    except ValueError:
        print("More than 2 coordinates passed to helper.convert_lat_long_to_nmbr function. Data was : {}".format(data))

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
        else:
            raise ValueError(f"Missing direction in {coord}")
        try:
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

            if is_east:
                return_value = -1 * (degree + minutes / 60 + seconds / 3600)
            else:
                return_value = degree + minutes / 60 + seconds / 3600

            if is_north or is_south:
                return_value = return_value * -1
                converted_coordinates[1] = return_value
            elif is_east or is_west:
                converted_coordinates[0] = return_value

        except ValueError as e:
            print(f"Error in the conversion of lat/long to decimal.{e}")
            return False

    return converted_coordinates

def world_to_screen(pos, offset, zoom):
    return (pos * zoom) - offset
