from pages.radar.Acft import Acft
from pages.radar.airspace.Point import Point


class QdmAnchor:

    def __init__(
            self,
            world_x: float,
            world_y: float,
            attached_object=None
    ):
        self.world_x = world_x
        self.world_y = world_y

        # Acft | Point | None
        self.attached_object = attached_object

    def get_position(self):

        if isinstance(self.attached_object, Acft):
            return (
                self.attached_object.pos_x,
                self.attached_object.pos_y
            )

        elif isinstance(self.attached_object, Point):
            return (
                self.attached_object.pos_x,
                self.attached_object.pos_y
            )

        return self.world_x, self.world_y