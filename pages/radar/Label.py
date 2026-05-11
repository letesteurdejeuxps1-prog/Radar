import pygame


class Label:

    # =========================
    # COLORS
    # =========================

    color_font = (255, 255, 255)
    color_bg = (0, 0, 0)
    color_border = (255, 255, 255)

    # =========================
    # DISPLAY STATES
    # =========================

    STATE_COLLAPSED = 0
    STATE_MEDIUM = 1
    STATE_FULL = 2

    # =========================
    # INIT
    # =========================

    def __init__(self, trl: int = 6000):

        self.TRL = trl
        self.font_size = 15
        self.font = pygame.font.SysFont("consolas", self.font_size)

        # Relative position from aircraft
        self.rel_pos_x = 20
        self.rel_pos_y = -20

        # Padding inside label
        self.padding = 4

        # Current display mode
        self.display_state = self.STATE_COLLAPSED

        # Dragging
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Last drawn rect
        self.last_draw_rect = pygame.Rect(0, 0, 0, 0)

    # =========================
    # STATE
    # =========================

    def next_state(self):

        self.display_state += 1

        if self.display_state > self.STATE_FULL:
            self.display_state = self.STATE_COLLAPSED

    # =========================
    # DRAW
    # =========================

    def draw(
            self,
            surface: pygame.Surface,
            aircraft_screen_x,
            aircraft_screen_y,
            vals: dict
    ):

        # Final label position
        draw_x = aircraft_screen_x + self.rel_pos_x
        draw_y = aircraft_screen_y + self.rel_pos_y

        # =========================
        # BUILD TEXT LINES
        # =========================

        lines = []

        # COLLAPSED
        if self.display_state == self.STATE_COLLAPSED:

            lines.append(
                f"{vals['cs']}  {self.alt_to_label(vals["altitude_act"])}"
            )

        # MEDIUM
        elif self.display_state == self.STATE_MEDIUM:

            lines.append(
                f"{vals['cs']}  {vals['wtc']}"
            )

            lines.append(
                f"{self.alt_to_label(vals['altitude_act'])} "
                f"{int(vals['act_speed_gs'])}"
            )

        # FULL
        elif self.display_state == self.STATE_FULL:

            lines.append(
                f"{vals['cs']} {vals['icao_type']} {vals['wtc']}"
            )

            lines.append(
                f"SSR {vals['ssr']} | GS: {int(vals['act_speed_gs'])}"
            )

            lines.append(
                f"HDG {int(vals['heading_act'])} / {int(vals['heading_req'])}"
            )

            lines.append(
                f"ALT:{self.alt_to_label(vals['altitude_act'])} / {self.alt_to_label(vals['altitude_req'])}"
            )

            lines.append(
                f"IAS:{vals['act_speed_ias']} / {vals['req_speed_ias']}"
            )


        # Safety
        if len(lines) == 0:
            return

        # =========================
        # CALCULATE SIZE
        # =========================

        max_width = 0

        for line in lines:

            txt_surface = self.font.render(
                line,
                True,
                self.color_font
            )

            max_width = max(
                max_width,
                txt_surface.get_width()
            )

        line_height = self.font_size

        box_width = max_width + (self.padding * 2)

        box_height = (
                len(lines) * line_height
                + (self.padding * 2)
        )

        # =========================
        # DRAW BACKGROUND
        # =========================

        background_rect = pygame.Rect(
            draw_x,
            draw_y,
            box_width,
            box_height
        )

        pygame.draw.rect(
            surface,
            self.color_bg,
            background_rect
        )

        pygame.draw.rect(
            surface,
            self.color_border,
            background_rect,
            1
        )

        # Save rect for collision
        self.last_draw_rect = background_rect

        # =========================
        # DRAW TEXT
        # =========================

        for i, line in enumerate(lines):

            txt_surface = self.font.render(
                line,
                True,
                self.color_font
            )

            surface.blit(
                txt_surface,
                (
                    draw_x + self.padding,
                    draw_y + self.padding + (i * line_height)
                )
            )

        # =========================
        # DRAW CONNECTOR LINE
        # =========================

        pygame.draw.line(
            surface,
            self.color_font,
            (aircraft_screen_x, aircraft_screen_y),
            (
                draw_x,
                draw_y + (box_height // 2)
            ),
            1
        )

    # =========================
    # MOUSE
    # =========================

    def is_mouse_over(self, mouse_x, mouse_y):

        return self.last_draw_rect.collidepoint(
            mouse_x,
            mouse_y
        )

    # =========================
    # DRAGGING
    # =========================

    def start_drag(self, mouse_x, mouse_y):

        self.dragging = True

        self.drag_offset_x = mouse_x - self.last_draw_rect.x
        self.drag_offset_y = mouse_y - self.last_draw_rect.y

    def stop_drag(self):

        self.dragging = False

    def drag(
            self,
            mouse_x,
            mouse_y,
            aircraft_screen_x,
            aircraft_screen_y
    ):

        if not self.dragging:
            return

        # New absolute label position
        new_x = mouse_x - self.drag_offset_x
        new_y = mouse_y - self.drag_offset_y

        # Convert to relative position
        self.rel_pos_x = new_x - aircraft_screen_x
        self.rel_pos_y = new_y - aircraft_screen_y

    # =========================
    # HELPERS
    # =========================

    def alt_to_label(self, value):
        return int(value / 100)