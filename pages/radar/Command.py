import pygame


class Command:

    pos_x: int = 20
    pos_y: int = 20

    width: int = 900
    height: int = 140

    padding: int = 8

    color_bg = (25, 25, 25)
    color_border = (255, 255, 255)

    color_text = (255, 255, 255)

    color_input_bg = (10, 10, 10)
    color_input_border = (120, 120, 120)

    color_button_bg = (50, 50, 50)
    color_button_hover = (80, 80, 80)
    color_button_border = (255, 255, 255)

    def __init__(self, surface: pygame.Surface):

        self.input_rect = None | pygame.Rect
        self.title_rect = None | pygame.Rect
        self.surface = surface

        self.font = pygame.font.SysFont("consolas", 18)

        self.selected_acft_name: str = ""

        self.input_text: str = ""
        self.input_active: bool = False

        self.button_values = [
            "0",
            "0.5",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10"
        ]

        self.button_count = len(self.button_values)

        self.buttons = []

        self.rect = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height
        )

        self.build_layout()

    def build_layout(self):

        self.title_rect = pygame.Rect(
            self.pos_x + self.padding,
            self.pos_y + self.padding,
            self.width - self.padding * 2,
            30
        )

        self.input_rect = pygame.Rect(
            self.pos_x + self.padding,
            self.title_rect.bottom + self.padding,
            self.width - self.padding * 2,
            30
        )


        self.buttons.clear()

        button_y = self.input_rect.bottom + self.padding

        available_width = self.width - (self.padding * 2)

        button_spacing = 4

        button_width = (
            available_width - ((self.button_count - 1) * button_spacing)
        ) // self.button_count

        button_height = 30

        for i, value in enumerate(self.button_values):
            x = (
                    self.pos_x
                    + self.padding
                    + (button_width + button_spacing) * i
            )

            rect = pygame.Rect(
                x,
                button_y,
                button_width,
                button_height
            )

            self.buttons.append({
                "rect": rect,
                "text": value,
                "value": value
            })

    def draw(self):

        # =========================
        # MAIN WINDOW
        # =========================

        pygame.draw.rect(
            self.surface,
            self.color_bg,
            self.rect
        )

        pygame.draw.rect(
            self.surface,
            self.color_border,
            self.rect,
            2
        )

        # =========================
        # TITLE BOX
        # =========================

        pygame.draw.rect(
            self.surface,
            (40, 40, 40),
            self.title_rect
        )

        pygame.draw.rect(
            self.surface,
            self.color_border,
            self.title_rect,
            1
        )

        title_surface = self.font.render(
            self.selected_acft_name,
            True,
            self.color_text
        )

        self.surface.blit(
            title_surface,
            (
                self.title_rect.x + 6,
                self.title_rect.y + 5
            )
        )

        # =========================
        # INPUT BOX
        # =========================

        pygame.draw.rect(
            self.surface,
            self.color_input_bg,
            self.input_rect
        )

        border_color = (
            (0, 255, 0)
            if self.input_active
            else self.color_input_border
        )

        pygame.draw.rect(
            self.surface,
            border_color,
            self.input_rect,
            2
        )

        input_surface = self.font.render(
            self.input_text,
            True,
            self.color_text
        )

        self.surface.blit(
            input_surface,
            (
                self.input_rect.x + 6,
                self.input_rect.y + 5
            )
        )

        # =========================
        # BUTTONS
        # =========================

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:

            hovered = button["rect"].collidepoint(mouse_pos)

            pygame.draw.rect(
                self.surface,
                self.color_button_hover if hovered else self.color_button_bg,
                button["rect"]
            )

            pygame.draw.rect(
                self.surface,
                self.color_button_border,
                button["rect"],
                1
            )

            txt_surface = self.font.render(
                button["text"],
                True,
                self.color_text
            )

            txt_rect = txt_surface.get_rect(
                center=button["rect"].center
            )

            self.surface.blit(
                txt_surface,
                txt_rect
            )

    def handle_keydown(self, event):

        if not self.input_active:
            return

        if event.key == pygame.K_BACKSPACE:

            self.input_text = self.input_text[:-1]

        elif event.key == pygame.K_RETURN:

            print("COMMAND:", self.input_text)

            self.input_text = ""

        else:

            self.input_text += event.unicode

    def handle_mouse_click(self, mouse_pos):

        # Input activation
        self.input_active = self.input_rect.collidepoint(mouse_pos)

        # Buttons
        for button in self.buttons:

            if button["rect"].collidepoint(mouse_pos):
                print(f"Clicked value: {button['value']}")


    def set_selected_acft(self, acft):

        if acft is None:
            self.selected_acft_name = ""
        else:
            self.selected_acft_name = acft.cs