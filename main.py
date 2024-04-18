import pygame
from anneling import evaluate_func, random_init, solve, init_set

# Specify the path to your CSV file
csv_file_path = "input.csv"


def read_text(path):
    with open(path, "r") as file:
        line_array = file.read().splitlines()
        cell_array = [
            [int(cell) if cell.isdigit() else 0 for cell in line] for line in line_array
        ]
    return cell_array


# Example usage:
file_path = "your_file.txt"  # Replace with the actual path to your text file
data_2d_list = read_text(file_path)

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 540, 540
SIZE = WIDTH // 9
FONT = pygame.font.SysFont("Arial", SIZE - 10)

# Set up the game board
board = [
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (2, 1), (0, 0), (0, 0), (1, 1), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
]

for i in range(9):
    for j in range(9):
        board[i][j] = (data_2d_list[i][j], 1 if data_2d_list[i][j] != 0 else 0)

# print(board)

# Set up the game screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Game")
choosing_color = (0, 100, 150)
valid_color = (200, 200, 20)
wrong_color = (255, 10, 10)
preset_color = (200, 200, 200)
normal_color = (255, 255, 255)


# Function to draw the board
def draw_board():
    for i in range(9):
        for j in range(9):
            text = None
            if board[i][j][0] == 0:
                text = FONT.render("", True, (0, 0, 0))
            else:
                text = FONT.render(str(board[i][j][0]), True, (0, 0, 0))
            if board[i][j][1] == 0:
                pygame.draw.rect(
                    screen, normal_color, pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                )

            elif board[i][j][1] == 1:
                pygame.draw.rect(
                    screen, preset_color, pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                )
            elif board[i][j][1] == 2:
                pygame.draw.rect(
                    screen, wrong_color, pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                )
            elif board[i][j][1] == 3:
                pygame.draw.rect(
                    screen, valid_color, pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                )
            elif board[i][j][1] == 4:
                pygame.draw.rect(
                    screen, choosing_color, pygame.Rect(j * SIZE, i * SIZE, SIZE, SIZE)
                )
            screen.blit(text, (j * SIZE + 20, i * SIZE + 4))


# Function to draw the gridlines
def draw_gridlines():
    for i in range(0, WIDTH, SIZE):
        if i % (3 * SIZE) == 0:
            pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, HEIGHT), 3)
        else:
            pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, SIZE):
        if i % (3 * SIZE) == 0:
            pygame.draw.line(screen, (0, 0, 0), (0, i), (WIDTH, i), 3)

        else:
            pygame.draw.line(screen, (0, 0, 0), (0, i), (WIDTH, i))


def is_valid_position(x, y, k):
    y_ord, x_ord = y // SIZE, x // SIZE
    # check rows and columns
    row_set, col_set, sub_set = init_set(board, x_ord, y_ord)
    if k in row_set:
        print("row_set_w", row_set)
        return False
    if k in col_set:
        print("col_set_w", col_set)
        return False
    # check sub-grids
    if k in sub_set:
        print("subgrid_set_w", sub_set)
        return False
    return True


def is_valid_sudoku(board):
    # Check rows and columns
    for i in range(9):
        row_set, col_set = set(), set()
        for j in range(9):
            if board[i][j][0] != 0:
                if board[i][j][0] in row_set:
                    return False
                row_set.add(board[i][j][0])
            if board[j][i][0] != 0:
                if board[j][i][0] in col_set:
                    return False
                col_set.add(board[j][i][0])

    # Check 3x3 sub-grids
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid_set = set()
            for x in range(i, i + 3):
                for y in range(j, j + 3):
                    if board[x][y][0] != 0:
                        if board[x][y][0] in subgrid_set:
                            return False
                        subgrid_set.add(board[x][y][0])

    return True


def handle_input(x, y, k):
    if board[y // SIZE][x // SIZE][1] == 1:
        return
    if not is_valid_position(x, y, k):
        print(x // SIZE, y // SIZE)
        board[y // SIZE][x // SIZE] = (k, 2)
    else:
        # for
        board[y // SIZE][x // SIZE] = (k, 3)


def color_special_square(x = -1, y = -1):
    y_ord, x_ord = y // SIZE, x // SIZE
    for i in range(9):
        for j in range(9):
            if board[i][j][1] == 4:
                board[i][j] = (board[i][j][0], 0)

    if x == -1 or y == -1:
        return
    if board[y_ord][x_ord][1] == 0:
        k = board[y_ord][x_ord][0]
        board[y_ord][x_ord] = (k, 4)


# Game loop
click = 0
coord = (0, 0)
solving = 0
running = True
ite = 1
current_error = int()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            coord = pygame.mouse.get_pos()
            click = 1
            color_special_square(coord[0], coord[1])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                print("ite: ", ite)
                break
            k = 0
            if event.key == pygame.K_1:
                k = 1
            elif event.key == pygame.K_2:
                k = 2
            elif event.key == pygame.K_3:
                k = 3
            elif event.key == pygame.K_4:
                k = 4
            elif event.key == pygame.K_5:
                k = 5
            elif event.key == pygame.K_6:
                k = 6
            elif event.key == pygame.K_7:
                k = 7
            elif event.key == pygame.K_8:
                k = 8
            elif event.key == pygame.K_9:
                k = 9
            else:
                if event.key == pygame.K_s:
                    random_init(board)
                    current_error = evaluate_func(board)

                elif event.key == pygame.K_p:
                    solving = 1
                elif event.key == pygame.K_a:
                    solving = 0
                click = 0
                continue
            handle_input(coord[0], coord[1], k)
            current_error = evaluate_func(board)
            click = 0
    if solving == 1:
        current_error = solve(board, ite, current_error)
        if (current_error >= 0):
            solving = 0
            print(ite)
        ite += 1
    screen.fill((255, 255, 255))
    draw_board()
    draw_gridlines()
    color_special_square()
    pygame.display.flip()
