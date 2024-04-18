import random
import math

# import copy
import pygame.time

PRESET = 1
VALID = 3
MAX_SCORE = 36
checkboard = [(0, 0), (0, 3), (0, 6), (3, 0), (6, 0), (3, 3), (3, 6), (6, 3), (6, 6)]


def preset_init(board, x, y):
    """
        Initialize set of ``row`` and ``col`` of coordinate ``x, y`` \
        in ``board`` that pre_intialize from begining or find in the learning phrase
        Args:
            ``board``: Sudoku board, 2d list
            ``x``: x co-ordination
            ``y``: y co-ordination
        Returns:
            ``row_set``: Set of blocks that in share same coord y that pre-init or found
            ``col_set``: Set of blocks that in share same coord x that pre-init or found
    """
    row_set, col_set = set(), set()
    for i in range(9):
        if board[i][x][1] == PRESET or board[i][x][1] == VALID:
            col_set.add(board[i][x][0])
        if board[y][i][1] == PRESET or board[y][i][1] == VALID:
            row_set.add(board[y][i][0])

    return row_set, col_set


def init_set(board, x, y):
    """
        Return sets of ``col``, ``row`` and ``3x3 subgrid`` \
        of coordinate ``x, y`` from ``board``
        Args:
            ``board``: Sudoku board, 2d list
            ``x``: x co-ordination
            ``y``: y co-ordination
        Returns:
            ``row_set``: Set of blocks that in share same coord y
            ``col_set``: Set of blocks that in share same coord x
            ``subgrid``: Set of blocks in a 3x3 subgrid contains (x, y)
    """
    row_set, col_set, subgrid = set(), set(), set()
    for i in range(9):
        # column
        if board[i][x][0] != 0:
            col_set.add(board[i][x][0])
        # row
        if board[y][i][0] != 0:
            row_set.add(board[y][i][0])

    startx = int(x / 3) * 3
    starty = int(y / 3) * 3

    for i in range(3):
        for j in range(3):
            if board[i + starty][j + startx][0] != 0:
                subgrid.add(board[i + starty][j + startx][0])
    return row_set, col_set, subgrid

def evaluate_func(board):
    """
        Evaluate the state of ``board``
        
        Returns:
            ``error``: The value of current ``board`` state
    """
    # row_sum, col_sum, grid_sum = list(), list(), list()
    # for i in range(9):
    #     val_r, val_c, val_g = 0, 0, 0
    #     for j in range(9):
    #         val_r += board[i][j][0]
    #         val_c += board[j][i][0]
    #     row_sum.append(val_r)
    #     col_sum.append(val_c)

    # for i in range(0, 9, 3):
    #     for j in range(0, 9, 3):
    #         val_g = 0
    #         for i1 in range(i, i + 3):
    #             for j1 in range(j, j + 3):
    #                 val_g += board[i1][j1][0]
    #         grid_sum.append(val_g)
    # print(row_sum)
    # print(col_sum)
    error = 0
    # for i in range(9):
    #     error += 1 if (row_sum[i] == 45) else -1
    #     error += 1 if (col_sum[i] == 45) else -1

    for i in range(9):
        row_set, col_set, _ = init_set(board, i, i)
        error += 0 if len(row_set) == 9 else len(row_set) - 9
        error += 0 if len(col_set) == 9 else len(col_set) - 9

    print(error)
    return error


def get_subgrid(board, x, y):
    """
    Return a list of elements in ``3x3 subgrid`` contains coordinate ``x, y``\
    that contains ``y_ord``, ``x_ord``, ``board[y_ord][x_ord]``.   
        Args:
            ``board``: Sudoku board, 2d list
            ``x``: x co-ordination
            ``y``: y co-ordination
        Returns:
            ``subgrid``: List of blocks in a 3x3 subgrid contains (x, y) 
            ``subgrid type``: tuple of ``y``, ``x``, ``board[y][x]``
    """
    startx = int(x / 3) * 3
    starty = int(y / 3) * 3

    subgrid = list()
    for y in range(3):
        for x in range(3):
            subgrid.append((y + starty, x + startx, board[y + starty][x + startx]))
    return subgrid


def random_init(board):
    """
    Fill the rest of the sudoku board by grid-rules.
    """
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            _, _, gridset = init_set(board, j, i)
            if len(gridset) == 9:
                continue
            for y_i in range(3):
                for x_i in range(3):
                    res = random.randint(1, 9)
                    while res in gridset and len(gridset) != 9:
                        res = random.randint(1, 9)

                    if (
                        board[x_i + i][y_i + j][1] != PRESET
                        and board[x_i + i][y_i + j][1] != VALID
                    ):
                        board[x_i + i][y_i + j] = (res, board[x_i + i][y_i + j][1])
                        gridset.add(res)

    return evaluate_func(board)


