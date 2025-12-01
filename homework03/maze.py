from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    grid1 = deepcopy(grid)
    grid1[coord[0]][coord[1]] = " "
    return grid1


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = choice(range(1, rows - 1, 2)), choice(range(1, rows - 1, 2))
        y_in = choice(range(1, rows - 1, 2)) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = choice(range(1, rows - 1, 2)) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = rows - 2, 0
        x_out, y_out = 1, cols - 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    for x_start in range(1, rows, 2):
        for y_start in range(1, cols, 2):
            t = randint(0, 1)
            if t:
                y_next = y_start + 2
                if y_next >= cols - 1:
                    y_next -= 2
                    x_next = x_start - 2
                    if x_next <= 0:
                        continue
                else:
                    x_next = x_start
            else:
                x_next = x_start - 2
                if x_next <= 0:
                    x_next += 2
                    y_next = y_start + 2
                    if y_next >= cols - 1:
                        continue
                else:
                    y_next = y_start
            grid = remove_wall(grid, ((x_next + x_start) // 2, (y_next + y_start) // 2))

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    rows = len(grid)
    cols = len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    grid1 = deepcopy(grid)
    rows = len(grid)
    cols = len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid1[x][y] == k:
                if x - 1 < 0:
                    if grid1[x][y] != 1:
                        return grid1
                elif not grid1[x - 1][y]:
                    grid1[x - 1][y] = k + 1

                if x + 1 >= rows:
                    if grid1[x][y] != 1:
                        return grid1
                elif not grid1[x + 1][y]:
                    grid1[x + 1][y] = k + 1

                if y - 1 < 0:
                    if grid1[x][y] != 1:
                        return grid1
                elif not grid1[x][y - 1]:
                    grid1[x][y - 1] = k + 1

                if y + 1 >= cols:
                    if grid1[x][y] != 1:
                        return grid1
                elif not grid1[x][y + 1]:
                    grid1[x][y + 1] = k + 1
    return make_step(grid1, k + 1)


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    x, y = exit_coord[0], exit_coord[1]

    if grid[x][y] == 1:
        return [(x, y)]

    coords = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    for coord in coords:
        if coord[0] < 0 or coord[0] >= rows or coord[1] < 0 or coord[1] >= cols:
            continue
        if int(grid[x][y]) - 1 != grid[coord[0]][coord[1]]:
            continue
        x1, y1 = coord[0], coord[1]
        t = shortest_path(grid, (x1, y1))
        if t:
            if len(t) + 1 == grid[exit_coord[0]][exit_coord[1]]:
                return [(x, y)] + t
    return None


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    rows = len(grid)
    cols = len(grid[0])
    x, y = coord[0], coord[1]
    k = 0
    if x - 1 >= 0:
        k += grid[x - 1][y] == " "
    if x + 1 < rows:
        k += grid[x + 1][y] == " "
    if y - 1 >= 0:
        k += grid[x][y - 1] == " "
    if y + 1 < cols:
        k += grid[x][y + 1] == " "
    if k:
        return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, exits[0]
    for ex in exits:
        if encircled_exit(grid, ex):
            return grid, None
    rows = len(grid)
    cols = len(grid[0])
    grid1 = deepcopy(grid)
    for x in range(rows):
        for y in range(cols):
            if grid1[x][y] == " " or grid1[x][y] == "X":
                grid1[x][y] = 0
    grid1[exits[0][0]][exits[0][1]] = 1
    grid1 = make_step(grid1, 1)
    print(pd.DataFrame(grid1))
    path = shortest_path(grid1, exits[1])
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
