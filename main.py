import random
import sys

import pygame

pygame.font.init()
pygame.init()


class Random_field:  # класс, который создаёт в начале игры значение полей
    def __init__(self):
        self.velue_list_H = [0] * 10  # список с значениями по горизонтале
        self.velue_list_V = [0] * 10  # список с значениями по вертикале
        self.board_start = list()
        for i in range(10):
            line_in_board = list()
            for j in range(10):
                n = random.randint(0, 1)
                line_in_board.append(n)
                if n == 1:
                    self.velue_list_V[j] += 1
                    self.velue_list_H[i] += 1
            self.board_start.append(line_in_board)  # матрица

    def displey_field(self):  # возврат параметров: матрицы и занчений
        return self.board_start, self.velue_list_V, self.velue_list_H


class Board:  # базовый класс поля
    def __init__(self, width=10, height=10, left=55, top=55, cell_size=50):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]  # матрица
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def ren(self, screen, board_main):  # создание квадратов
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 2)

    def get_cell_pos(self, mouse_pos):  # получение позиции нажатия и возврат положения клетки
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):  # переписать в наследниках классах
        pass

    def get_click(self, mouse_pos):  # нажатие на поле
        cell = self.get_cell_pos(mouse_pos)
        if cell:
            self.on_click(cell)


class My_game(Board):  # класс сложного уровня игры
    def __init__(self, width=10, height=10, left=55, top=55, cell_size=50):
        super().__init__(width, height, left, top, cell_size)
        self.count_mistakes_red = 0  # счётчик ошибок

    def on_click(self, cell):  # при нажатии на клетку она получает значение
        self.board[cell[1]][cell[0]] = 1

    def ren(self, screen, board_main):  # обновление поля, передаётся задуманное поле
        self.count_mistakes_red = 0
        self.board_main = board_main

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:  # если значения нашего поля == 1
                    if self.board_main[y][x] == 1:  # и задуманного == 1
                        pygame.draw.rect(screen, pygame.Color((31, 117, 254)), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))  # голубым закрашивается
                    elif not self.board_main[y][x]:  # если ошибка
                        pygame.draw.rect(screen, pygame.Color('red'), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))  # красным закрашивается

                        self.count_mistakes_red += 1  # и прибавляется ошибка

                pygame.draw.rect(screen, pygame.Color(0, 0, 0), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 2)  # обводка квадратов

    def display_mistakes_n(self):  # возврат количества ошибок
        return self.count_mistakes_red


class My_game_easy(My_game):  # лёгкий уровень
    def __init__(self, width=10, height=10, left=55, top=55, cell_size=50):
        super().__init__(width, height, left, top, cell_size)
        self.count_mistakes_red = 0  # счётчик ошибок
        self.list_velue_start = list()  # список значений, которые будут закрашены изначально
        for i in range(20):
            # рандомный выбор значений
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.board[x][y] = 1
            self.list_velue_start.append((x, y))

    def ren(self, screen, board_main):
        self.count_mistakes_red = 0
        self.board_main = board_main
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:  # если значения нашего поля == 1
                    if self.board_main[y][x] == 1:  # и задуманного == 1
                        pygame.draw.rect(screen, pygame.Color((31, 117, 254)), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))  # голубым закрашивается
                    elif not self.board_main[y][x]:  # если ошибка
                        pygame.draw.rect(screen, pygame.Color('red'), (
                            x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                            self.cell_size))  # красным закрашивается

                        if (y, x) not in self.list_velue_start:
                            self.count_mistakes_red += 1  # и прибавляется ошибка

                pygame.draw.rect(screen, pygame.Color(0, 0, 0), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size),
                                 2)  # обводка квадратов


