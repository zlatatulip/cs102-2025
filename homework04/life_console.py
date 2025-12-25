import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        data = self.life.curr_generation
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                try:
                    char = "#" if data[y][x] else " "
                    screen.addstr(y + 1, x + 1, char)
                except curses.error:
                    pass
        screen.refresh()

    def run(self) -> None:
        curses.initscr()
        win_height = self.life.rows + 2
        win_width = self.life.cols + 2

        screen = curses.newwin(win_height, win_width, 0, 0)
        screen.nodelay(True)
        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                key = screen.getch()
                if key == ord('q') or key == 27:
                    break

                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                curses.napms(300)
                self.life.step()
        finally:
            curses.endwin()
