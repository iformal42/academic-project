import pygame as pg

PATH = "gameasset/Main Characters/Mask Dude/"

ALL_SPRITE = {"idle": ["Idle (32x32).png", 11],
              "run": ["Run (32x32).png", 12],
              "jump": ["Jump (32x32).png", 1],
              "hit": ["Hit (32x32).png", 7],
              "fall": ["Fall (32x32).png", 1],
              "double_jump": ["Double Jump (32x32).png", 6],
              "wall_jump": ["Wall Jump (32x32).png", 5]
              }


class Player(pg.sprite.Sprite):
    def __init__(self, width, height, screen):
        super().__init__()

        self.width, self.height = width, height
        self.window = screen
        self.direction = "right"
        self.rect = pg.Rect(0, 0, self.width, self.height)
        # self.rect.x, self.rect.y = 100, 500
        # print(self.rect.center)
        self.sprites_states = {}

        # storing all sprite into dictionary to respective keys
        for sprite_sheet in ALL_SPRITE:
            character_img = pg.image.load(f"{PATH}{ALL_SPRITE[sprite_sheet][0]}")
            frames = ALL_SPRITE[sprite_sheet][1]
            player_list = []
            for frame in range(frames):
                player_list.append(self.stand(frame, character_img))
            self.sprites_states[sprite_sheet] = player_list

        self.current_state = "idle"
        self.animation_rate = 0

    def stand(self, frame, img):
        """make working sprite sheet """
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(frame * self.width, 0, self.width, self.height)
        image.blit(img, (0, 0), self.rect)
        return pg.transform.scale2x(image)

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

        self.window.blit(img, (self.rect.x, self.rect.y))

    def move(self, horizontal_vel, vertical_vel=0):
        # move the player on screen
        self.current_state = "run"
        print(self.rect.x, self.rect.y)
        self.rect.move_ip(horizontal_vel, vertical_vel)


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
                player.move(5)

        pg.display.update()
