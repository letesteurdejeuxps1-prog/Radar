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

        self.EMERGENCY_CODE = "EM"
        self.COM_FAILURE_CODE = "CF"
        self.HIJACK = "HI"
        self.emergency_color = (255, 50, 50)
        self.TRL = trl
        self.font_size = 15
        self.font = pygame.font.SysFont("consolas", self.font_size)

        # Relative position from aircraft
        self.rel_pos_x = 20
        self.rel_pos_y = -20

        # Padding inside label
        self.padding = 4

        # Current display mode
        self.display_state = self.STATE_MEDIUM

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


        ssr = self.get_ssr_status(vals['ssr'])
        if isinstance(ssr, tuple):
            ssr_content = ssr[0]
            border_color = ssr[1]
        else:
            ssr_content = ""
            border_color = self.color_border


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
                f"{vals['cs']}  {self.alt_to_label(vals["altitude_act"])}  {ssr_content}"
            )

        # MEDIUM
        elif self.display_state == self.STATE_MEDIUM:

            lines.append(
                f"{vals['cs']}  {vals['wtc']}  {ssr_content}"
            )

            lines.append(
                f"{self.alt_to_label(vals['altitude_act'])} "
                f"{int(vals['act_speed_gs'])}"
            )

        # FULL
        elif self.display_state == self.STATE_FULL:

            lines.append(
                f"{vals['cs']} {vals['icao_type']} {vals['wtc']}  {ssr_content}"
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
                f"RoC: {vals['rate_of_climb']} ft/sec"
            )

            lines.append(
                f"IAS:{int(vals['act_speed_ias'])} / {int(vals['req_speed_ias'])}"
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
            border_color,
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

        anchor_x, anchor_y = self.get_connector_anchor(
            aircraft_screen_x,
            aircraft_screen_y,
            draw_x,
            draw_y,
            box_width,
            box_height
        )

        pygame.draw.line(
            surface,
            self.color_font,
            (aircraft_screen_x, aircraft_screen_y),
            (anchor_x, anchor_y),
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
    
    def get_ssr_status(self, ssr):
        ssr = str(ssr)
        if ssr == "7700":
            return self.EMERGENCY_CODE, self.emergency_color
        elif ssr == "7600" or ssr == "7601":
            return self.COM_FAILURE_CODE, self.emergency_color
        elif ssr == "7500":
            return self.HIJACK, self.emergency_color
        else:
            return False

    def get_connector_anchor(
            self,
            aircraft_x,
            aircraft_y,
            label_x,
            label_y,
            label_w,
            label_h
    ):
        """
        Returns best connector point on label border.
        """

        center_x = label_x + (label_w / 2)
        center_y = label_y + (label_h / 2)

        dx = aircraft_x - center_x
        dy = aircraft_y - center_y

        # =========================
        # HORIZONTAL SIDE
        # =========================

        if abs(dx) > abs(dy):

            # Aircraft LEFT of label
            if dx < 0:

                # top-left
                if dy < -(label_h * 0.33):
                    return label_x, label_y

                # bottom-left
                elif dy > (label_h * 0.33):
                    return label_x, label_y + label_h

                # middle-left
                else:
                    return label_x, label_y + (label_h / 2)

            # Aircraft RIGHT of label
            else:

                # top-right
                if dy < -(label_h * 0.33):
                    return label_x + label_w, label_y

                # bottom-right
                elif dy > (label_h * 0.33):
                    return label_x + label_w, label_y + label_h

                # middle-right
                else:
                    return label_x + label_w, label_y + (label_h / 2)

        # =========================
        # VERTICAL SIDE
        # =========================

        else:

            # Aircraft ABOVE label
            if dy < 0:

                # top-left
                if dx < -(label_w * 0.33):
                    return label_x, label_y

                # top-right
                elif dx > (label_w * 0.33):
                    return label_x + label_w, label_y

                # middle-top
                else:
                    return label_x + (label_w / 2), label_y

            # Aircraft BELOW label
            else:

                # bottom-left
                if dx < -(label_w * 0.33):
                    return label_x, label_y + label_h

                # bottom-right
                elif dx > (label_w * 0.33):
                    return label_x + label_w, label_y + label_h

                # middle-bottom
                else:
                    return label_x + (label_w / 2), label_y + label_h