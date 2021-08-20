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
k = {
    "white": True,
    "black": False
}

list_of_figures = []

pawns = []
rooks = []
knights = []
bishops = []
kings = []
queens = []
cells = []
color_cells = []

my_figures = []
opponent_figures = []


def create_figures():
    global list_of_figures
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
    list_of_figures = pawns + knights + rooks + bishops + kings + queens


def filter_figures(my_color):
    for f in list_of_figures:
        if f.color == my_color:
            my_figures.append(f)
        else:
            opponent_figures.append(f)


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

    for index in range(len(rooks)):
        if rooks[index].color == "black":
            rooks[index].start_position = chessboard[0][black_index]
            black_index += 7
        else:
            rooks[index].start_position = chessboard[7][white_index]
            white_index += 7

    black_index = 2
    white_index = 2

    for index in range(len(bishops)):
        if bishops[index].color == "black":
            bishops[index].start_position = chessboard[0][black_index]
            black_index += 3
        else:
            bishops[index].start_position = chessboard[7][white_index]
            white_index += 3

    black_index = 1
    white_index = 1

    for index in range(len(knights)):
        if knights[index].color == "black":
            knights[index].start_position = chessboard[0][black_index]
            black_index += 5
        else:
            knights[index].start_position = chessboard[7][white_index]
            white_index += 5

    for index in range(len(kings)):
        if kings[index].color == "black":
            kings[index].start_position = chessboard[0][4]
        else:
            kings[index].start_position = chessboard[7][4]

    for index in range(len(queens)):
        if queens[index].color == "black":
            queens[index].start_position = chessboard[0][3]
        else:
            queens[index].start_position = chessboard[7][3]


def cells_chess_board(color):
    counter = 0
    col = k[color]
    for index in range(len(chessboard)):
        for x, y in chessboard[index]:
            counter += 1
            rect = pygame.Rect(x, y, 80, 80)

            cell = Cells(rect)
            if col:
                cell.standard_color = dict_color[counter % 2 == 1]
                cell.color = cell.standard_color
            else:
                cell.standard_color = dict_color[counter % 2 == 0]
                cell.color = cell.standard_color
            if counter % 8 == 0:
                col = not col
            cells.append(cell)


def draw_chess_board():
    for cell in cells:
        if cell.is_active:
            pygame.draw.rect(screen, color="lightblue", rect=cell)
        else:
            pygame.draw.rect(screen, color=cell.color, rect=cell)
        if cell.under_check:
            pygame.draw.rect(screen, color="red", rect=cell)


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


def check_king_under_attack(pos):
    for f in opponent_figures:
        for x_y in f.attack_moves:
            if tuple(x_y) == pos:
                return True
    return False


def rules(obj: Figure):
    global list_of_figures
    obj.moves.clear()
    list_of_figures = my_figures + opponent_figures

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
        obj.attack_moves.clear()
        cant_move = False
        f_index = get_index()
        pos = tuple(board[f_index[0] - 1, f_index[1]])
        if not on_way(pos):
            obj.moves.append(pos)
        else:
            cant_move = True
        if tuple(obj.current_position) == tuple(obj.start_position):
            pos = tuple(board[f_index[0] - 2, f_index[1]])
            if not on_way(pos) and not cant_move:
                obj.moves.append(pos)
        try:
            obj.attack_moves.append(tuple(board[f_index[0] - 1, f_index[1] + 1]))
        except IndexError:
            pass
        try:
            obj.attack_moves.append(tuple(board[f_index[0] - 1, f_index[1] - 1]))
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
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            x += 1
            if x > 7:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            y -= 1
            if y < 0:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            y += 1
            if y > 7:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)

            if on_way(pos):
                break

    def bishop(board: np.array):
        index = get_index()
        x, y = index.copy()
        for c in range(8):
            x -= 1
            y -= 1
            if x < 0 or y < 0:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            x += 1
            y += 1
            if x > 7 or y > 7:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            y -= 1
            x += 1
            if y < 0 or x > 7:
                break
            pos = tuple(board[x][y])
            obj.moves.append(pos)
            if on_way(pos):
                break

        x, y = index.copy()
        for c in range(8):
            y += 1
            x -= 1
            if y > 7 or x < 0:
                break
            pos = tuple(board[x][y])

            obj.moves.append(pos)
            if on_way(pos):
                break

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

            under_attack_ = check_king_under_attack(obj)
            if not under_attack_:
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
    for fg in list_of_figures:
        rules(fg)


def check_check():
    global my_king

    pos = tuple(my_king.current_position)
    tuple_of_position = tuple(map(lambda x: (x.x, x.y), cells))

    kings_cell = tuple_of_position.index(pos)

    for f in opponent_figures:
        if pos in f.attack_moves:
            cells[kings_cell].under_check = True
            break


color = "white"

create_chess_board()
cells_chess_board(color)
create_figures()
set_start_position()
filter_figures(color)
add_images()
update_figures(list_of_figures)
update_coordinates()

running = True
active_fig = False
figure = None
your_move = True

all_moves = []
q = {
    True: "white",
    False: "black"
}


def get_king():
    for f in my_figures:
        if f.name == "king":
            return f


my_king = get_king()

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
            for cell in cells:
                if cell.collidepoint(position):
                    de_highlight(cells)
                    cell.is_active = True
                    coordinates = (cell.x, cell.y)
                    if not active_fig:
                        for f in my_figures:
                            if tuple(f.current_position) == tuple(coordinates):
                                figure = f
                                active_fig = True
                                break
                    else:
                        for f in opponent_figures:
                            if coordinates == tuple(f.current_position) and figure.can_attack(coordinates):
                                index = opponent_figures.index(f)
                                popped = list_of_figures.pop(index)
                                if figure.can_move(coordinates):
                                    figure.do_move(coordinates)
                                    update_coordinates()

                                    under_attack = check_king_under_attack(tuple(my_king.current_position))
                                    if under_attack:
                                        figure.cancel_move()
                                        opponent_figures.insert(index, popped)
                                        update_coordinates()
                                        active_fig = False
                                        break
                                elif figure.name == "pawn":
                                    figure.do_move(coordinates)
                                    update_coordinates()

                                    under_attack = check_king_under_attack(tuple(my_king.current_position))
                                    if under_attack:
                                        figure.cancel_move()
                                        list_of_figures.insert(index, popped)
                                        update_coordinates()
                                        active_fig = False
                                        break
                                    your_move = not your_move
                                break
                            elif coordinates == tuple(f.current_position):
                                break
                        else:
                            if figure.can_move(coordinates):
                                figure.do_move(coordinates)
                                update_coordinates()

                                under_attack = check_king_under_attack(tuple(my_king.current_position))
                                if under_attack:
                                    figure.cancel_move()
                                    update_coordinates()
                                    active_fig = False
                                    break
                                your_move = not your_move

                        active_fig = False
                    update_coordinates()
            for cell in cells:
                cell.under_check = False
            # check_check()
