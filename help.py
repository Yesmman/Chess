import pygame
import pathlib
from Figures import Figure, Cells
from functools import partial
import numpy as np

list_of_paths = []
for path in pathlib.Path().glob(pattern="*.png"):
    list_of_paths.append(path)
WIDTH = 800
HEIGHT = 800

fps = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cheese")

chessboard_list = []
chessboard = np.array(object=object)


# x+80, y+80
def create_chess_board():
    global chessboard
    start_x = 100
    start_y = 50
    raw = []
    for i in range(8):
        for j in range(8):
            raw.append((start_x, start_y))

            start_x += 80
        chessboard_list.append(raw.copy())
        raw.clear()
        start_x = 100
        start_y += 80

    chessboard = np.array(chessboard_list)


dict_color = {
    True: "White",
    False: "Pink"
}
#
k = False

list_of_figures = []
list_of_coordinates = []
pawns = []
rooks = []
knights = []
bishops = []
kings = []
queens = []
cells = []
color_cells = []


# white_attack = []
# black_attack = []

def create_figures():
    for index in range(8):
        pawns.append(Figure("pawn", "white"))
        pawns.append(Figure("pawn", "black"))
    for index in range(2):
        knights.append(Figure("knight", "white"))
        rooks.append(Figure("rook", "white"))
        knights.append(Figure("knight", "black"))
        rooks.append(Figure("rook", "black"))
        bishops.append(Figure("bishop", "white"))
        bishops.append(Figure("bishop", "black"))
    kings.append(Figure("king", "white"))
    kings.append(Figure("king", "black"))
    queens.append(Figure("queen", "white"))
    queens.append(Figure("queen", "black"))


#
#
def set_start_position():
    black_index = 0
    white_index = 0
    for index in range(len(pawns)):
        if pawns[index].color == "black":
            pawns[index].start_position = chessboard[1][black_index]
            black_index += 1
        else:
            pawns[index].start_position = chessboard[6][white_index]
            white_index += 1

    black_index = 0
    white_index = 0
    # print(black_index, white_index)
    for index in range(len(rooks)):
        if rooks[index].color == "black":
            rooks[index].start_position = chessboard[0][black_index]
            black_index += 7
        else:
            rooks[index].start_position = chessboard[7][white_index]
            white_index += 7
    # for item in rooks:
    #    print(item.start_position)
    black_index = 2
    white_index = 2

    for index in range(len(bishops)):
        if rooks[index].color == "black":
            bishops[index].start_position = chessboard[0][black_index]
            black_index += 3
        else:
            bishops[index].start_position = chessboard[7][white_index]
            white_index += 3

    black_index = 1
    white_index = 1

    for index in range(len(knights)):
        if rooks[index].color == "black":
            knights[index].start_position = chessboard[0][black_index]
            black_index += 5
        else:
            knights[index].start_position = chessboard[7][white_index]
            white_index += 5

    for index in range(len(kings)):
        if rooks[index].color == "black":
            kings[index].start_position = chessboard[0][4]
        else:
            kings[index].start_position = chessboard[7][4]

    for index in range(len(queens)):
        if rooks[index].color == "black":
            queens[index].start_position = chessboard[0][3]
        else:
            queens[index].start_position = chessboard[7][3]


def cells_chess_board():
    counter = 0
    global k
    for index in range(len(chessboard)):
        for x, y in chessboard[index]:
            counter += 1
            rect = pygame.Rect(x, y, 80, 80)

            cell = Cells(rect)
            if k:
                cell.standard_color = dict_color[counter % 2 == 1]
                cell.color = cell.standard_color
            else:
                cell.standard_color = dict_color[counter % 2 == 0]
                cell.color = cell.standard_color
            if counter % 8 == 0:
                k = not k
            cells.append(cell)


#
#
def draw_chess_board():
    for cell in cells:
        if cell.is_active:
            pygame.draw.rect(screen, color="lightblue", rect=cell)
        else:
            pygame.draw.rect(screen, color=cell.color, rect=cell)


def add_images():
    global list_of_figures
    list_of_figures = pawns + rooks + knights + kings + queens + bishops
    for f in list_of_figures:
        f.image = pygame.image.load(f.image)


def de_highlight(list_):
    for cell in list_:
        cell.is_active = False


def update_figures(list_):
    for f in list_:
        f.current_position = f.start_position


