import pygame as pg

PATH = "gameasset/Main Characters/Mask Dude/"


class Player(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.player = []
        self.character_img = pg.image.load(f"{PATH}Idle (32x32).png")

    def stand(self):
        pass


if __name__ == "__main__":
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()
    player = Player("yes")

    # window
    window = pg.display.set_mode((1200, 1000))

    running = True
    while running:
        # 60 FPS
        window.fill((135, 206, 235))
        window.blit(player.character_img, (0, 0))
        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False
        pg.display.update()
