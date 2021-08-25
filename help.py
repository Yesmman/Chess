import pygame
import pathlib
from Figures import Figure, Cells, Client, Server, Net
from functools import partial
import threading as tr
import numpy as np


list_of_figures = []

i_got_figures = False
i_send_figures = False

pawns = []
rooks = []
knights = []
bishops = []
kings = []
queens = []
cells = []
my_king: Figure
my_figures = []
opponent_figures = []

your_move = True
enemy_move = False
counter_move = 0
position_to_delete = ()
images = {}
screen: pygame.Surface



def convert(list_: list):
    for i in range(len(list_)):
        x = list_[i].current_position[0]
        y = list_[i].current_position[1]
        y = 660 - y
        x = 760 - x
        new = (x, y)
        list_[i].current_position = new
        list_[i].color = "black"
    return list_


def convert_position(pos: tuple):
    if len(pos) != 0:
        x = pos[0]
        y = pos[1]
        x = 760 - x
        y = 660 - y
        return (x, y)
    return ()


def get_chess(client):
    global opponent_figures, your_move, i_got_figures, your_move, position_to_delete
    while True:
        data = client.get_chess()
        opponent_figures = convert(data["figures"])
        your_move = not data["move"]
        i_got_figures = data["reset"]
        # your_move = data["reset"]
        position_to_delete = convert_position(data["position"])


def create_chess_board():
    chessboard_list = []
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
    return chessboard


def create_figures(reverse):
    global my_figures
    for index in range(8):
        pawns.append(Figure("pawn", reverse))
    for index in range(2):
        knights.append(Figure("knight", reverse))
        rooks.append(Figure("rook", reverse))
        bishops.append(Figure("bishop", reverse))
    kings.append(Figure("king", reverse))
    queens.append(Figure("queen", reverse))
    my_figures = pawns + knights + rooks + bishops + kings + queens


def set_start_position(chessboard):
    start_index = 0
    for index in range(len(pawns)):
        pawns[index].start_position = chessboard[6][start_index]
        start_index += 1

    start_index = 0

    for index in range(len(rooks)):
        rooks[index].start_position = chessboard[7][start_index]
        start_index += 7

    start_index = 2

    for index in range(len(bishops)):
        bishops[index].start_position = chessboard[7][start_index]
        start_index += 3

    start_index = 1

    for index in range(len(knights)):
        knights[index].start_position = chessboard[7][start_index]
        start_index += 5

    kings[0].start_position = chessboard[7][4]
    queens[0].start_position = chessboard[7][3]


def cells_chess_board(chessboard):
    dict_color = {
        True: "White",
        False: "Pink"
    }

    k = True
    counter = 0
    for index in range(len(chessboard)):
        for x, y in chessboard[index]:
            counter += 1
            rect = pygame.Rect(x, y, 80, 80)

            cell = Cells(rect)
            cell.standard_color = dict_color[k]
            k = not k
            cell.color = cell.standard_color
            if counter % 8 == 0:
                counter = 0
                k = not k
            cells.append(cell)


def draw_chess_board(screen):
    for cell in cells:
        if cell.is_active:
            pygame.draw.rect(screen, color="lightblue", rect=cell)
        else:
            pygame.draw.rect(screen, color=cell.color, rect=cell)
        if cell.under_check:
            pygame.draw.rect(screen, color="red", rect=cell)
        if cell.to_check:
            pygame.draw.rect(screen, color="red", rect=cell)


def add_images(list_):
    for f in list_:
        images[f] = pygame.image.load(f.image)


def de_highlight(list_):
    for cell in list_:
        cell.is_active = False


def update_figures(list_):
    for f in list_:
        f.current_position = tuple(f.start_position)


def check_king_under_attack(pos):
    for f in opponent_figures:
        for x_y in f.attack_moves:
            if tuple(x_y) == pos:
                print(f)
                return True
    return False


def check_king_under_attack_(pos):
    for f in opponent_figures:
        for x_y in f.attack_moves:
            if tuple(x_y) == pos:
                print(f)
                return True, f
    return False, 0


def get_king():
    return kings[0]


def get_queen():
    return queens[0]


