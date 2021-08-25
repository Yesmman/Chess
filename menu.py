import pygame_menu
from pygame_menu.examples import create_example_window
from functools import partial
import threading as tr
from Figures import Server


def start(menu: pygame_menu.Menu):
    from help import game
    menu.close()
    menu.disable()
    game()


def serv(server):
    while True:
        server.get_data()
        server.send_data(server.data)


def start_server():
    server = Server()
    thread = tr.Thread(target=partial(serv, server), daemon=True)
    try:
        thread.start()
    except OSError:
        print("Is already started")


def main_menu():
    surface = create_example_window(title="Menu",
                                    window_size=(800, 800))

    menu = pygame_menu.Menu(
        height=400,
        width=400,
        title="Main menu"
    )

    menu.add.button("Start", partial(start, menu))
    menu.add.button("Start server", start_server)
    menu.mainloop(surface)


main_menu()
