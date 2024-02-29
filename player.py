import pygame as pg

PATH = "gameasset/Main Characters/Mask Dude/"


class Player(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.player = []
        self.image = pg.Surface((width, height))

        self.character_img = pg.image.load(f"{PATH}Idle (32x32).png")
        self.rect1 = self.character_img.get_rect()

    def stand(self, width, height):
        image = pg.Surface((width, height))




if __name__ == "__main__":
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()
    player = Player(50,50)

    # window
    window = pg.display.set_mode((1200, 1000))

    running = True
    while running:
        # 60 FPS
        window.fill((135, 206, 235))
        window.blit(player.image,(0,0))

        # pg.draw.rect(window, (255, 0, 0), player.rect1)
        # window.blit(player.character_img, (0, 0))

        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False
        pg.display.update()
