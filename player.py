import pygame as pg
import random as rd

PATH = "gameasset/Main Characters/"
player = ["Virtual Guy/", "Ninja Frog/", "Pink Man/", "Mask Dude/"]
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
        self.character = rd.choice(player)
        self.path = f"{PATH}{self.character}"
        self.width, self.height = width, height
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.sprites_states = {}
        for sprite_sheet in ALL_SPRITE:
            character_img = pg.image.load(f"{self.path}{ALL_SPRITE[sprite_sheet][0]}")
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

        self.img = None
        self.air_count, self.air_timer = 0, 30
        self.width, self.height = width, height
        self.direction = "right"
        self.surface = pg.Surface((2 * self.width, 2 * self.height), pg.SRCALPHA).convert_alpha()
        self.mask = pg.mask.from_surface(self.surface)
        self.character_states = self.sprites_states
        self.x_vel, self.y_vel, self.speed = 0, 0, 6
        self.current_state = "idle"
        self.animation_rate = 0
        self.fall_count, self.in_air = 0, True
        self.is_hit, self.hit_count = False, 0
        self.jump_count = 0
        self.rect.x, self.rect.y = 400, 810
        self.let_bounce = False
        self.life = 6

    def update(self):
        """made mask for collision"""
        self.surface = pg.Surface((2 * self.width, 2 * self.height), pg.SRCALPHA).convert_alpha()
        self.surface.blit(self.img, (0, 0))
        self.mask = pg.mask.from_surface(self.surface)

    def animate_player(self):
        """animate the player"""
        self.animation_rate += 0.2

        # player's state
        character_state = self.sprites_states[self.current_state]

        # stabilize animation rate
        if int(self.animation_rate) >= len(character_state):
            self.animation_rate = 0

        if self.direction == "left":
            # for direction left
            self.img = pg.transform.flip(character_state[int(self.animation_rate)], True, False)
        else:
            # for direction right
            self.img = character_state[int(self.animation_rate)]
        self.update()

    def draw(self, screen, offset_x):
        self.animate_player()
        # pg.draw.rect(screen,(255,0,0),self.rect)
        screen.blit(self.surface, (self.rect.x - offset_x, self.rect.y))

    def hit(self):
        self.is_hit = True

    def run(self, horizontal_vel: int, vertical_vel: int = 0):
        """move the sprite"""
        if self.direction == "left":
            self.speed = -6

        else:
            self.speed = 6
        self.x_vel = self.speed
        self.current_state = "run"
        self.rect.move_ip(self.x_vel, vertical_vel)

    def fall(self, should_fall: bool, x_vel):
        """gravity"""
        if should_fall:
            self.in_air = True
            self.current_state = "fall"
            self.fall_count += GRAVITY / 60
            self.rect.move_ip(x_vel, self.fall_count)

    def jump(self, vertical_vel: int = 0):
        """ jump the player on screen"""
        if self.jump_count == 2:
            state = "double_jump"
        else:
            state = "jump"

        self.current_state = state
        self.in_air = True
        self.rect.move_ip(self.x_vel * 0.5, vertical_vel)

    def bounce(self):
        self.let_bounce = True
        self.air_timer = 20
        self.air_count = 0

    def landed(self):
        self.y_vel = 0
        self.fall_count = 0
        self.air_count = 0
        self.jump_count = 0
        self.let_bounce = False
        if not self.is_hit:
            self.current_state = "idle"

        self.in_air, self.air_timer = False, 30

    def loop(self):
        if self.air_count <= self.air_timer and self.jump_count == 2:
            self.jump(self.y_vel)
            self.air_count += 1

        elif self.air_count <= self.air_timer and (self.jump_count > 0 or self.let_bounce):
            self.jump(self.y_vel)
            self.air_count += 1

        if self.air_count > self.air_timer:
            self.y_vel = 0
            self.fall(True, x_vel=self.x_vel * 0.8)

        if self.hit_count >= 90:
            self.is_hit = False
            self.hit_count = 0
            self.life -= 1
        elif self.hit_count < 90 and self.is_hit:
            if self.hit_count < 6:
                self.rect.move_ip(-self.speed, 0)
            self.hit_count += 1
            self.current_state = "hit"