def start_screen(screen):  # начало игры - заставка
    name = 'Введите имя'
    while True:
        fon = pygame.image.load('fon_start.jpg')  # фон начала
        screen.blit(pygame.transform.scale(fon, (900, 700)), (0, 0))

        font = pygame.font.Font(None, 100)  # шрифт названия
        font1 = pygame.font.Font(None, 50)  # шрифт другого текста
        # текст на заставке
        t1 = font.render('Головоломка', True, (0, 191, 255))
        t2 = font.render('с', True, (0, 191, 255))
        t3 = font.render('клеточками', True, (0, 191, 255))
        t4 = font1.render('Новая игра', True, (0, 0, 0))
        t5 = font1.render('enter - сложный уровень', True, (127, 255, 212))  # для перехода на сложный уровень
        t6 = font1.render('ctrl + f - лёгкий уровень', True, (127, 255, 212))  # для перехода на лёгкий уровень
        # расчёт расположения всего текста
        t1_pos = t1.get_rect()
        t1_pos.center = screen.get_rect().center
        t2_pos = t2.get_rect()
        t2_pos.center = screen.get_rect().center
        t3_pos = t3.get_rect()
        t3_pos.center = screen.get_rect().center
        t4_pos = t4.get_rect()
        t4_pos.center = screen.get_rect().center
        t5_pos = t5.get_rect()
        t5_pos.center = screen.get_rect().center
        t6_pos = t6.get_rect()
        t6_pos.center = screen.get_rect().center
        # размещение текстов на экране
        screen.blit(t1, (t1_pos[0], 80))
        screen.blit(t2, (t2_pos[0], 160))
        screen.blit(t3, (t3_pos[0], 240))
        screen.blit(t4, (t4_pos[0], 350))
        screen.blit(t5, (t5_pos[0], 400))
        screen.blit(t6, (t6_pos[0], 450))
        # обновление экрана
        pygame.display.update()

        flag = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # если нажать на крестик
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # события с клавиатуры
                    keys = pygame.key.get_pressed()  # для двойных нажатий
                    if event.key == pygame.K_RETURN:  # если нажать enter, то сложный уровень
                        if len(name) >= 1:
                            return [True, name]
                    elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                        pygame.quit()
                        sys.exit()
                    elif keys[pygame.K_LCTRL] and keys[pygame.K_f]:  # если нажать ctrl + f, то лёгкий уровень
                        if len(name) >= 1:
                            return [False, name]
                    # ввод имени игрока(при нажатии на буквы - пишется текст, или удаляется при K_BACKSPACE)
                    elif event.unicode.isalpha():
                        if name == 'Введите имя':
                            name = event.unicode
                        else:
                            name += event.unicode
                        flag = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                        flag = True
                        break
            if flag:
                break
            # отображение имени на экране
            t7 = font1.render(name, True, (0, 0, 0))
            t7_pos = t7.get_rect()
            t7_pos.center = screen.get_rect().center
            screen.blit(t7, (t7_pos[0], 550))
            pygame.display.update()


