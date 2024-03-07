import pygame as pg

PATH = "gameasset/Terrain/Terrain (16x16).png"


class Platform(pg.sprite.Sprite):
    def __init__(self, width, height, screen):
        super().__init__()
        self.mask = None
        self.width, self.height = width, height
        self.window = screen
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.block = self.build(pg.image.load(PATH))

    def build(self, img):
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(96, 0, self.width, self.height)
        image.blit(img, (0, 0), self.rect)
        return pg.transform.scale2x(image)
