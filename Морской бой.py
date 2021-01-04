import pygame
import os
import sys
size = (1110, 725)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
running = True
ship_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


ship_image = [load_image('Однопалубный.png'), load_image('Двухпалубный.png'),
              load_image('Трехпалубный.png'), load_image('Четырехпалубный.png')]
fon = pygame.transform.scale(load_image('Море.png'), (1110, 725))
screen.blit(fon, (0, 0))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 60

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, pygame.Color('#033F60'),
                                 [(self.left + i * self.cell_size, self.top + j * self.cell_size),\
                                  (self.cell_size, self.cell_size)], 2)
                pygame.draw.rect(screen, pygame.Color('#F3B770'),
                                 [(self.left + i * self.cell_size + 2, self.top + j * self.cell_size + 2),\
                                  (self.cell_size - 2, self.cell_size - 3)], )


class Ships(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(ship_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


board = Board(10, 10)
board.set_view(140, 90, 60)
for i in range(4):
    Ships(810, 360 - 90 * i, ship_image[i])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    ship_group.draw(screen)
    board.render()
    pygame.display.flip()
pygame.quit()