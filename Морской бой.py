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
end_game = (False, None)
splash = pygame.mixer.Sound(os.path.join('data', 'Всплеск.wav'))
breaking_through = pygame.mixer.Sound(os.path.join('data', 'Есть пробитие.mp3'))
win = pygame.mixer.Sound(os.path.join('data', 'Победа.mp3'))
pygame.mixer.music.load(os.path.join('data', 'Море.mp3'))
pygame.mixer.music.play()


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
blown_up_ships = [load_image('Взорванный_однопалубник.png'), load_image('Взорванный_двухпалубник.png'),
                  load_image('Взорванный_трехпалубник.png'), load_image('Взорванный_четырехпалубник.png')]
fon = pygame.transform.scale(load_image('Море.png'), (1110, 725))
screen.blit(fon, (0, 0))


class Board:
    def __init__(self, name, other_name, surface):
        self.width = 10
        self.height = 10
        self.board = [[0] * 10 for _ in range(10)]
        self.board_image = [[None, None, None, None, None] * 10 for _ in range(10)]
        self.left = 140
        self.top = 90
        self.cell_size = 60
        self.name = name
        self.other_name = other_name
        self.surface = surface
        self.ship_cell = [4 for _ in range(20)]

    def render(self):
        words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for i in range(self.width):
            for j in range(self.height):
                if self.board[i][j] != 2:
                    if self.board[i][j] == 3:
                        pygame.draw.rect(self.surface, pygame.Color('#A60000'),
                                         [(self.left + i * self.cell_size, self.top + j * self.cell_size),
                                          (self.cell_size, self.cell_size)], )
                    elif self.board[i][j] == 0 or self.board[i][j] == 1:
                        pygame.draw.rect(self.surface, pygame.Color('#F3B770'),
                                         [(self.left + i * self.cell_size + 2, self.top + j * self.cell_size + 2),
                                          (self.cell_size - 2, self.cell_size - 3)], )
                        pygame.draw.rect(self.surface, pygame.Color('#033F60'),
                                            [(self.left + i * self.cell_size, self.top + j * self.cell_size),
                                            (self.cell_size, self.cell_size)], 2)
                    if (self.board[i][j] == 1 and self != second_board_on_war and self != first_board_on_war) or\
                            self.board[i][j] == 4:
                        if self.board_image[i][j][1]:
                            source_area = pygame.Rect((60 * self.board_image[i][j][2], 0), (60, 60))
                        else:
                            source_area = pygame.Rect((0, self.board_image[i][j][2] * 60), (60, 60))
                        self.surface.blit(self.board_image[i][j][0],
                                          (self.left + i * self.cell_size, self.top + j * self.cell_size), source_area)

        text_coord = self.left + 20
        for word in words:
            string_rendered = font.render(word, True, pygame.Color('navy'))
            string_rect = string_rendered.get_rect()
            string_rect.x = text_coord
            text_coord += 60
            string_rect.y = 50
            self.surface.blit(string_rendered, string_rect)
        text_coord = self.top + 20
        for i in range(1, 11):
            number_rendered = font.render(str(i), True, pygame.Color('navy'))
            number_rect = number_rendered.get_rect()
            number_rect.y = text_coord
            text_coord += 60
            if self != second_board_on_war:
                number_rect.x = 125 - number_rect.width
            else:
                number_rect.x = 1475
            self.surface.blit(number_rendered, number_rect)
        name_rendered = font.render(self.name, True, pygame.Color('navy'))
        name_rect = name_rendered.get_rect()
        name_rect.x = self.left - 50
        name_rect.y = self.top - 80
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
                                        board.board_image[cell[0]][cell[1]] = [ship.image, side, position, coord_ship,
                                                                               self.check_neighbors(coord_ship)]
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
                                                                               side, position, coord_ship,
                                                                               self.check_neighbors(coord_ship)]
                                        position = position + 1
                                    break
                    else:
                        if self.update(self.check_neighbors([(first_button % 10, first_button // 10)]),
                                       [(first_button % 10, first_button // 10)], True):
                            self.board[first_button % 10][first_button // 10] = 1
                            board.board_image[first_button % 10][first_button // 10] = \
                                [ship.image, side, 0, [(first_button % 10, first_button // 10)],
                                 self.check_neighbors([(first_button % 10, first_button // 10)])]
                            break
        for ship in sprites:
            ship.count = 0

    def update(self, cells, ship_buttons, auto_or_not):
        if len(cells) == 1:
            print(cells)
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

    def fire(self, pos):
        global end_game
        pos_x_pressed = (pos[0] - self.left) // 60
        pos_y_pressed = (pos[1] - self.top) // 60
        if self.board[pos_x_pressed][pos_y_pressed] == 0:
            self.board[pos_x_pressed][pos_y_pressed] = 2
            splash.play()
            return (True, False)
        elif self.board[pos_x_pressed][pos_y_pressed] == 1:
            self.board[pos_x_pressed][pos_y_pressed] = 3
            breaking_through.play()
            self.ship_cell.pop()
            if not bool(self.ship_cell):
                end_game = (True, self.other_name)
                win.play()
            if [self.board[ship[0]][ship[1]] for ship in self.board_image[pos_x_pressed][pos_y_pressed][3]].count(3) ==\
                    len(self.board_image[pos_x_pressed][pos_y_pressed][3]):
                for ship in self.board_image[pos_x_pressed][pos_y_pressed][3]:
                    self.board[ship[0]][ship[1]] = 4
                for cell in self.board_image[pos_x_pressed][pos_y_pressed][4]:
                    if self.board[cell[0]][cell[1]] != 4:
                        self.board[cell[0]][cell[1]] = 2
            return (True, True)
        else:
            return (False, False)


class Button:
    def create_button(self, surface, x, y, length, height, text):
        self.remaining_ships = [ship.count for ship in ship_group.sprites()]
        if self.remaining_ships.count(0) != len(self.remaining_ships) and self == next_screen_button and not bool(second_board):
            surface = self.draw_button(surface, pygame.Color('gray28'), length, height, x, y)
        elif end_game[0]:
            surface = self.draw_button(surface, pygame.Color('#4A0134'), length, height, x, y)
        else:
            surface = self.draw_button(surface, pygame.Color('#EC9F3B'), length, height, x, y)
        surface = self.write_text(surface, text, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text,  length, height, x, y):
        font_size = int(length//len(text) * 1.5)
        button_font = pygame.font.SysFont("Calibri", font_size)
        button_text = button_font.render(text, True, pygame.Color('black'))
        surface.blit(button_text, ((x+length/2) - button_text.get_width()/2, (y+height/2) - button_text.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y):
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        if not end_game[0]:
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
                self.neighbors = board.check_neighbors(self.ship_button)
                self.ship_can_be_installed = board.update(self.neighbors,
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
                    board.board_image[i[0]][i[1]] = [self.image, self.sideways, position, self.ship_button, self.neighbors]
                    position = position + 1
            else:
                this_ship_is_on_the_right.count = this_ship_is_on_the_right.count + 1
            this_ship_is_on_the_right.next_ship = False
            self.kill()
        self.render()


auto_button = Button()
next_screen_button = Button()
exit_button = Button()
first_board_on_war = Board('Игрок1', 'Игрок2', screen)
second_board_on_war = Board('Игрок2', 'Игрок1', screen)
board = Board('Игрок1', 'Игрок2', screen)
first_board = []
second_board = []
start_screen = True
start_fon = pygame.transform.scale(load_image('Заставка.jpeg'), (1110, 725))
arrow = pygame.transform.scale(load_image('Стрелочка.png'), (100, 60))
first_player_goes = choice((True, False))
if first_player_goes:
    arrow = pygame.transform.flip(arrow, True, False)
for i in range(4):
    Ships(810, 360 - 90 * i, ship_image[i], 4 - i, screen, False)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            for sprite in ship_group.sprites():
                sprite.rotate()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not start_screen:
            if auto_button is not None and auto_button.pressed(event.pos):
                board.automatic_placement()
            elif event.pos[0] > 140 and event.pos[0] < 740 and event.pos[1] > 90 and event.pos[1] < 690 and\
                    (not bool(first_board) or not bool(second_board)):
                board.permution(event.pos)
            elif end_game[0] and exit_button.pressed(event.pos):
                running = False
            elif next_screen_button.pressed(event.pos) and \
                  (next_screen_button.remaining_ships.count(0) == len(next_screen_button.remaining_ships) or
                   bool(second_board) or end_game[0]):
                if not bool(first_board):
                    first_board = board.board
                    first_board_image = board.board_image
                    for i in range(10):
                        for j in range(10):
                            if first_board_image[i][j] is not None:
                                if first_board_image[i][j][1]:
                                    first_board_image[i][j][0] = blown_up_ships[len(first_board_image[i][j][3]) - 1]
                                else:
                                    first_board_image[i][j][0] = \
                                        pygame.transform.rotate(blown_up_ships[len(first_board_image[i][j][3]) - 1], 90)
                    board.name = 'Игрок2'
                elif not bool(second_board):
                    second_board = board.board
                    second_board_image = board.board_image
                    for i in range(10):
                        for j in range(10):
                            if second_board_image[i][j] is not None:
                                if second_board_image[i][j][1]:
                                    second_board_image[i][j][0] = blown_up_ships[len(second_board_image[i][j][3]) - 1]
                                else:
                                    second_board_image[i][j][0] = pygame.transform.rotate\
                                        (blown_up_ships[len(second_board_image[i][j][3]) - 1], 90)
                    second_board_on_war.board = second_board
                    second_board_on_war.board_image = second_board_image
                    first_board_on_war.board = first_board
                    first_board_on_war.board_image = first_board_image
                    screen = pygame.display.set_mode((1527, 801))
                    fon = pygame.transform.scale(load_image('Море.png'), (1527, 801))
                    second_board_on_war.left = 860
                    auto_button = None
                else:
                    first_board = []
                    second_board = []
                    screen = pygame.display.set_mode(size)
                    fon = pygame.transform.scale(load_image('Море.png'), (1110, 725))
                    ship_group = pygame.sprite.Group()
                    for i in range(4):
                        Ships(810, 360 - 90 * i, ship_image[i], 4 - i, screen, False)
                    board = Board('Игрок1', 'Игрок2', screen)
                    first_board_on_war = Board('Игрок1', 'Игрок2', screen)
                    second_board_on_war = Board('Игрок2', 'Игрок1', screen)
                    auto_button = Button()
                    end_game = (False, None)
                board.board = [[0] * 10 for _ in range(10)]
                board.board_image = [[None, None, None, None] * 10 for _ in range(10)]
                for sprite in ship_group.sprites():
                    sprite.count = (300 - sprite.rect.width) // 60
            elif bool(first_board) and bool(second_board):
                if first_player_goes and 140 < event.pos[0] < 740 and 90 < event.pos[1] < 690:
                    result = first_board_on_war.fire(event.pos)
                    if result[0] and not result[1]:
                        arrow = pygame.transform.flip(arrow, True, False)
                        first_player_goes = False
                if not first_player_goes and 860 < event.pos[0] < 1460 and 90 < event.pos[1] < 690:
                    result = second_board_on_war.fire(event.pos)
                    if result[0] and not result[1]:
                        arrow = pygame.transform.flip(arrow, True, False)
                        first_player_goes = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and start_screen:
            start_screen = False
        if end_game[0]:
            screen = pygame.display.set_mode(size)
            fon = pygame.transform.scale(load_image('win.jpg'), (1110, 725))
            font_size = int(300 // len(end_game[1]) * 1.5)
            button_font = pygame.font.SysFont("Calibri", font_size)
            text = button_font.render(end_game[1], True, pygame.Color(124, 46, 125))

    if start_screen:
        screen.blit(start_fon, (0, 0))
    else:
        screen.blit(fon, (0, 0))
        if not bool(first_board) or not bool(second_board):
            auto_button.create_button(screen, 810, 450, 281, 61, 'Авто расстановка')
            next_screen_button.create_button(screen, 960, 640, 141, 51, '--->')
            board.render()
            ship_group.update()
            ship_group.draw(screen)
        elif end_game[0]:
            screen.blit(text, (size[0] // 2 - 100, 100))
            exit_button.create_button(screen, 300, 550, 200, 60, 'Выход')
            next_screen_button.create_button(screen, 600, 550, 200, 60, 'Перезапуск')
        else:
            first_board_on_war.render()
            second_board_on_war.render()
            screen.blit(arrow, (750, 390))
            next_screen_button.create_button(screen, 1150, 700, 300, 60, 'Перезапуск')
    pygame.display.flip()
pygame.quit()