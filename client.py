import socket
import pickle
import threading as tr
from Figures import Net


def create_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('', 0))
    return client


opponent_figures = []
my_figures = []


def get_chess(figures, move):
    while True:
        try:
            data = get_data()
            pickled = pickle.loads(data)
            figures = pickled["figured"]
            move = pickled["move"]
        except ConnectionError:
            pass


thread = tr.Thread(target=get_chess, daemon=True)


def get_data(from_):
    return from_.recv(1024)


def pick_data(figures, move):
    data_to_send = {
        "move": move,
        "figures": figures
    }
    return data_to_send


def send_to(from_, to, data):
    from_.sendto(pickle.dumps(data), to)