def get_col(number):
    return number % 8


def get_raw(number):
    return int(number / 8)


def rules(obj: Figure):
    pawn_dict = {
        "black": 1,
        "white": -1
    }
    obj.moves.clear()

    def get_index():
        for i_ in range(8):
            for j_ in range(8):
                tup = tuple(chessboard[i_, j_])
                pos = tuple(obj.current_position)
                if tup == pos:
                    return [i_, j_]

    def on_way(pos):
        for f in list_of_figures:
            if pos == tuple(f.current_position):
                return True
        return False

    def pawn(board: np.array):

        index = get_index()
        obj.moves.append(tuple(board[index[0] + pawn_dict[obj.color], index[1]]))
        if tuple(obj.current_position) == tuple(obj.start_position):
            obj.moves.append(tuple(board[index[0] + 2 * pawn_dict[obj.color], index[1]]))
        try:
            obj.attack_moves.append(tuple(board[index[0] + pawn_dict[obj.color], index[1] + 1]))
        except IndexError:
            pass
        try:
            obj.attack_moves.append(tuple(board[index[0] + pawn_dict[obj.color], index[1] - 1]))
        except IndexError:
            pass

    def rook(board: np.array):
        index = get_index()
        x, y = index.copy()
        for c in range(8):
            x -= 1

            if x < 0:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            x += 1
            if x > 7:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            y -= 1
            if y < 0:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            y += 1
            if y > 7:
                break
            pos = tuple(board[x][y])

            if on_way(pos):
                break
            obj.moves.append(pos)

    def bishop(board: np.array):
        index = get_index()
        x, y = index.copy()
        for c in range(8):
            x -= 1
            y -= 1
            if x < 0 or y < 0:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            x += 1
            y += 1
            if x > 7 or y > 7:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            y -= 1
            x += 1
            if y < 0 or x > 7:
                break
            pos = tuple(board[x][y])
            if on_way(pos):
                break
            obj.moves.append(pos)

        x, y = index.copy()
        for c in range(8):
            y += 1
            x -= 1
            if y > 7 or x < 0:
                break
            pos = tuple(board[x][y])

            if on_way(pos):
                break
            obj.moves.append(pos)

    def knight(board: np.array):
        index = get_index()
        list_of_values = [(-2, 1), (-2, -1), (1, -2), (1, 2), (2, 1), (2, -1), (-1, 2), (-1, -2)]
        for value in list_of_values:
            x, y = index
            x += value[0]
            y += value[1]
            if x < 0 or y < 0 or x > 7 or y > 7:
                continue
            pos = tuple(board[x][y])

            if on_way(pos):
                continue
            obj.moves.append(pos)

    def king(board: np.array):
        index = get_index()
        list_of_values = [(1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, -1), (-1, 1)]
        for values in list_of_values:
            x, y = index
            x += values[0]
            y += values[1]
            if x < 0 or y < 0 or x > 7 or y > 7:
                continue

            pos = tuple(board[x][y])
            if on_way(pos):
                continue
            obj.moves.append(pos)

    def queen(board: np.array):
        rook(board)
        bishop(board)

    functions = {"pawn": pawn,
                 "rook": rook,
                 "bishop": bishop,
                 "knight": knight,
                 "king": king,
                 "queen": queen}
    functions[obj.name](chessboard)
    if obj.name != "pawn":
        obj.attack_moves = obj.moves.copy()


def update_coordinates():
    list_of_coordinates.clear()
    for fg in list_of_figures:
        list_of_coordinates.append(fg.current_position)
        rules(fg)


#
create_chess_board()
cells_chess_board()
create_figures()
set_start_position()
add_images()
update_figures(list_of_figures)
update_coordinates()

running = True
active_fig = False
figure = None
#
while running:

    screen.fill("black")
    draw_chess_board()
    i = 0
    for fig in list_of_figures:
        screen.blit(fig.image, fig.current_position)
        i += 1
    pygame.display.flip()
    position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item in cells:
                if item.collidepoint(position):
                    de_highlight(cells)
                    item.is_active = True
                    coordinates = (item.x, item.y)
                    if not active_fig:
                        for fig in list_of_figures:
                            if tuple(fig.current_position) == tuple(coordinates):
                                figure = fig
                                active_fig = True
                                break
                    else:

                        figure.do_move(coordinates)
                        active_fig = False
                    update_coordinates()