def random_subgrid(board):
    """
        Choose the ``3x3 subgrid`` randomly.
        If the subgrid is full or nearly full (8 / 9), \
        use the grid-rules to fill the last and remove that \
        subgrid from ``checkboard``
            Returns:
                ``y, x``: The top-left position of the subgrid
    """
    # found = False
    # checkboard = [(0, 0), (0, 3), (0, 6), (3, 0), (6, 0), (3, 3), (3, 6), (6, 3), (6, 6)]
    random.shuffle(checkboard)
    for minigrid in checkboard:
        (x, y) = minigrid
        subgrid = get_subgrid(board, x, y)
        count = 0
        for ele in subgrid:
            if ele[2][1] == VALID or ele[2][1] == PRESET:
                count += 1
                continue
        # print("checkboard size: ", len(checkboard))
        # print("checkboard: ", *checkboard)
        if count >= 8:
            # print(*subgrid)
            for ele in subgrid:
                if ele[2][1] != PRESET:
                    board[ele[0]][ele[1]] = (ele[2][0], VALID)
            # temp = input()
            checkboard.remove((x, y))
            if len(checkboard) == 0:
                return None, None
            continue
        elif count >= 6:
            if random.random() < 0.2:
                return y, x
        else:
            # print(*subgrid)
            return y, x
    return None, None


def clearboard(board):
    """
        Clear uncertain blocks to form the new board following the grid-rules.
    """
    for y in range(9):
        for x in range(9):
            if board[y][x][1] != PRESET and board[y][x][1] != VALID:
                board[y][x] = (0, 0)


def solve(board, ite, current_error):
    """
        Implement the stimulation Annealing (SA) Sudoku
    """
    max_iter = 2000
    if ite % max_iter == 1999:
        print("===========Reinitialize for better another aproach=========")
        clearboard(board)
        error = random_init(board)
        # assert False
        pygame.time.delay(500)
        return error
    # store = list()
    print("Current Best: ", current_error)
    # if current_error > -6 and ite % 197 == 1:
    #     reduce_board(board)

    y, x = random_subgrid(board)
    # print(x, y)
    if y is None or x is None:
        return 0
    checklist = list()
    subgrid = get_subgrid(board, x, y)
    x1, y1 = random.randint(0, 2), random.randint(0, 2)
    # print("check x1, y1")
    random.shuffle(subgrid)
    for ele in subgrid:
        if ele[2][1] != PRESET and ele[2][1] != VALID:
            x1 = ele[1] - x
            y1 = ele[0] - y

    # print(f"x = {x1 + x}, y = {y1 + y}, {board[y1 + y][x1 + x]}")

    foundBlock = False
    for ele in subgrid:
        # print("ele in subgrid: ", ele)
        if x1 == ele[1] - x and y1 == ele[0] - y:
            # print(ele)
            # print("Duplicate error")
            continue
        if ele[2][1] == PRESET or ele[2][1] == VALID:
            # print("Preset Error")
            continue
        y2, x2 = ele[0] - y, ele[1] - x
        prow_set, pcol_set = preset_init(board, x2 + x, y2 + y)

        if board[y1 + y][x1 + x][0] in prow_set or board[y1 + y][x1 + x][0] in pcol_set:
            # print("XY1 can fit in XY2 position")
            continue

        checklist.append((x2, y2, board[y2 + y][x2 + x]))
        foundBlock = True

    if not foundBlock:
        if board[y1 + y][x1 + x][1] != PRESET:
            board[y1 + y][x1 + x] = (board[y1 + y][x1 + x][0], VALID)
        return current_error

    # print("checklist: ", checklist)

    # prow_set, pcol_set = preset_init(board, x1 + x, y1 + y)
    # print(prow_set, pcol_set)
    # for ele in checklist:
    #     y2, x2 = ele[1], ele[0]
    #     if board[y1 + y][x1 + x][0] in prow_set or board[y1 + y][x1 + x][0] in pcol_set:
    #         checklist.remove(ele)

    ele = random.choice(checklist)
    # print("SWAP")
    x2, y2 = ele[0], ele[1]
    board[y1 + y][x1 + x], board[y2 + y][x2 + x] = (
        (board[y1 + y][x1 + x][0], 4),
        (board[y2 + y][x2 + x][0], 4),
    )
    board[y1 + y][x1 + x], board[y2 + y][x2 + x] = (
        board[y2 + y][x2 + x],
        board[y1 + y][x1 + x],
    )

    new_error = evaluate_func(board)
    deltaE = current_error - new_error
    if deltaE < 0:
        return new_error
    # print(deltaE)
    # print(float(-deltaE / float(ite * 0.0001)))
    EPSILON = math.exp(
        float(-deltaE / float((ite % 3000 if (ite % 3000 != 0) else 2999) * 0.00005))
    )
    print("EPSILON: ", EPSILON)
    if new_error >= 0:
        return new_error
    rate = random.random()
    if rate > EPSILON:
        # unacceptable result
        board[y1 + y][x1 + x], board[y2 + y][x2 + x] = (
            board[y2 + y][x2 + x],
            board[y1 + y][x1 + x],
        )
        return current_error

    return new_error
    # print(EPSILON)
