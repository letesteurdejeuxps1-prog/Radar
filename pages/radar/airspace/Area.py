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
        limit_low: int = limit_low
        limit_high: int = limit_high
        highest_alt: int = highest_alt
        lowest_alt: int = lowest_alt