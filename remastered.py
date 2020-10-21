import pygame
import numpy as np
from pygame.draw import *
from random import randint
name = str(input())
pygame.init()
pygame.font.init()

# Параметры
FPS = 60
WIDTH = 1000
HEIGHT = 600
ball_time = 30
square_time = 60
max_balls = 5
max_squares = 3
score = 0
tick_count = 0
ball_score = 1
square_score = 3
balls = []
squares = []
FONT_SIZE = 32
max_time = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
names_list = ['name' for i in range(10)]
scores_list = [0 for i in range(10)]

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def read_records():
    """
    Функция считывает таблицу рекордов в списки
    :return:
    """
    names = open('records_names', 'r')
    scores = open('records_scores', 'r')
    r_1 = names.readlines()
    r_2 = scores.readlines()
    for i in range(10):
        r_1[i] = r_1[i].rstrip()
        r_2[i] = r_2[i].rstrip()
        scores_list[i] = int(r_2[i])
        names_list[i] = str(r_1[i])


class Ball:
    def __init__(self):
        """
        Функция-конструктор объекта класса шариков
        """
        self.r = randint(30, 50)
        (self.x, self.y) = (randint(self.r, WIDTH - self.r), randint(self.r, HEIGHT - self.r))
        (self.dx, self.dy) = (randint(-5, 5), randint(-5, 5))
        self.color = COLORS[randint(0, 5)]

    def movement(self):
        """
        Функция рисует положение шарика на текущем кадре
        :return:
        """
        if not WIDTH - self.r > self.x + self.dx > self.r:
            self.dx = - self.dx
        if not HEIGHT - self.r > self.y + self.dy > self.r:
            self.dy = -self.dy
        self.y += self.dy
        self.x += self.dx
        circle(screen, self.color, (self.x, self.y), self.r)

    def score(self, event, i):
        """
        Функция проверяет попадание по шарику для каждого нажатия мыши, в случае попадания удаляет шарик
        :param event: нажатие на кнопку мыши
        :param i: номер шарика в списке шариков
        :return:
        """
        global score
        (x_click, y_click) = event.pos
        if (x_click-self.x)**2 + (y_click-self.y)**2 <= self.r**2:
            score += ball_score
            balls.pop(i)


class Square:
    def __init__(self):
        """
        Функция-конструктор объекта класса квадратов
        """
        self.r = randint(30, 50)
        (self.x, self.y) = (randint(self.r, WIDTH - self.r), randint(self.r, HEIGHT - self.r))
        (self.dx, self.dy) = (randint(-5, 5), randint(-5, 5))
        self.color = COLORS[randint(0, 5)]
        self.teleport_time = randint(60, 90)

    def movement(self):
        """
        Функция рисует положение квадрата на текущем кадре
        :return:
        """
        if not WIDTH - self.r > self.x + self.dx > self.r:
            self.dx = - self.dx
        if not HEIGHT - self.r > self.y + self.dy > self.r:
            self.dy = -self.dy
        self.y += self.dy
        self.x += self.dx
        rect(screen, self.color, (self.x - self.r, self.y - self.r, 2*self.r, 2*self.r))

    def teleport(self):
        """
        Функция телепортирует квадрат в случайное место на игровом поле
        :return:
        """
        if tick_count % self.teleport_time == 0:
            (self.x, self.y) = (randint(self.r, WIDTH - self.r), randint(self.r, HEIGHT - self.r))

    def score(self, event, i):
        """
        Функция проверяет попадание по квадрату для каждого нажатия мыши, в случае попадания удаляет квадрат
        :param event: нажатие на кнопку мыши
        :param i: номер квадрата в списке квадратов
        :return:
        """
        global score
        (x_click, y_click) = event.pos
        if self.x - self.r <= x_click <= self.x + self.r and self.y - self.r <= y_click <= self.y + self.r:
            score += square_score
            squares.pop(i)


def text():
    """
    Функция отображает имя игрока, текущий счёт и оставшееся время на игровой панели
    :return:
    """
    screen.blit(pygame.font.Font(None, FONT_SIZE).render('Игрок:'
                                                         + name
                                                         + 'Текущий счёт:'
                                                         + str(score)
                                                         + 'Оставшееся время:'
                                                         + str(max_time - np.floor(tick_count/FPS)), 1, WHITE),
                (int((WIDTH - 20 * FONT_SIZE) / 2), 0))


def end_game():
    """
    Останавливает игру после истечения времени max_time, записывает результат, если он попал в десятку лучших
    :return:
    """
    global score
    w = open('records', 'w')
    w_1 = open('records_scores', 'w')
    w_2 = open('records_names', 'w')
    i = 0
    while i < 10:
        if scores_list[i] < score:
            for j in range(8, i, -1):
                scores_list[j + 1] = scores_list[j]
                names_list[j + 1] = names_list[j]
            scores_list[i] = score
            names_list[i] = name
            i = 9
        i += 1
    for i in range(10):
        print(names_list[i], ': ', scores_list[i], file=w)
        print(scores_list[i], file=w_1)
        print(names_list[i], file=w_2)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Открываем таблицу рекордов
read_records()

while not finished:
    clock.tick(FPS)
    tick_count += 1
    # Проверка условия окончания игры
    if tick_count == FPS * max_time:
        end_game()
        finished = True
    # Появление новых шариков и квадратов
    if tick_count % ball_time == 0 and len(balls) < max_balls:
        balls.append(Ball())
    if tick_count % square_time == 0 and len(squares) < max_squares:
        squares.append(Square())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, ball in enumerate(balls):
                ball.score(event, i)
            for i, square in enumerate(squares):
                square.score(event, i)
    for ball in balls:
        ball.movement()
    for square in squares:
        square.teleport()
        square.movement()
    text()
    pygame.display.update()
    screen.fill(BLACK)


pygame.quit()
