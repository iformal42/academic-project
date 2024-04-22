import pygame as pg
import random as rd

PATH = "gameasset/Terrain/Terrain (16x16).png"


class Object(pg.sprite.Sprite):
    def __init__(self, width: int, height: int, path=PATH, scale_x=42, scale_y=16):
        super().__init__()
        self.SCALE_X, self.SCALE_Y = scale_x, scale_y
        self.width, self.height = width, height
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.block_w, self.block_h = self.width + self.SCALE_X, self.height + self.SCALE_Y
        self.image = pg.image.load(path)

    def build(self, begin_x, begin_y):
        """return block suitable block image"""
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(begin_x, begin_y, self.block_w, self.block_h)
        image.blit(self.image, (0, 0), self.rect)
        block = pg.transform.scale(image, (self.block_w, self.block_h))
        return block


class Platform(Object):
    def __init__(self, x, y, width, height, begin_x, begin_y):
        super().__init__(width, height)
        self.image = self.build(begin_x, begin_y)
        self.rect.topleft = (x, y)
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.surface.blit(self.image, (0, 0))
        self.mask = pg.mask.from_surface(self.surface)

    def draw(self, win, offset_x):
        """draw the blocks on the screen"""
        # pg.draw.rect(win, (255, 0, 0), self.rect)
        win.blit(self.surface, (self.rect.x - offset_x, self.rect.y))


TRAP_PATH = "gameasset/Traps/Fire/On (16x32).png"


class Trap(Object):
    def __init__(self, pos_x, pos_y):
        super().__init__(16, 32, path=TRAP_PATH, scale_x=20, scale_y=28)

        self.img = None
        self.all_sprites = [self.build(begin_x=i * 16, begin_y=0) for i in range(3)]
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.mask = pg.mask.from_surface(self.surface)
        self.rect.topleft = (pos_x, pos_y)
        self.animation_rate = 0

    def update(self):
        """made mask for collision"""
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.surface.blit(self.img, (0, 0))
        self.mask = pg.mask.from_surface(self.surface)

    def animate(self):
        self.animation_rate += 0.09
        if int(self.animation_rate) >= len(self.all_sprites) - 1:
            self.animation_rate = 0
        self.img = self.all_sprites[int(self.animation_rate)]
        self.update()

    def draw(self, screen, offset):
        self.animate()
        screen.blit(self.img, (self.rect.x - offset, self.rect.y))


fruit_path = "gameasset/Fruits/"
fruits = {
    "apple": [f"{fruit_path}Apple.png", 17],
    "cherries": [f"{fruit_path}Cherries.png", 17],
    "strawberry": [f"{fruit_path}Strawberry.png", 17],
    "melon": [f"{fruit_path}Melon.png", 17],
    "orange": [f"{fruit_path}Orange.png", 17],
    "kiwi": [f"{fruit_path}Kiwi.png", 17],
    "pineapple": [f"{fruit_path}Pineapple.png", 17],

}


class Collect(Object):
    def __init__(self):
        super().__init__(32, 32, path=f"{fruit_path}Collected.png", scale_x=32, scale_y=32)
        self.done = False
        self.img = None
        self.all_sprites = [self.build(begin_x=i * 32, begin_y=0) for i in range(6)]
        self.animation_rate = 0

    def animate(self):
        self.animation_rate += 0.20
        if int(self.animation_rate) >= len(self.all_sprites):
            self.animation_rate = 0
            self.done = True
        self.img = self.all_sprites[int(self.animation_rate)]

    def draw(self, screen, offset_x):
        self.animate()
        if not self.done:
            screen.blit(self.img, (self.rect.x - offset_x, self.rect.y))
        return self.done


class Fruits(Object):
    def __init__(self, pos_x, pos_y):
        self.position = None
        self.window = None
        fruit_list = ["apple", "strawberry", "cherries", "pineapple", "melon", "orange", "kiwi"]
        self.name = rd.choice(fruit_list)
        super().__init__(32, 32, path=fruits[self.name][0], scale_x=32, scale_y=32)
        self.img = None
        self.all_sprites = [self.build(begin_x=i * 32, begin_y=0) for i in range(fruits[self.name][1])]
        self.surface = pg.Surface((self.block_w, self.block_h), pg.SRCALPHA).convert_alpha()
        self.mask = pg.mask.from_surface(self.surface)
        self.rect.center = (pos_x, pos_y)
        self.animation_rate = 0

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
        self.window = screen
        self.position = (self.rect.x - offset, self.rect.y)
        self.animate()
        screen.blit(self.img, self.position)


