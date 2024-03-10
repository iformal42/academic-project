import pygame as pg

PATH = "gameasset/Main Characters/Pink Man/"
GRAVITY = 9.8
ALL_SPRITE = {"idle": ["Idle (32x32).png", 11],
              "run": ["Run (32x32).png", 12],
              "jump": ["Jump (32x32).png", 1],
              "hit": ["Hit (32x32).png", 7],
              "fall": ["Fall (32x32).png", 1],
              "double_jump": ["Double Jump (32x32).png", 6],
              "wall_jump": ["Wall Jump (32x32).png", 5]
              }


class Player(pg.sprite.Sprite):
    def __init__(self, width: int, height: int, screen):
        super().__init__()

        self.width, self.height = width, height
        self.window = screen
        self.direction = "right"
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.mask = None
        self.sprites_states = {}

        # storing all sprite into dictionary to respective keys
        for sprite_sheet in ALL_SPRITE:
            character_img = pg.image.load(f"{PATH}{ALL_SPRITE[sprite_sheet][0]}")
            frames = ALL_SPRITE[sprite_sheet][1]
            player_list = []
            for frame in range(frames):
                player_list.append(self.stand(frame, character_img))
            self.sprites_states[sprite_sheet] = player_list

        # self.rect.center = (50, 900 - 96)
        self.current_state = "idle"
        self.animation_rate = 0
        self.fall_count = 0

    def stand(self, frame: int, img):
        """make working sprite sheet """
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(frame * self.width, 0, 2 * self.width, 2 * self.height)
        image.blit(img, (0, 0), self.rect)
        return pg.transform.scale2x(image)

    def fall(self):
        self.fall_count += GRAVITY / 60
        y = min(1, self.fall_count)
        # self.current_state = "fall"
        self.rect.move_ip(0, self.fall_count)

    def animate_player(self):
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

        self.window.blit(img, self.rect)

        return img

    def run(self, horizontal_vel: int, vertical_vel: int = 0):
        # print(self.rect.x, self.rect.y)
        self.rect.move_ip(horizontal_vel, vertical_vel)

        # run the player on screen
        # self.current_state = "run"

    def jump(self, horizontal_vel: int, vertical_vel: int = 0):
        # jump the player on screen
        self.current_state = "jump"
        if self.direction == "left":
            horizontal_vel *= -1
        self.rect.move_ip(horizontal_vel, vertical_vel)

    def updated(self, sprites):
        self.rect = sprites.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pg.mask.from_surface(sprites)
        return self.mask


if __name__ == "__main__":
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((1200, 1000))

    player = Player(32, 32, window)
    sprite = pg.sprite.Group()
    # print(player)
    # print(sprite)
    # sprite.add(player)
    running = True
    while running:
        # 60 FPS
        clock.tick(60)

        window.fill((135, 206, 235))

        player.animate_player()
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
