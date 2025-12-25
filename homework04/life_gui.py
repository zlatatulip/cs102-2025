import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cols * self.cell_size
        self.height = life.rows * self.cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("snow"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("snow"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        gr = self.life.curr_generation
        x, y = self.life.cols, self.life.rows
        size = self.cell_size
        for i in range(y):
            for j in range(x):
                if gr[i][j]:
                    color = pygame.Color('darkolivegreen3')
                else:
                    color = pygame.Color('lightpink1')
                pygame.draw.rect(self.screen, color, (size * j, size * i, self.height, self.width))
        self.draw_lines()

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = False
        while running and self.life.is_changing and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                if event.type == pygame.MOUSEBUTTONDOWN and paused:
                    x, y = event.pos
                    col = x // self.cell_size
                    row = y // self.cell_size

                    if 0 <= col < self.life.cols and 0 <= row < self.life.rows:
                        if self.life.curr_generation[row][col] == 0:
                            self.life.curr_generation[row][col] = 1
                        else:
                            self.life.curr_generation[row][col] = 0

            self.draw_lines()
            self.draw_grid()
            if not paused:
                self.life.step()
                clock.tick(self.speed)

            pygame.display.flip()
        pygame.quit()
