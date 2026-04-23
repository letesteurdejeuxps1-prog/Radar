import pygame

from pages.Variables import Variables


class Main:

    game_acft_id_counter: int = 1
    game_acft_selected_id: int = 0

    main_clock: pygame.time.Clock = pygame.time.Clock()
    main_running: bool = False
    main_second_counter: int = 1

    radar_color_bg: tuple[int, int, int] = (0, 0, 0)

    zoom: int|float = 1
    cam_offset_x: int = 0
    cam_offset_y: int = 0

    def __init__(self, v: Variables) -> None:
        self.main_running = True
        self.main_counter = 0
        self.main_surface = None
        self.variables = v
        self.init()

    def init(self) -> None:
        pygame.init()
        self.main_surface = pygame.display.set_mode((self.variables.display_width, self.variables.display_height))
        pygame.display.set_caption(self.variables.game_caption)
        self.test_init()

    def test_init(self):
        pass

    def test(self):
        pass

    def draw(self):
        # Adapt tests to zoom
        self.test_draw()


    def test_draw(self):
        items = (
            ((255, 0, 255), (10, 10, 60, 70)),
            ((0, 255, 255), (100, 140, 200, 70)),
            ((255, 255, 0), (35, 35, 600, 10)),
            ((255, 50, 50), (70, 80, 30, 30))
        )
        for item in items:
            pygame.draw.rect(
                self.main_surface,
                item[0],
                (
                    item[1][0] * self.zoom + self.cam_offset_x,
                    item[1][1] * self.zoom + self.cam_offset_y,
                    item[1][2] * self.zoom,
                    item[1][3] * self.zoom
                )
            )

    def run(self) -> None:
        while self.main_running:
            self.update_counter()
            self.main_surface.fill(self.radar_color_bg)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main_running = False
                if event.type == pygame.KEYDOWN:
                    self.handle_event_key_down(event.key)

            # TODO REMOVE TEST FUNCTION
            self.test()
            self.test_draw()
            pygame.display.flip()
            self.main_clock.tick(self.variables.display_fps)

        pygame.quit()

    def handle_event_key_down(self, key_pressed):
        if key_pressed == pygame.K_KP_PLUS:
            self.zoom += 0.2
            print("Zoom OUT TO {}".format(self.zoom))
        elif key_pressed == pygame.K_KP_MINUS:
            self.zoom -= 0.2
            print("Zoom OUT TO {}".format(self.zoom))
        elif key_pressed == pygame.K_DOWN:
            print("DOWN")
            self.cam_offset_y -= 10
        elif key_pressed == pygame.K_UP:
            print("UP")
            self.cam_offset_y += 10
        elif key_pressed == pygame.K_LEFT:
            print("LEFT")
            self.cam_offset_x -= 10
        elif key_pressed == pygame.K_RIGHT:
            print("RIGHT")
            self.cam_offset_x += 10


    def update_counter(self) -> None:
        self.main_second_counter += 1
        # TODO : REMOVE AFTER DEBUG, ENABLE PLANE TO MOVE EVERY TICK AND NOT ONCE PER SEC
        if self.main_second_counter >= self.variables.display_fps // 6:
            self.main_second_counter = 0

