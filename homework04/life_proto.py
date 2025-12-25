import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = GameOfLife.create_grid(self, True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("snow"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("snow"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            GameOfLife.draw_grid(self)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        x, y = self.cell_width, self.cell_height
        gr = [[0] * x for _ in range(y)]
        if randomize:
            for i in range(y):
                for j in range(x):
                    if random.randint(0, 1):
                        gr[i][j] = 1
        return gr

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        gr = self.grid
        x, y = self.cell_width, self.cell_height
        size = self.cell_size
        for i in range(y):
            for j in range(x):
                if gr[i][j]:
                    color = pygame.Color("darkolivegreen3")
                else:
                    color = pygame.Color("lightpink1")
                pygame.draw.rect(self.screen, color, (size * j, size * i, self.height, self.width))
        GameOfLife.draw_lines(self)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        y, x = cell
        neighbours = []
        coords = (
            (y - 1, x - 1),
            (y - 1, x),
            (y - 1, x + 1),
            (y, x - 1),
            (y, x + 1),
            (y + 1, x - 1),
            (y + 1, x),
            (y + 1, x + 1),
        )
        for i, j in coords:
            if 0 <= j < self.cell_width and 0 <= i < self.cell_height:
                neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        x, y = self.cell_width, self.cell_height
        gr = self.grid
        gr1 = [[0] * x for _ in range(y)]
        for i in range(y):
            for j in range(x):
                t = GameOfLife.get_neighbours(self, (i, j)).count(1)
                if gr[i][j]:
                    if t == 2 or t == 3:
                        gr1[i][j] = 1
                    else:
                        gr1[i][j] = 0
                else:
                    if t == 3:
                        gr1[i][j] = 1
                    else:
                        gr1[i][j] = 0
        return gr1
