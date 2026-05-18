import pygame


class TodoBox:

    def __init__(self, surface: pygame.Surface):

        self.surface = surface

        self.font = pygame.font.SysFont("consolas", 16)

        self.x = 40
        self.y = 300

        self.width = 320
        self.height = 180

        self.dragging = False

        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.selected_acft = None

        self.bg_color = (20, 20, 20)
        self.border_color = (180, 180, 180)
        self.text_color = (255, 255, 255)

        self.header_height = 24

    def set_selected_acft(self, acft):
        self.selected_acft = acft

    def draw(self):

        # Only show when aircraft selected
        if self.selected_acft is None:
            return

        rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # Background
        pygame.draw.rect(
            self.surface,
            self.bg_color,
            rect
        )

        # Border
        pygame.draw.rect(
            self.surface,
            self.border_color,
            rect,
            1
        )

        # Header
        header_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.header_height
        )

        pygame.draw.rect(
            self.surface,
            (40, 40, 40),
            header_rect
        )

        title = f"TODO LIST - {self.selected_acft.cs}"

        title_surface = self.font.render(
            title,
            True,
            self.text_color
        )

        self.surface.blit(
            title_surface,
            (self.x + 6, self.y + 4)
        )

        # Draw todo items
        start_y = self.y + self.header_height + 8

        if len(self.selected_acft.todo_list) == 0:
            empty_surface = self.font.render(
                "No pending items",
                True,
                (120, 120, 120)
            )

            self.surface.blit(
                empty_surface,
                (self.x + 8, start_y)
            )

            return

        for i, item in enumerate(self.selected_acft.todo_list):
            text = self.format_item(item)

            text_surface = self.font.render(
                text,
                True,
                self.text_color
            )

            self.surface.blit(
                text_surface,
                (self.x + 8, start_y + i * 22)
            )

    def format_item(self, item):

        try:
            target_type = item["target_type"]
            target = item["target"]
            command = item["command"]

            if target_type == "l":
                prefix = f"AT FL{target}"

            elif target_type == "f":
                prefix = f"AT {target}"

            else:
                prefix = "AT ?"

            cmd = command.get("cmd", "")

            value = command.get("value", "")

            return f"{prefix} -> {cmd} {value}"

        except Exception:
            return "INVALID TODO ITEM"

    def handle_mouse_click(self, mouse_pos):

        if self.selected_acft is None:
            return False

        mouse_x, mouse_y = mouse_pos

        header_rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.header_height
        )

        if header_rect.collidepoint(mouse_x, mouse_y):
            self.dragging = True

            self.drag_offset_x = mouse_x - self.x
            self.drag_offset_y = mouse_y - self.y

            return True

        return False

    def handle_mouse_release(self):

        self.dragging = False

    def handle_mouse_motion(self, mouse_pos):

        if not self.dragging:
            return

        mouse_x, mouse_y = mouse_pos

        self.x = mouse_x - self.drag_offset_x
        self.y = mouse_y - self.drag_offset_y
