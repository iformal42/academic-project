import pygame as pg

PATH = "gameasset/Terrain/Terrain (16x16).png"
SCALE_X, SCALE_Y = 42, 16


class Object(pg.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()

        self.width, self.height = width, height
        self.rect = pg.Rect(0, 0, self.width, self.height)
        # self.mask = pg.mask.from_surface(self.image)
        self.block_w, self.block_h = self.width + SCALE_X, self.height + SCALE_Y
        self.image = pg.image.load(PATH)

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