def check_check(king: Figure):
    global counter_move
    print(counter_move)
    bool_, f = check_king_under_attack_(king.current_position)
    if bool_:
        for cell in cells:
            if (cell.x, cell.y) == king.current_position:
                cell.under_check = True
                if counter_move == 0 and f.name != "king":
                    counter_move += 1
                    pos = f.current_position
                    for c in cells:
                        if (c.x, c.y) == pos:
                            c.to_check = True
                            break
                break


def rules(obj: Figure, chessboard):
    global list_of_figures, my_king
    obj.moves.clear()
    list_of_figures = my_figures + opponent_figures

    pawn_dict = {
        "black": 1,
        "white": -1
    }

    def get_index():
        for i_ in range(8):
            for j_ in range(8):
                tup = tuple(chessboard[i_][j_])
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
        if obj.current_position[1] == 50:
            global screen
            ims = ["queen_white.png",
                   "rook_white.png",
                   "bishop_white.png",
                   "knight_white.png"]

            real_images = []
            for path in ims:
                real_images.append(pygame.image.load(path))
            samples = []
            selecting = True
            y = 50
            x = 20
            for i in range(4):
                samples.append(pygame.Rect(x, y, 80, 80))
                y += 80

            while selecting:
                for image in zip(samples, real_images):
                    pygame.draw.rect(screen, "green", image[0])
                    screen.blit(image[1], image[0])

                pygame.display.flip()
                position = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(len(ims)):
                            if samples[i].collidepoint(position):
                                if i == 0:
                                    obj.name = "queen"
                                    selecting = False
                                elif i == 1:
                                    obj.name = "rook"
                                    selecting = False
                                elif i == 2:
                                    obj.name = "bishop"
                                    selecting = False
                                elif i == 3:
                                    obj.name = "knight"
                                    selecting = False

                obj.set_image(False)
                images[obj] = pygame.image.load(obj.image)

        cant_move = False
        index = get_index()

        pos = tuple(board[index[0] + pawn_dict[obj.color], index[1]])
        if not on_way(pos):
            obj.moves.append(pos)
        else:
            cant_move = True
        if tuple(obj.current_position) == tuple(obj.start_position):
            pos = tuple(board[index[0] + 2 * pawn_dict[obj.color], index[1]])
            if not on_way(pos) and not cant_move:
                obj.moves.append(pos)
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

    if not my_king.did_move:
        for r in my_figures:
            if r.name == "rook" and not r.did_move:
                if obj.current_position in r.moves:
                    if r.current_position == tuple(chessboard[7][0]):
                        king_roque_left = (r.current_position[0] + 160, r.current_position[1])
                        # obj.moves.append(king_roque_left)
                        obj.left_roque_move = king_roque_left
                        r.right_roque_move = (king_roque_left[0] + 80, king_roque_left[1])
                        obj.left_figure = r
                    elif r.current_position == tuple(chessboard[7][7]):
                        king_roque_right = (r.current_position[0] - 80, r.current_position[1])
                        # obj.moves.append(king_roque_right)
                        obj.right_roque_move = king_roque_right
                        r.left_roque_move = (king_roque_right[0] - 80, king_roque_right[1])
                        obj.right_figure = r


def update_coordinates(chessboard):
    for fg in list_of_figures:
        rules(fg, chessboard)


def pick_data(pos=()):
    # global your_move
    d = {
        "figures": my_figures.copy(),
        "move": your_move,
        "reset": True,
        "position": pos
    }
    return d


