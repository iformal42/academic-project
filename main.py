import pygame as pg
from player import Player

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1200, 1000
VELOCITY = 5


def action_handler(p):
        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            p.move(VELOCITY)
        if keys[pg.K_a]:
            p.move(-VELOCITY)


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    # adding player object
    player = Player(32, 32, window)
    running = True
    while running:
        # 60 FPS
        clock.tick(60)
        window.fill(SKY)
        # window.blit(player.stand(3, 2), (50, 500))
        player.animation_idle(9)
        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False

            action_handler(p=player)


        pg.display.update()


if __name__ == "__main__":
    main_game()
