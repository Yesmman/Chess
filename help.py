import pygame
import pathlib
from Figures import Figure
from functools import partial

list_of_paths = []
for path in pathlib.Path().glob(pattern="*.png"):
    list_of_paths.append(path)
WIDTH = 800
HEIGHT = 800

fps = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cheese")

chessboard = []


# x+80, y+80
def create_chess_board():
    start_x = 100
    start_y = 50
    for i in range(8):
        for j in range(8):
            chessboard.append((start_x, start_y))
            start_x += 80
        start_x = 100
        start_y += 80


dict_color = {
    True: "White",
    False: "Pink"
}

k = False

list_of_images = []
list_of_figures = []
list_of_coordinates = []


def create_figures():
    for i in range(8):
        pawns.append(Figure("pawn", "white"))
        pawns.append(Figure("pawn", "black"))
    for i in range(2):
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


pawns = []
rooks = []
knights = []
bishops = []
kings = []
queens = []

cells = []
color_cells = []

white_attack = []
black_attack = []


def set_start_position():
    # print(bishops)
    index_b = 0
    index_w = 0
    c_b = 0
    c_w = 0
    for item in pawns:
        if item.color == "black":
            if c_b == 0:
                index_b = 8

                c_b += 1

            item.start_position = chessboard[index_b]
            index_b += 1
        elif item.color == "white":
            if c_w == 0:
                index_w = 48
                c_w += 1
            item.start_position = chessboard[index_w]
            index_w += 1

    index_b = 0
    index_w = 0
    c_b = 0
    c_w = 0
    for item in rooks:
        if item.color == "black":
            if c_b == 0:
                index_b = 0

                c_b += 1

            item.start_position = chessboard[index_b]
            index_b += 7
        elif item.color == "white":
            if c_w == 0:
                index_w = 56
                c_w += 1
            item.start_position = chessboard[index_w]
            index_w = 63

    c_b = 0
    c_w = 0
    for item in bishops:
        if item.color == "black":
            if c_b == 0:
                index_b = 2

                c_b += 1

            item.start_position = chessboard[index_b]
            index_b = 5
        elif item.color == "white":
            if c_w == 0:
                index_w = 58
                c_w += 1
            item.start_position = chessboard[index_w]
            index_w = 61
    c_b = 0
    c_w = 0
    for item in knights:
        if item.color == "black":
            if c_b == 0:
                index_b = 1

                c_b += 1

            item.start_position = chessboard[index_b]
            index_b = 6
        elif item.color == "white":
            if c_w == 0:
                index_w = 57
                c_w += 1
            item.start_position = chessboard[index_w]
            index_w = 62

    for item in queens:
        if item.color == "black":
            item.start_position = chessboard[3]
        elif item.color == "white":
            item.start_position = chessboard[59]
    for item in kings:
        if item.color == "black":
            item.start_position = chessboard[4]
        elif item.color == "white":
            item.start_position = chessboard[60]


class Cells(pygame.Rect):
    def __init__(self, rect):
        super().__init__(rect)

        self.standard_color = "red"
        self.color = self.standard_color
        self.is_active = False


def cells_chess_board():
    counter = 0
    global k
    for x, y in chessboard:
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


def draw_chess_board():
    global k
    global i
    i = 1
    for cell in cells:
        # print(cell)
        if cell.is_active:
            pygame.draw.rect(screen, color="lightblue", rect=cell)
        else:
            pygame.draw.rect(screen, color=cell.color, rect=cell)


def add_images():
    global list_of_figures
    list_of_figures = pawns + rooks + knights + kings + queens + bishops
    for item in list_of_figures:
        item.image = pygame.image.load(item.image)
        # list_of_images.append(i)


def de_highlight(list_):
    for cell in list_:
        cell.is_active = False


def update_figures(list_):
    for fig in list_:
        fig.current_position = fig.start_position


def get_col(number):
    return number % 8


def get_raw(number):
    return int(number / 8)