def game():
    global list_of_figures, pawns, rooks, knights, kings, bishops, queens, cells, opponent_figures, your_move, \
        i_got_figures, i_send_figures, my_king, screen, counter_move
    list_of_paths = []

    client = Client()
    config = Net.host, Net.port

    client.send_data(None, config)
    i_am_black = False
    color = client.get_chess()
    if color == "black":
        i_am_black = True
        your_move = False

    for path in pathlib.Path().glob(pattern="*.png"):
        list_of_paths.append(path)
    width = 800
    height = 800

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Cheese")

    chessboard = create_chess_board()

    thread = tr.Thread(target=partial(get_chess, client), daemon=True)

    cells_chess_board(chessboard)
    create_figures(i_am_black)
    set_start_position(chessboard)
    my_king = get_king()
    oh_no_my_queen = get_queen()
    if color == "black":
        my_king.start_position, oh_no_my_queen.start_position = oh_no_my_queen.start_position, my_king.start_position

    list_of_figures = opponent_figures + my_figures
    add_images(list_of_figures)

    update_figures(list_of_figures)
    update_coordinates(chessboard)

    running = True
    active_fig = False
    figure = None

    thread.start()
    yes = False
    while running:

        screen.fill("black")
        draw_chess_board(screen)
        i = 0
        if i_got_figures:
            if position_to_delete != ():
                for f in my_figures:
                    if f.current_position == position_to_delete:
                        my_figures.remove(f)
                        break

            list_of_figures = my_figures.copy() + opponent_figures.copy()
            images.clear()

            for fig in list_of_figures:
                fig.set_image(i_am_black)
            add_images(list_of_figures)

            i_got_figures = False
            update_coordinates(chessboard)

        for fig in list_of_figures:
            screen.blit(images[fig], fig.current_position)
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
                        if your_move:
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
                                        popped = opponent_figures.pop(index)
                                        if figure.can_move(coordinates):
                                            figure.do_move(coordinates)
                                            update_coordinates(chessboard)

                                            under_attack = check_king_under_attack(tuple(my_king.current_position))
                                            if under_attack:
                                                figure.cancel_move()
                                                opponent_figures.insert(index, popped)
                                                update_coordinates(chessboard)

                                                break
                                            else:
                                                counter_move += 1
                                                if counter_move == 2:
                                                    your_move = False
                                                    counter_move = 0
                                                data = pick_data(coordinates)
                                                client.send_data(data, config)
                                                # your_move = False

                                        elif figure.name == "pawn":
                                            figure.do_move(coordinates)
                                            update_coordinates(chessboard)

                                            under_attack = check_king_under_attack(tuple(my_king.current_position))
                                            if under_attack:
                                                figure.cancel_move()
                                                opponent_figures.insert(index, popped)
                                                update_coordinates(chessboard)

                                                break

                                            else:
                                                counter_move += 1
                                                if counter_move == 2:
                                                    your_move = False
                                                    counter_move = 0
                                                data = pick_data(coordinates)
                                                client.send_data(data, config)
                                                # your_move = False

                                        break
                                    elif coordinates == tuple(f.current_position):
                                        break
                                else:
                                    ok = True
                                    for f in my_figures:
                                        if f.current_position == coordinates and figure != f:
                                            ok = False
                                    if ok:
                                        if figure.name == "king" and not figure.did_move:
                                            if coordinates == figure.right_roque_move:

                                                figure.do_right_roque()
                                                figure.right_figure.do_left_roque()
                                                figure.did_move = True
                                                counter_move += 1
                                                if counter_move == 2:
                                                    your_move = False
                                                    counter_move = 0
                                                data = pick_data(coordinates)
                                                client.send_data(data, config)
                                                # your_move = False
                                                break
                                            elif coordinates == figure.left_roque_move:
                                                figure.do_left_roque()
                                                figure.left_figure.do_right_roque()
                                                figure.did_move = True
                                                counter_move += 1
                                                if counter_move == 2:
                                                    your_move = False
                                                    counter_move = 0
                                                data = pick_data(coordinates)
                                                client.send_data(data, config)
                                                # your_move = False
                                                break
                                        if figure.can_move(coordinates):
                                            figure.do_move(coordinates)
                                            update_coordinates(chessboard)

                                            under_attack = check_king_under_attack(tuple(my_king.current_position))
                                            if under_attack:
                                                figure.cancel_move()
                                                update_coordinates(chessboard)
                                                active_fig = False
                                                break

                                            else:
                                                figure.did_move = True
                                                counter_move += 1
                                                if counter_move == 2:
                                                    your_move = False
                                                    counter_move = 0
                                                data = pick_data()

                                                client.send_data(data, config)
                                                # your_move = False

                                active_fig = False
                            update_coordinates(chessboard)
                    for cell in cells:
                        cell.under_check = False
                        cell.to_check = False

                    check_check(my_king)
