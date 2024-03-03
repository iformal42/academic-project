import pygame as pg

PATH = "gameasset/Main Characters/Mask Dude/"
JUMP = "Double Jump (32x32).png"
IDLE = "Idle (32x32).png"
RUN = "Run (32x32).png"


class Player(pg.sprite.Sprite):
    def __init__(self, width, height, screen):
        super().__init__()
        self.x_vel, self.y_vel = 0, 0
        self.width, self.height = width, height
        self.window = screen
        self.direction = "right"
        self.character_img = pg.image.load(f"{PATH}{IDLE}")
        self.rect = pg.Rect(0, 0, self.width, self.height)
        self.player_list = []
        self.animation()
        self.animation_rate = 0

    def stand(self, frame):
        image = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()
        self.rect = pg.Rect(frame * self.width, 0, self.width, self.height)
        image.blit(self.character_img, (0, 0), self.rect)
        return pg.transform.scale2x(image)

    def animation(self):
        for x in range(12):
            self.player_list.append(self.stand(x))

    def animation_idle(self, position):
        self.animation_rate += 0.20
        if int(self.animation_rate) >= 11:
            self.animation_rate = 0
        self.window.blit(self.player_list[int(self.animation_rate)], (self.rect.x, self.rect.y))

    def move(self, horizontal_vel):
        self.rect.move_ip(horizontal_vel, self.y_vel)


if __name__ == "__main__":
    # initialize the pygame
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((1200, 1000))

    player = Player(32, 32, window)
    sprite = pg.sprite.Group()
    # print(player)
    # print(sprite)
    # sprite.add(player)
    running = True
    while running:
        # 60 FPS
        clock.tick(60)

        window.fill((135, 206, 235))

        player.animation_idle(9)
        # sprite.draw(window)
        for event in pg.event.get():
            # stop condition
            if event.type is pg.QUIT:
                running = False

            keys = pg.key.get_pressed()
            if keys[pg.K_RIGHT]:
                print("yes")
                player.move()

        pg.display.update()
