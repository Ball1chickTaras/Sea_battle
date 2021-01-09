import pygame
import os
import sys
pygame.init()
size = (1110, 725)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Морской бой')
running = True
ship_group = pygame.sprite.Group()
font = pygame.font.Font(None, 40)


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
    def __init__(self, name, surface):
        self.width = 10
        self.height = 10
        self.board = [[0] * 10 for _ in range(10)]
        self.left = 140
        self.top = 90
        self.cell_size = 60
        self.name = name
        self.surface = surface

    def render(self):
        words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.surface, pygame.Color('#033F60'),
                                 [(self.left + i * self.cell_size, self.top + j * self.cell_size),
                                  (self.cell_size, self.cell_size)], 2)
                pygame.draw.rect(self.surface, pygame.Color('#F3B770'),
                                 [(self.left + i * self.cell_size + 2, self.top + j * self.cell_size + 2),
                                  (self.cell_size - 2, self.cell_size - 3)], )
        text_coord = 160
        for word in words:
            string_rendered = font.render(word, True, pygame.Color('navy'))
            string_rect = string_rendered.get_rect()
            string_rect.x = text_coord
            text_coord += 60
            string_rect.y = 50
            self.surface.blit(string_rendered, string_rect)
        text_coord = 110
        for i in range(1, 11):
            number_rendered = font.render(str(i), True, pygame.Color('navy'))
            number_rect = number_rendered.get_rect()
            number_rect.y = text_coord
            text_coord += 60
            number_rect.x = 125 - number_rect.width
            self.surface.blit(number_rendered, number_rect)
        name_rendered = font.render(self.name, True, pygame.Color('navy'))
        name_rect = name_rendered.get_rect()
        name_rect.x = 60
        name_rect.y = 10
        self.surface.blit(name_rendered, name_rect)


class Button:
    def create_button(self, surface, x, y, length, height, text):
        surface = self.draw_button(surface, pygame.Color('#EC9F3B'), length, height, x, y)
        surface = self.write_text(surface, text, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text,  length, height, x, y):
        font_size = int(length//len(text) * 1.5)
        button_font = pygame.font.SysFont("Calibri", font_size)
        button_text = button_font.render(text, True, pygame.Color('black'))
        surface.blit(button_text, ((x+length/2) - button_text.get_width()/2, (y+height/2) - button_text.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y):
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        pygame.draw.rect(surface, pygame.Color('MediumPurple4'), (x, y, length, height), 3)
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        print("Some button was pressed!")
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


class Ships(pygame.sprite.Sprite):
    def __init__(self, x, y, image, count, surface, next_ship):
        super().__init__(ship_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = count
        self.surface = surface
        self.next_ship = next_ship
        self.corner_x = 0
        self.corner_y = 0
        self.ship_move = False
        self.ship_not_installed = True
        self.new_ship = None

    def render(self):
        if not self.ship_move:
            count_rendered = font.render(str(self.count), True, pygame.Color('navy'))
            intro_rect = count_rendered.get_rect()
            intro_rect.y = self.rect.y + 30
            intro_rect.x = self.rect.x + self.rect.width + 10
            self.surface.blit(count_rendered, intro_rect)

    def update(self):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos) and self.count != 0\
                and not self.next_ship:
            self.count = self.count - 1
            self.new_ship = Ships(self.rect.x, self.rect.y, self.image, self.count, screen, True)
            self.next_ship = True
            self.corner_x = event.pos[0] - self.rect.x
            self.corner_y = event.pos[1] - self.rect.y
            self.ship_move = True
        if event.type == pygame.MOUSEMOTION and self.ship_move:
            self.rect.x = event.pos[0] - self.corner_x
            self.rect.y = event.pos[1] - self.corner_y
        if event.type == pygame.MOUSEBUTTONUP and self.ship_move:
            if self.ship_not_installed:
                self.new_ship.count = self.new_ship.count + 1
                self.new_ship.next_ship = False
                self.ship_move = False
                self.kill()
        self.render()


auto_button = Button()
next_screen_button = Button()
board = Board('Игрок1', screen)
for i in range(4):
    Ships(810, 360 - 90 * i, ship_image[i], 4 - i, screen, False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(fon, (0, 0))
    auto_button.create_button(screen, 810, 450, 281, 61, 'Авто расстановка')
    next_screen_button.create_button(screen, 960, 640, 141, 51, '--->')
    ship_group.update()
    board.render()
    ship_group.draw(screen)
    pygame.display.flip()
pygame.quit()