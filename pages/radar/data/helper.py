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