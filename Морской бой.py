import pygame
import os
import sys
size = (1110, 725)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
running = True


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



board = Board(10, 10)
board.set_view(140, 90, 60)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    board.render()
    pygame.display.flip()
pygame.quit()