mass = [i for i in range(64)]

start = 0
end = 8
for k in range(8):
    print(mass[start:end])
    start += 8
    end += 8


class cell:
    def __init__(self, number):
        self.number = number
        self.raw = self.get_raw()
        self.col = self.get_col()
        print(self.__repr__())

    def get_raw(self):
        return self.number // 8

    def get_col(self):
        return self.number % 8

    def __repr__(self):
        return f"{self.number=}, {self.raw=}, {self.col=}"


l = [1, 2, 3, 4, 5]
l2 = ["a", "b", "c", "d", "e"]

for number, liter in zip(l, l2):
    print(number, liter)
