import pygame as pg
from object import Object

path = "gameasset/Enemy/"
enemies = {
    "mushroom": [f"{path}Mushroom/move.png", 16, 32, 32],
    "chicken": [f"{path}Chicken/move.png", 14, 32, 34],
    "snail": [f"{path}Snail/move.png", 10, 38, 24],
    "bunny": [f"{path}Bunny/move.png", 12, 34, 44],
    "pig": [f"{path}AngryPig/move.png", 16, 36, 30],
    "chameleon": [f"{path}Chamelion/img.png", 8, 84, 38],
    "bat": [f"{path}Bat/img.png", 7, 46, 30],
    "ghost": [f"{path}Ghost/img.png", 10, 44, 30],
    "slime": [f"{path}Slime/img.png", 10, 44, 30],
}


class Enemy(Object):
    def __init__(self, pos_x, pos_y, travel_dist, name="mushroom", flip="last", vel=2):
        """name:-{mushroom,chicken,snail,bunny,pig}"""
        self.name = name
        self.character = enemies[self.name]

        super().__init__(self.character[2], self.character[3], path=enemies[self.name][0],
                         scale_x=self.character[2], scale_y=self.character[3])

        self.img = None
        self.x_vel, self.distance = -vel, travel_dist
        self.all_sprites = [self.build(begin_x=i * self.character[2], begin_y=0) for i in range(self.character[1])]
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.mask = pg.mask.from_surface(self.surface)
        self.pos_x = pos_x
        self.rect.topright = (pos_x, pos_y)
        self.flip_at = flip
        self.animation_rate = 0

    def flip(self):
        flipped_sprites = []
        for sprite in self.all_sprites:
            flipped = pg.transform.flip(sprite, True, False)
            flipped_sprites.append(flipped)
        self.all_sprites.clear()
        self.all_sprites = flipped_sprites

    def move(self):
        if abs(abs(self.rect.x) - self.pos_x) > self.distance or self.flip_at == "first":
            self.pos_x = self.rect.x
            self.x_vel *= -1
            self.flip()
            self.flip_at = "last"
        self.rect.move_ip(self.x_vel, 0)

    def update(self):
        """made mask for collision"""
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.surface.blit(self.img, (0, 0))
        self.mask = pg.mask.from_surface(self.surface)

    def animate(self):
        self.animation_rate += 0.25
        if int(self.animation_rate) >= len(self.all_sprites):
            self.animation_rate = 0
        self.img = self.all_sprites[int(self.animation_rate)]
        self.update()

    def draw(self, screen, offset):
        self.animate()
        self.move()
        screen.blit(self.img, (self.rect.x - offset, self.rect.y))
