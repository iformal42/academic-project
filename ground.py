import pygame as pg

PATH = "gameasset/Terrain/Terrain (16x16).png"
SCALE_X, SCALE_Y = 42, 16


class Platform(pg.sprite.Sprite):
    def __init__(self, width: int, height: int, screen):
        super().__init__()

        self.width, self.height = 3 * width, 3 * height
        self.window = screen
        self.rect = pg.Rect(0, 0, self.width, self.height)
        # self.mask = pg.mask.from_surface(self.image)
        self.block_w, self.block_h = self.width + SCALE_X, self.height + SCALE_Y
        self.image = pg.image.load(PATH)


    def build(self, begin_y, begin_x):
        """return block suitable block image"""
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(begin_x, begin_y, self.block_w, self.block_h)
        image.blit(self.image, (0, 0), self.rect)
        block = pg.transform.scale(image, (self.block_w, self.block_h))
        self.rect = block.get_rect()
        return block
