import pygame
from pygame.draw import *
from random import randint
pygame.init()

# Базовые параметры
(FPS, score, tick_count, balls, squares, players) = (60, 0, 0, [], [], [0 for i in range(10)])

# Границы, от которых отскакивают шарики
borders = [0, 1200, 0, 700]

# Параметры экрана
screen = pygame.display.set_mode((1200, 700))

# Цвета
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def r_players():
    input = open('best_players_tech', 'r')
    r = input.readlines()
    for i in range(10):
        r[i] = r[i].rstrip()
        players[i] = int(r[i])


def new_ball():
    """
    Функция создаёт на экране новый шарик с заданными параметрами и добавляет параметры в текущий список шариков
    :return:
    """
    x = randint(100, 1100)
    y = randint(100, 600)
    r = randint(30, 50)
    dx = randint(-5, 5)
    dy = randint(-5, 5)
    color = COLORS[randint(0, 5)]
    balls.append([x, y, r, color, dx, dy])
    circle(screen, color, (x, y), r)


def ball_movement():
    """
    Функция производит перемещение шариков за один тик
    :return:
    """
    for i in range(len(balls)):
        # Считывание параемтров шарика
        dx = balls[i][4]
        dy = balls[i][5]
        r = balls[i][2]
        color = balls[i][3]
        # Отскоки
        if borders[1] - r >= balls[i][0] + dx >= r + borders[0]:
            x = balls[i][0] + dx
        else:
            dx = -dx
            x = balls[i][0] + dx
        if borders[3] - r >= balls[i][1] + dy >= r + borders[2]:
            y = balls[i][1] + dy
        else:
            dy = -dy
            y = balls[i][1] + dy
        circle(screen, color, (x, y), r)
        # Замена предыдущих характеристик шарика на новые
        balls.pop(i)
        balls.insert(i, [x, y, r, color, dx, dy])


def new_square():
    """
    Создаёт квадрат, который через определённое время телепортируется в случайное место,
    не меняя свою скорость, цвет и размер
    """
    x = randint(100, 1100)
    y = randint(100, 600)
    r = randint(50, 70)
    dx = randint(-5, 5)
    dy = randint(-5, 5)
    color = COLORS[randint(0, 5)]
    teleport_timer = randint(15, 45)
    squares.append([x, y, r, color, dx, dy, teleport_timer])


def square_movement():
    """
    Функция производит перемещение квадратов за один тик
    :return:
    """
    for i in range(len(squares)):
        # Считывание параметров квадрата
        teleport_timer = squares[i][6]
        dx = squares[i][4]
        dy = squares[i][5]
        r = squares[i][2]
        color = squares[i][3]
        # Отскоки
        if borders[1] - r/2 >= squares[i][0] + dx >= r/2 + borders[0]:
            x = squares[i][0] + dx
        else:
            dx = -dx
            x = squares[i][0] + dx
        if borders[3] - r/2 >= squares[i][1] + dy >= r/2 + borders[2]:
            y = squares[i][1] + dy
        else:
            dy = -dy
            y = squares[i][1] + dy
        rect(screen, color, (x - round(r/2), y + round(r/2), r, r))
        # Замена предыдущих характеристик квадрата на новые
        squares.pop(i)
        squares.insert(i, [x, y, r, color, dx, dy, teleport_timer])


def teleportation():
    """
    Телепортация шариков
    :return:
    """
    for i, square in enumerate(squares):
        teleport_timer = square[6]
        old_r = square[2]
        old_color = square[3]
        old_dx = square[4]
        old_dy = square[5]
        if tick_count % teleport_timer == 0:
            x = randint(100, 1100)
            y = randint(100, 600)
            squares.pop(i)
            squares.insert(i, [x, y, old_r, old_color, old_dx, old_dy, teleport_timer])


def score_count(event):
    """
    Функция проверяет попадание игрока в мишень и начисляет соответствующее число очков
    :param event: событие (нажатие на кнопку мыши)
    :return: возвращает число очков после нажатия на левую кнопку мыши
    """
    global score
    (x_click, y_click) = event.pos
    # Попадание в шарик
    for i, ball in enumerate(balls):
        x = ball[0]
        y = ball[1]
        r = ball[2]
        if (x_click-x)**2 + (y_click-y)**2 <= r**2:
            score += 1
            balls.pop(i)
    # Попадание в квадрат
    for i, square in enumerate(squares):
        x = square[0]
        y = square[1]
        r = square[2]
        if x - r/2 <= x_click <= x + r/2 and y - r/2 <= y_click <= y + r/2:
            score += 3
            squares.pop(i)
    print('Текущее число очков после нажатия:', score)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    tick_count += 1
    if tick_count == 1200:
        finished = True
        output = open('best_players', 'w')
        output_tech = open('best_players_tech', 'w')
        i = 0
        while i < 10:
            print(i)
            if players[i] < score:
                print(i)
                for j in range(8, i, -1):
                    players[j + 1] = players[j]
                print(i)
                players[i] = score
                i = 10
            i += 1
        for i in range(10):
            print('Result', i + 1, ': ', players[i], file=output)
            print(players[i], file=output_tech)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            score_count(event)
    if tick_count % 30 == 0:
        new_ball()
    if tick_count % 60 == 0:
        new_square()
    ball_movement()
    square_movement()
    teleportation()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
