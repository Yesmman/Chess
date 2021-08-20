import socket
import pickle
import threading as tr
from Figures import Net

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('', 0))

opponent_figures = []
my_figures = []


def get_chess():
    global opponent_figures
    while True:
        try:
            data = client.recv(1024)
            opponent_figures = pickle.loads(data)
        except ConnectionError:
            pass


thread = tr.Thread(target=get_chess, daemon=True)


def send_chess():
    client.sendto(pickle.dumps(my_figures), (Net.host, Net.port))
