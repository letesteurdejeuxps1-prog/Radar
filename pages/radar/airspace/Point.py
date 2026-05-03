import pygame


class Point:
    pygame_img = None

    icon_size = (50, 50)

    default_icon: str = 'UNKNOWN'

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
        try:
            point_img_file = "{}\\{}\\{}_{}{}".format(
                root_dir,
                icon_file_folder,
                self.type_of_point,
                color,
                icon_file_format
            )
            img = pygame.image.load(point_img_file).convert_alpha()
            img = pygame.transform.smoothscale(img, self.icon_size)
            self.pygame_img = img
        except FileNotFoundError:
            point_img_file = "{}\\{}\\{}_{}{}".format(
                root_dir,
                icon_file_folder,
                self.default_icon,
                color,
                icon_file_format
            )
            img = pygame.image.load(point_img_file).convert_alpha()
            img = pygame.transform.smoothscale(img, self.icon_size)
            self.pygame_img = img
