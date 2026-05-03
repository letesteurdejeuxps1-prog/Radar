import pygame


class Point:
    pygame_img = None

    def __init__(
            self,
            name: str,
            abbreviation: str,
            type_of_point: str,
            pos_x: int | float = 0,
            pos_y: int | float = 0,
    ):
        self.name = name
        self.abbreviation = abbreviation
        self.type_of_point = type_of_point
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_image_file(self, root_dir: str, icon_file_folder: str, color: str, icon_file_format: str):
        point_img_file = "{}\\{}\\{}_{}{}".format(
            root_dir,
            icon_file_folder,
            self.type_of_point,
            color,
            icon_file_format
        )
        self.pygame_img = pygame.image.load(point_img_file)
