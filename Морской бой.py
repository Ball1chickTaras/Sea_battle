import pygame
import os
from random import randint, choice
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
        self.board_image = [[None, None, None, None] * 10 for _ in range(10)]
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
                if self.board[i][j] == 1:
                    if self.board_image[i][j][1]:
                        source_area = pygame.Rect((60 * self.board_image[i][j][2], 0), (60, 60))
                    else:
                        source_area = pygame.Rect((0, self.board_image[i][j][2] * 60), (60, 60))
                    self.surface.blit(self.board_image[i][j][0],
                                      (self.left + i * self.cell_size, self.top + j * self.cell_size), source_area)
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

    def check_neighbors(self, ship_button):
        neighbors = set()
        for cell in ship_button:
            if cell[0] > 0:
                if cell[1] > 0:
                    neighbors.add((cell[0] - 1, cell[1] - 1))
                neighbors.add((cell[0] - 1, cell[1]))
                if cell[1] < 9:
                    neighbors.add((cell[0] - 1, cell[1] + 1))
            if cell[1] > 0:
                neighbors.add((cell[0], cell[1] - 1))
            if cell[1] < 9:
                neighbors.add((cell[0], cell[1] + 1))
            if cell[0] < 9:
                if cell[1] > 0:
                    neighbors.add((cell[0] + 1, cell[1] - 1))
                neighbors.add((cell[0] + 1, cell[1]))
                if cell[1] < 9:
                    neighbors.add((cell[0] + 1, cell[1] + 1))
            neighbors.add((cell[0], cell[1]))
        return list(neighbors)

    def automatic_placement(self):
        sprites = ship_group.sprites()
        sprites.reverse()
        self.board = [[0] * 10 for _ in range(10)]
        for ship in sprites:
            for j in range((300 - ship.rect.width) // 60):
                while True:
                    side = choice((True, False))
                    first_button = randint(0, 99)
                    if (300 - ship.rect.width) // 60 != 4:
                        if side:
                            if first_button % 10 + ship.rect.width // 60 < 10:
                                coord_ship = [(first_button % 10 + i, first_button // 10) for i in range(ship.rect.width // 60)]
                                if self.update(self.check_neighbors(coord_ship), coord_ship, True):
                                    position = 0
                                    for cell in coord_ship:
                                        self.board[cell[0]][cell[1]] = 1
                                        board.board_image[cell[0]][cell[1]] = [ship.image, side, position, coord_ship]
                                        position = position + 1
                                    break
                        else:
                            if first_button // 10 + ship.rect.width // 60 < 10:
                                coord_ship = [(first_button % 10, first_button // 10 + i) for i in range(ship.rect.width // 60)]
                                if self.update(self.check_neighbors(coord_ship), coord_ship, True):
                                    position = 0
                                    for cell in coord_ship:
                                        self.board[cell[0]][cell[1]] = 1
                                        board.board_image[cell[0]][cell[1]] = [pygame.transform.rotate(ship.image, 90),
                                                                               side, position, coord_ship]
                                        position = position + 1
                                    break
                    else:
                        if self.update(self.check_neighbors([(first_button % 10, first_button // 10)]),
                                       [(first_button % 10, first_button // 10)], True):
                            self.board[first_button % 10][first_button // 10] = 1
                            board.board_image[first_button % 10][first_button // 10] = \
                                [ship.image, side, 0, [(first_button % 10, first_button // 10)]]
                            break
        for ship in sprites:
            ship.count = 0

    def update(self, cells, ship_buttons, auto_or_not):
        ship_can_be_installed = True
        color = pygame.Color('green4')
        for checking in cells:
            if self.board[checking[0]][checking[1]] != 0:
                color = pygame.Color('red3')
                ship_can_be_installed = False
                break
        if not auto_or_not:
            for cell in cells:
                if cell not in ship_buttons and self.board[cell[0]][cell[1]] == 0:
                    pygame.draw.rect(self.surface, color,
                                     [(self.left + cell[0] * self.cell_size + 2, self.top + cell[1] * self.cell_size + 2),
                                      (self.cell_size - 2, self.cell_size - 3)], )
        return ship_can_be_installed

    def permution(self, pos):
        pos_x_pressed = (pos[0] - 140) // 60
        pos_y_pressed = (pos[1] - 90) // 60
        if self.board[pos_x_pressed][pos_y_pressed] == 1:
            pos_x_first = self.board_image[pos_x_pressed][pos_y_pressed][3][0][0] * 60 + 140
            pos_y_first = self.board_image[pos_x_pressed][pos_y_pressed][3][0][1] * 60 + 90
            rearranged = Ships(pos_x_first, pos_y_first, self.board_image[pos_x_pressed][pos_y_pressed][0], 0, screen, False)
            rearranged.ship_move = True
            rearranged.corner_x = pos[0] - pos_x_first
            rearranged.corner_y = pos[1] - pos_y_first
            rearranged.sideways = self.board_image[pos_x_pressed][pos_y_pressed][1]
            rearranged.ship_can_be_installed = True
            rearranged.ship_button = self.board_image[pos_x_pressed][pos_y_pressed][3]
            for cell in self.board_image[pos_x_pressed][pos_y_pressed][3]:
                self.board[cell[0]][cell[1]] = 0


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
        if self.rect.collidepoint(mouse[0], mouse[1]):
            return True
        else:
            return False


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
        self.ship_can_be_installed = False
        self.new_ship = None
        self.sideways = True

    def render(self):
        if not self.ship_move:
            count_rendered = font.render(str(self.count), True, pygame.Color('navy'))
            intro_rect = count_rendered.get_rect()
            intro_rect.y = self.rect.y + 30
            intro_rect.x = self.rect.x + self.rect.width + 10
            self.surface.blit(count_rendered, intro_rect)

    def rotate(self):
        if self.ship_move:
            if self.sideways:
                self.sideways = False
                self.image = pygame.transform.rotate(self.image, 90)
            else:
                self.sideways = True
                self.image = pygame.transform.rotate(self.image, -90)
            self.rect = self.image.get_rect()
            self.corner_x, self.corner_y = self.corner_y, self.corner_x
            self.rect.x = self.event_pos_x - self.corner_x
            self.rect.y = self.event_pos_y - self.corner_y

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
            self.ship_can_be_installed = False
            self.event_pos_x = event.pos[0]
            self.event_pos_y = event.pos[1]
            self.ship_button = []
            self.neighbors = set()
            self.rect.x = event.pos[0] - self.corner_x
            self.rect.y = event.pos[1] - self.corner_y
            if self.rect.x > 80 and self.rect.x + self.rect.width < 800 \
                    and self.rect.y > 30 and self.rect.y + self.rect.height < 750:
                if self.rect.y < 90:
                    if self.sideways:
                        if self.rect.x > 140:
                            for i in range(self.rect.width // 60):
                                self.ship_button.append(((self.rect.x - 140) // 60 + i, 0))
                        else:
                            for i in range(self.rect.width // 60):
                                self.ship_button.append((i, 0))
                    else:
                        if self.rect.x > 140:
                            for i in range(self.rect.height // 60):
                                self.ship_button.append(((self.rect.x - 140) // 60, i))
                        else:
                            for i in range(self.rect.height // 60):
                                self.ship_button.append((0, i))
                else:
                    if self.sideways:
                        if self.rect.x > 140:
                            for i in range(self.rect.width // 60):
                                self.ship_button.append(((self.rect.x - 140) // 60 + i,
                                                         (self.rect.y - 90) // 60))
                        else:
                            for i in range(self.rect.width // 60):
                                self.ship_button.append((i, (self.rect.y - 90) // 60))
                    else:
                        if self.rect.x > 140:
                            for i in range(self.rect.height // 60):
                                self.ship_button.append(((self.rect.x - 140) // 60,
                                                         (self.rect.y - 90) // 60 + i))
                        else:
                            for i in range(self.rect.height // 60):
                                self.ship_button.append((0, (self.rect.y - 90) // 60 + i))
                self.ship_can_be_installed = board.update(board.check_neighbors(self.ship_button),
                                                          self.ship_button, False)
        if event.type == pygame.MOUSEBUTTONUP and self.ship_move:
            position = 0
            for sprite in ship_group.sprites():
                if self.sideways:
                    if sprite.rect.width == self.rect.width and sprite != self:
                        this_ship_is_on_the_right = sprite
                else:
                    if sprite.rect.width == self.rect.height and sprite != self:
                        this_ship_is_on_the_right = sprite
            if self.ship_can_be_installed:
                for i in self.ship_button:
                    board.board[i[0]][i[1]] = 1
                    board.board_image[i[0]][i[1]] = [self.image, self.sideways, position, self.ship_button]
                    position = position + 1
            else:
                this_ship_is_on_the_right.count = this_ship_is_on_the_right.count + 1
            this_ship_is_on_the_right.next_ship = False
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
        if event.type == pygame.KEYDOWN:
            for sprite in ship_group.sprites():
                sprite.rotate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if auto_button.pressed(event.pos):
                board.automatic_placement()
            elif event.pos[0] > 140 and event.pos[0] < 740 and event.pos[1] > 90 and event.pos[1] < 690:
                board.permution(event.pos)
    screen.blit(fon, (0, 0))
    auto_button.create_button(screen, 810, 450, 281, 61, 'Авто расстановка')
    next_screen_button.create_button(screen, 960, 640, 141, 51, '--->')
    board.render()
    ship_group.update()
    ship_group.draw(screen)
    pygame.display.flip()
pygame.quit()