def rules(obj: Figure):
    step_dict = {
        "black": 8,
        "white": -8
    }

    obj.moves.clear()

    def on_way(pos):
        for f in list_of_figures:
            if pos == f.current_position:
                return True
        return False

    def pawn(board: list):

        obj.attack_moves.clear()
        pos = obj.current_position
        index = board.index(pos)
        coord = index + step_dict[obj.color]
        obj.moves.append(board[coord])
        if pos == obj.start_position:
            obj.moves.append(board[index + 2 * step_dict[obj.color]])
        left = coord - 1
        right = coord + 1
        raw = (index + step_dict[obj.color]) // 8
        if left // 8 == raw:
            obj.attack_moves.append(board[left])
        if right // 8 == raw:
            obj.attack_moves.append(board[right])

    def rook(board: list):
        x = obj.current_position[0]
        y = obj.current_position[1]
        index = board.index((x, y))
        end_index = 8
        raw = int(index / 8)
        col = (index % 8)

        current_index = index
        right_end_index = end_index - col - 1
        for a in range(right_end_index):

            current_index += 1
            pos = board[current_index]

            obj.moves.append(board[current_index])
            if on_way(pos):
                break

        current_index = index
        for a in range(8 - right_end_index - 1):
            current_index -= 1
            pos = board[current_index]

            obj.moves.append(board[current_index])
            if on_way(pos):
                break

        current_index = index
        up_end_index = end_index - raw - 1
        for a in range(up_end_index):
            current_index += 8
            pos = board[current_index]

            obj.moves.append(board[current_index])
            if on_way(pos):
                break

        current_index = index
        for a in range(8 - up_end_index):
            current_index -= 8
            pos = board[current_index]

            obj.moves.append(board[current_index])
            if on_way(pos):
                break

    def bishop(board: list):

        x = obj.current_position[0]
        y = obj.current_position[1]
        index = board.index((x, y))

        current_index = index

        for a in range(8):
            if not get_raw(current_index) or not get_col(current_index):
                break
            current_index -= 9
            pos = board[current_index]

            obj.moves.append(pos)
            if on_way(pos):
                break

        current_index = index

        for a in range(8):
            if get_raw(current_index) >= 7 or get_col(current_index) >= 7:
                break
            current_index += 9
            if current_index >= 64:
                break
            pos = board[current_index]

            obj.moves.append(pos)
            if on_way(pos):
                break

        current_index = index
        for a in range(8):

            if not get_raw(current_index) or get_col(current_index) >= 7:
                break
            current_index -= 7
            pos = board[current_index]

            obj.moves.append(pos)
            if on_way(pos):
                break

        current_index = index
        for a in range(8):
            if get_raw(current_index) >= 7 or not get_col(current_index):
                break
            current_index += 7
            if current_index >= 64:
                break
            pos = board[current_index]

            obj.moves.append(pos)
            if on_way(pos):
                break


    def knight(board: list):
        x = obj.current_position[0]
        y = obj.current_position[1]
        index = board.index((x, y))
        list_of_values = [15, 17, 10, 6, -15, -17, -10, - 6]
        for value in list_of_values:
            try:
                obj.moves.append(board[index + value])
            except IndexError:
                continue
    # Knight is problem:: need to solve this

    def king(board: list):
        x = obj.current_position[0]
        y = obj.current_position[1]
        index = board.index((x, y))
        list_of_values = [-8, 8, -1, 1, -7, 7, -9, 9]
        raw = get_raw(index)
        col = get_col(index)

        if col == 7:
            list_of_values.remove(1)
            list_of_values.remove(9)
            list_of_values.remove(-7)
        elif col == 0:
            list_of_values.remove(-1)
            list_of_values.remove(-9)
            list_of_values.remove(7)
        if raw == 0:
            list_of_values.remove(-8)
            list_of_values.remove(-9)
            list_of_values.remove(-7)
        elif raw == 7:
            list_of_values.remove(8)
            list_of_values.remove(9)
            list_of_values.remove(7)

        obj.attack_moves.clear()
        for value in list_of_values:
            obj.attack_moves.append(board[index + value])
        for value in list_of_values:
            current_index = index + value
            under_attack = False
            pos = board[current_index]
            for f in list_of_figures:
                if f.color != obj.color:
                    for coordinates in f.attack_moves:
                        if coordinates == pos:
                            under_attack = True

            if not under_attack:
                obj.moves.append(pos)

    def queen(board: list):
        rook(board)
        bishop(board)

    functions = {"pawn": pawn,
                 "rook": rook,
                 "bishop": bishop,
                 "knight": knight,
                 "king": king,
                 "queen": queen}

    functions[obj.name](chessboard)
    if obj.name != "pawn" and obj.name != "king":
        obj.attack_moves = obj.moves.copy()


def update_coordinates():
    list_of_coordinates.clear()
    for fg in list_of_figures:
        list_of_coordinates.append(fg.current_position)
        rules(fg)


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
                            if fig.current_position == coordinates:
                                figure = fig
                                active_fig = True
                                break
                    else:
                        # if figure.can_move(coordinates):
                        #     for fig in list_of_figures:
                        #         if
                            figure.do_move(coordinates)
                        active_fig = False
                    update_coordinates()
