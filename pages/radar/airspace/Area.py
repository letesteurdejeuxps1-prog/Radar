import pygame

class Area:
    def __init__(
        self,
        coordinates: tuple[int, ...],
        limit_low: int,
        limit_high: int,
        highest_alt: int,
        lowest_alt: int
    ):
        self.coordinates = coordinates
        self.limit_low = limit_low
        self.limit_high = limit_high
        self.highest_alt = highest_alt
        self.lowest_alt = lowest_alt