import pygame as pg

# initializing constants
FPS = 60
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1200, 1000


def main_game():
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((WIDTH, HEIGHT))

    running = True
    while running:
        # 60 FPS
        window.fill(SKY)
        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False
        pg.display.update()


if __name__ == "__main__":
    main_game()
