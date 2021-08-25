from pygame import Rect
import socket
import pickle


class Figure:

    def __init__(self, name, reverse=False):
        self.start_position = (0, 0)
        self.current_position = self.start_position
        self.color = "white"

        self.name = name
        self.image = ""
        self.set_image(reverse)
        self.moves = []
        self.attack_moves = []
        self.under_check = False
        self.prev_move = ()
        self.s = ()

        self.did_move = False
        self.right_roque_move = ()
        self.left_roque_move = ()
        self.left_figure = None
        self.right_figure = None

    def do_left_roque(self):
        self.do_move(self.left_roque_move)
        self.did_move = True

    def do_right_roque(self):
        self.do_move(self.right_roque_move)
        self.did_move = True

    def check_first_move(self):
        return self.did_move

    def do_first_move(self):
        self.did_move = True

    def set_image(self, reverse):
        reversed_ = {
            "black": "white",
            "white": "black"
        }
        if reverse:
            self.image = f"{self.name}_{reversed_[self.color]}.png"
        else:
            self.image = f"{self.name}_{self.color}.png"

    def do_move(self, position):
        self.prev_move = self.current_position
        self.current_position = position

    def can_move(self, position):
        if position in self.moves:
            return True

    def can_attack(self, position):
        if position in self.attack_moves:
            return True

    def cancel_move(self):
        self.current_position = self.prev_move

    def __repr__(self):
        return self.name


class Cells(Rect):
    def __init__(self, rect):
        super().__init__(rect)

        self.standard_color = "red"
        self.color = self.standard_color
        self.is_active = False
        self.under_check = False
        self.to_check = False


class Net:
    host = '127.0.0.1'
    port = 65432


class Client:
    def __init__(self):
        self.client = self.create_client()

    @staticmethod
    def create_client():
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.bind(('', 0))
        return client

    def get_chess(self):
        try:
            data = self.client.recv(10240)

            pickled = pickle.loads(data)

            return pickled
        except ConnectionError:
            print("Error")

    def send_data(self, data, to):
        pickled = pickle.dumps(data)

        self.client.sendto(pickled, to)


class Server:
    def __init__(self):
        self.server = self.start_server()
        self.data = bytes(1)
        self.addresses = []
        self.current_address = None
        self.choice = {
            1: "white",
            2: "black"
        }
        self.count = 0

    @staticmethod
    def start_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("0.0.0.0", Net.port))
        return server

    def send_data(self, data):
        for address in self.addresses:
            if address != self.current_address and data is not None and type(data) == bytes:
                self.server.sendto(data, address)

    def get_data(self):
        self.data, address = self.server.recvfrom(10240)
        if address not in self.addresses:
            self.addresses.append(address)
            self.count += 1
            self.data = self.choice[self.count]

            self.send_data(pickle.dumps(self.data))
        self.current_address = address