def finish_screen_loss(screen, time, error, name):  # проигрыш - заставка
    fon = pygame.image.load('fon_finish.jpg')  # загрузка фона проигрыша
    screen.blit(pygame.transform.scale(fon, (900, 700)), (0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (50, 50, 800, 350), 0)  # прямоугольник с текстом
    font2 = pygame.font.Font(None, 50)  # шрифт
    # текст при проигрыше
    t1 = font2.render(f'{name}, Вы проиграли!', True, (0, 0, 0))
    t2 = font2.render(f'Времени осталось: {time}', True, (0, 0, 0))
    t3 = font2.render(f'Ошибок: {error}', True, (0, 0, 0))
    # расчёт расположения всего текста
    t1_pos = t1.get_rect()
    t1_pos.center = screen.get_rect().center
    t2_pos = t2.get_rect()
    t2_pos.center = screen.get_rect().center
    t3_pos = t3.get_rect()
    t3_pos.center = screen.get_rect().center
    # размещение текстов на экране
    screen.blit(t1, (t1_pos[0], 100))
    screen.blit(t2, (t2_pos[0], 200))
    screen.blit(t3, (t3_pos[0], 300))

    # обновление экрана
    pygame.display.update()

    flag3 = True
    while flag3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажать на крестик
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # события с клавиатуры
                keys = pygame.key.get_pressed()  # для двойных нажатий
                if event.key == pygame.K_RETURN:  # если нажать enter, то переход на стартовый экран
                    flag3 = False
                    main()
                elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                    pygame.quit()
                    sys.exit()


def finish_screen_win(screen, time, error, name):  # победа - заставка
    fon = pygame.image.load('fon_finish_win.jpg')  # загрузка фона победы
    screen.blit(pygame.transform.scale(fon, (900, 700)), (0, 0))
    pygame.draw.rect(screen, (92, 20, 97), (50, 50, 800, 350), 0)  # прямоугольник с текстом
    font2 = pygame.font.Font(None, 70)  # шрифт
    # текст при победе
    t1 = font2.render(f'{name}, Вы выиграли!', True, (0, 191, 255))
    t2 = font2.render(f'Времени осталось: {time}', True, (0, 127, 255))
    t3 = font2.render(f'Ошибок: {error}', True, (66, 170, 255))
    # расчёт расположения всего текста
    t1_pos = t1.get_rect()
    t1_pos.center = screen.get_rect().center
    t2_pos = t2.get_rect()
    t2_pos.center = screen.get_rect().center
    t3_pos = t3.get_rect()
    t3_pos.center = screen.get_rect().center
    # размещение текстов на экране
    screen.blit(t1, (t1_pos[0], 100))
    screen.blit(t2, (t2_pos[0], 200))
    screen.blit(t3, (t3_pos[0], 300))
    # обновление экрана
    pygame.display.update()

    flag4 = True
    while flag4:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажать на крестик
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # события с клавиатуры
                keys = pygame.key.get_pressed()  # для двойных нажатий
                if event.key == pygame.K_RETURN:  # если нажать enter, то переход на стартовый экран
                    flag4 = False
                    main()
                elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                    pygame.quit()
                    sys.exit()


def pause(screen, time, error):  # пауза - заставка
    flag6 = True
    while flag6:
        fon = pygame.image.load('fon_pause.jpg')  # загрузка фона паузы
        screen.blit(pygame.transform.scale(fon, (900, 700)), (0, 0))  # прямоугольник с текстом
        pygame.draw.rect(screen, (204, 58, 214), (150, 50, 600, 350), 0)
        font5 = pygame.font.Font(None, 60)  # шрифт
        # текст при паузе
        t1 = font5.render('Пауза', True, (0, 0, 0))
        t2 = font5.render(f'Времени осталось: {time}', True, (0, 0, 0))
        t3 = font5.render(f'Ошибок: {error}', True, (0, 0, 0))
        # расчёт расположения всего текста
        t1_pos = t1.get_rect()
        t1_pos.center = screen.get_rect().center
        t2_pos = t2.get_rect()
        t2_pos.center = screen.get_rect().center
        t3_pos = t3.get_rect()
        t3_pos.center = screen.get_rect().center
        # размещение текстов на экране
        screen.blit(t1, (t1_pos[0], 100))
        screen.blit(t2, (t2_pos[0], 200))
        screen.blit(t3, (t3_pos[0], 300))
        # обновление экрана
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажать на крестик
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # события с клавиатуры
                keys = pygame.key.get_pressed()  # для двойных нажатий
                if event.key == pygame.K_RETURN:  # если нажать enter, то игра продолжится
                    flag6 = False
                elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                    pygame.quit()
                    sys.exit()
    # обновление экрана
    pygame.display.update()


def confirmation_field(screen, cause):  # окно подтверждения
    fon = pygame.image.load('fon_confirmation.jpg')  # загрузка фона подтверждающего окна
    screen.blit(pygame.transform.scale(fon, (900, 700)), (0, 0))  # прямоугольник с текстом
    pygame.draw.rect(screen, (179, 222, 255), (150, 50, 600, 450), 0)
    font5 = pygame.font.Font(None, 50)  # шрифт
    # текст при подтверждении
    t1 = font5.render('Вы уверены,', True, (0, 0, 0))
    if cause == 'проверка':
        t_cause = font5.render('что хотите проверить?', True, (0, 0, 0))
    else:
        t_cause = font5.render('что хотите завершить?', True, (0, 0, 0))
    t2 = font5.render('"ДА" - ctrl + y', True, (0, 0, 0))
    t3 = font5.render('"НЕТ" - ctrl + n', True, (0, 0, 0))
    # расчёт расположения всего текста
    t1_pos = t1.get_rect()
    t1_pos.center = screen.get_rect().center
    t_cause_pos = t_cause.get_rect()
    t_cause_pos.center = screen.get_rect().center
    t2_pos = t2.get_rect()
    t2_pos.center = screen.get_rect().center
    t3_pos = t3.get_rect()
    t3_pos.center = screen.get_rect().center
    # размещение текстов на экране
    screen.blit(t1, (t1_pos[0], 100))
    screen.blit(t_cause, (t_cause_pos[0], 200))
    screen.blit(t2, (t2_pos[0], 300))
    screen.blit(t3, (t3_pos[0], 400))
    # обновление экрана
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажать на крестик
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # события с клавиатуры
                keys = pygame.key.get_pressed()  # для двойных нажатий
                if keys[pygame.K_LCTRL] and keys[pygame.K_y]:  # если да
                    return True
                elif keys[pygame.K_LCTRL] and keys[pygame.K_n]:  # если нет
                    return False
                elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                    pygame.quit()
                    sys.exit()


def main():
    size = width, height = 900, 700
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Головоломка с клеточками')

    game_level = start_screen(screen)  # начальная заставка
    name = game_level[1]  # имя игрока

    new_game = Random_field()  # создание поля для игры
    new_game1 = new_game.displey_field()  # матрица и значения
    board_main = new_game1[0]  # сама матрица для игры
    velue_V = new_game1[1]  # значения по вертикале
    velue_H = new_game1[2]  # значения по горизонтале
    sum_velue = sum(velue_V)  # всего голубых квадратиков

    if game_level[0]:  # сложная
        board = My_game()
    elif not game_level[0]:  # простая
        board = My_game_easy()
    print(board_main)  # вывод матрицы в консоле
    # для таймера
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    count_seconds = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # если нажать на крестик
                running = False

            if event.type == MYEVENTTYPE:  # таймер
                count_seconds += 1
                if count_seconds == 1200:  # если время закончилось
                    finish_screen_loss(screen, f'0:00', str(board.display_mistakes_n()), name)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # при нажатии на экран
                board.get_click(event.pos)  # передача параметров положения клика
                pygame.display.update()

                if board.display_mistakes_n() >= 19:  # проверка количества ошибок
                    finish_screen_loss(screen, f'{(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}', '20',
                                       name)

            if event.type == pygame.KEYDOWN:  # события с клавиатуры
                keys = pygame.key.get_pressed()  # для двойных нажатий
                if event.key == pygame.K_RETURN:  # если нажать enter, то игра проверит твоё поле, если правильно, то выведет заставку победы
                    confirmation = confirmation_field(screen, 'проверка')
                    if confirmation:  # если подтвердил
                        rounds = 0
                        board.ren(screen, board_main)
                        for i in range(10):
                            for j in range(10):
                                color = screen.get_at((j * 50 + 70, i * 50 + 70))  # получение цвета в клетке
                                print(color)
                                if color == (31, 117, 254, 255) and board_main[i][j] == 1:
                                    rounds += 1
                        if sum_velue == rounds:  # если голубых клеток сколько и должно быть, то победа
                            finish_screen_win(screen, f'{(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}',
                                              str(board.display_mistakes_n()), name)
                        else:  # если меньше голубых клеток
                            finish_screen_loss(screen, f'{(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}',
                                               str(board.display_mistakes_n()), name)

                elif keys[pygame.K_LCTRL] and keys[pygame.K_a]:  # закрытие
                    running = False

                elif keys[pygame.K_LCTRL] and keys[pygame.K_s]:  # досрочное завершение
                    confirmation = confirmation_field(screen, 'досрочное завершение')
                    board.ren(screen, board_main)
                    if confirmation:
                        finish_screen_loss(screen, f'{(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}',
                                           str(board.display_mistakes_n()), name)

                elif keys[pygame.K_LCTRL] and keys[pygame.K_z]:  # пауза
                    pause(screen, f'{(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}',
                          str(board.display_mistakes_n()))

        screen.fill((252, 116, 253))
        font = pygame.font.Font(None, 40)  # шрифт 1
        font2 = pygame.font.Font(None, 30)  # шрифт 2

        text2 = font.render(f"Ошибок: {board.display_mistakes_n()}", True, (0, 0, 0))  # количество ошибок
        text1 = font.render(f"Осталось: {(1200 - count_seconds) // 60}:{(1200 - count_seconds) % 60}", True,
                            (0, 0, 0))  # таймер
        # текст правил
        text_rules1 = font2.render("Красная клетка - ошибка.", True, (0, 0, 0))
        text_rules2 = font2.render("Голубая клетка - ошибка.", True, (0, 0, 0))
        text_rules3 = font2.render("Можно допустить", True, (0, 0, 0))
        text_rules4 = font2.render("20 ошибок.", True, (0, 0, 0))
        text_rules5 = font2.render("На прохождение", True, (0, 0, 0))
        text_rules6 = font2.render("уровня даётся", True, (0, 0, 0))
        text_rules7 = font2.render("20 минут.", True, (0, 0, 0))
        text_rules8 = font2.render("Завершить - ctrl + s", True, (0, 0, 0))
        text_rules9 = font2.render("Пауза - ctrl + z", True, (0, 0, 0))
        text_rules10 = font2.render("Выход - ctrl + a", True, (0, 0, 0))
        text_rules11 = font2.render("Проверить - enter", True, (0, 0, 0))
        text_rules12 = font2.render("Удачи!", True, (255, 255, 255))
        text_rules13 = font2.render("Победы!", True, (255, 255, 255))

        text_x = 50
        text_y = 580
        # размещение счётчиков
        screen.blit(text1, (text_x, text_y))
        screen.blit(text2, (text_x, text_y + 60))
        # размещение текстов на экране
        screen.blit(text_rules1, (610, 55 + 40))
        screen.blit(text_rules2, (610, 55 + 40 * 2))
        screen.blit(text_rules3, (610, 55 + 40 * 3))
        screen.blit(text_rules4, (610, 55 + 40 * 4))
        screen.blit(text_rules5, (610, 55 + 40 * 5))
        screen.blit(text_rules6, (610, 55 + 40 * 6))
        screen.blit(text_rules7, (610, 55 + 40 * 7))
        screen.blit(text_rules8, (610, 55 + 40 * 8))
        screen.blit(text_rules9, (610, 55 + 40 * 9))
        screen.blit(text_rules10, (610, 55 + 40 * 10))
        screen.blit(text_rules11, (610, 55 + 40 * 11))
        screen.blit(text_rules12, (610, 55 + 40 * 12))
        screen.blit(text_rules13, (610, 55 + 40 * 13))
        # размещение значений
        for i in range(10):
            numbers_pos = 50
            numbers_H = font.render(str(velue_H[i]), True, (255, 255, 255))
            numbers_V = font.render(str(velue_V[i]), True, (255, 255, 255))
            screen.blit(numbers_V, (numbers_pos * i + 70, 20))
            screen.blit(numbers_H, (20, numbers_pos * i + 70))

        board.ren(screen, board_main)
        pygame.display.flip()
    pygame.quit()


main()
