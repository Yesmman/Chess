class Figure:
    def __init__(self, name, color="white"):
        self.start_position = (0, 0)
        self.current_position = self.start_position
        self.color = color
        self.move_is_enable = True
        self.name = name
        self.image = ""
        self.set_image()
        self.moves = []
        self.attack_moves = []

    def block_move(self):
        self.move_is_enable = False

    def unblock_move(self):
        self.move_is_enable = True

    def set_image(self):
        self.image = f"{self.name}_{self.color}.png"

    def do_move(self, position):
        self.current_position = position

    def can_move(self, position):
        if position in self.moves:
            return True

    def can_attack(self, position):
        if position in self.attack_moves:
            return True

    def __repr__(self):
        return self.name
