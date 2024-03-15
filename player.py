import pygame as pg

PATH = "gameasset/Main Characters/Mask Dude/"
GRAVITY = 9.8
ALL_SPRITE = {"idle": ["Idle (32x32).png", 11],
              "run": ["Run (32x32).png", 12],
              "jump": ["Jump (32x32).png", 1],
              "hit": ["Hit (32x32).png", 7],
              "fall": ["Fall (32x32).png", 1],
              "double_jump": ["Double Jump (32x32).png", 6],
              "wall_jump": ["Wall Jump (32x32).png", 5]
              }


class Sprite(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.width, self.height = width, height
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.sprites_states = {}
        for sprite_sheet in ALL_SPRITE:
            character_img = pg.image.load(f"{PATH}{ALL_SPRITE[sprite_sheet][0]}")
            frames = ALL_SPRITE[sprite_sheet][1]
            player_list = []
            for frame in range(frames):
                player_list.append(self.stand(frame, character_img))
            self.sprites_states[sprite_sheet] = player_list

    def stand(self, frame: int, img):
        """make working sprite sheet """
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(frame * self.width, 0, 2 * self.width, 2 * self.height)
        image.blit(img, (0, 0), self.rect)
        return pg.transform.scale2x(image)


class Player(Sprite):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        self.air_count, self.air_timer = 0, 30
        self.width, self.height = width, height
        self.direction = "right"
        self.surface = pg.Surface((2 * self.width, 2 * self.height), pg.SRCALPHA).convert_alpha()
        self.mask = pg.mask.from_surface(self.surface)
        self.character_states = self.sprites_states
        self.y_vel = 5
        self.current_state = "idle"
        self.animation_rate = 0
        self.fall_count, self.in_air = 0, True
        self.jump_count = 0
        self.rect.x = 500

    def fall(self, should_fall: bool, horizontal_vel):
        """gravity"""
        if self.direction == "left":
            horizontal_vel *= -1

        if should_fall:
            self.in_air = True
            self.current_state = "fall"
            self.fall_count += GRAVITY / 60
            self.rect.move_ip(horizontal_vel, self.fall_count)

    def update(self, img):
        """made mask for collision"""
        self.surface = pg.Surface((2 * self.width, 2 * self.height), pg.SRCALPHA).convert_alpha()
        self.surface.blit(img, (0, 0))
        self.mask = pg.mask.from_surface(self.surface)

    def animate_player(self, screen):
        """animate the player"""
        self.animation_rate += 0.20

        # player's state
        character_state = self.sprites_states[self.current_state]

        # stabilize animation rate
        if int(self.animation_rate) >= len(character_state):
            self.animation_rate = 0

        if self.direction == "left":
            # for direction left
            img = pg.transform.flip(character_state[int(self.animation_rate)], True, False)
        else:
            # for direction right
            img = character_state[int(self.animation_rate)]
        self.update(img)
        # pg.draw.rect(screen,(255,0,0),self.rect)
        screen.blit(self.surface, self.rect)

    def run(self, horizontal_vel: int, vertical_vel: int = 0):
        """move the sprite"""
        self.current_state = "run"
        self.rect.move_ip(horizontal_vel, vertical_vel)

    def jump(self, horizontal_vel: int, vertical_vel: int = 0):
        """ jump the player on screen"""
        if self.direction == "left":
            horizontal_vel *= -1

        if self.jump_count == 2:
            state = "double_jump"

        else:
            state = "jump"

        self.current_state = state
        self.in_air = True
        self.rect.move_ip(horizontal_vel, vertical_vel)

    def landed(self):
        self.fall_count = 0
        self.air_count = 0
        self.jump_count = 0
        self.current_state = "idle"
        self.in_air, self.air_timer = False, 30

    def loop(self):
        if self.air_count <= self.air_timer and self.jump_count == 2:
            self.jump(3, -5)
            self.air_count += 1

        elif self.air_count <= self.air_timer and self.jump_count > 0:
            self.jump(4, -5)
            self.air_count += 1

        if self.air_count > self.air_timer:
            self.fall(True, 3)


if __name__ == "__main__":
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((1200, 1000))

    player = Player(32, 32)
    sprite = pg.sprite.Group()
    # print(player)
    # print(sprite)
    # sprite.add(player)
    running = True
    while running:
        # 60 FPS
        clock.tick(60)

        window.fill((135, 206, 235))

        player.animate_player(window)
        # sprite.draw(window)
        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                print("yes")
                player.run(5)

        pg.display.update()
