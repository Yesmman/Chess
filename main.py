import tkinter as tk
import pathlib

window = tk.Tk()

window.wm_minsize(800, 800)

height = window.winfo_reqheight() * 3.5
width = window.winfo_reqwidth() * 3.5

print(height, width)
canvas = tk.Canvas(width=700, height=700)
second_canvas = tk.Canvas(width=700, height=700)
canvas.pack()
second_canvas.pack()
list_of_paths = []
list_of_images = []
list_of_rect = []
for path in pathlib.Path().glob(pattern="*.png"):
    list_of_paths.append(path)
dict_color = {
    True: "LightBlue1",
    False: "SkyBlue1"
}


def draw_board():
    start_x = 3
    start_y = 10
    end_x = height / 8
    end_y = width / 8

    rect_width = width / 8
    rect_height = height / 8
    k = True
    for i in range(8):
        for j in range(8):
            canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=dict_color[j % 2 == k])
            list_of_rect.append((start_x, start_y, end_x, end_y))
            start_x = end_x
            end_x = start_x + rect_width
        k = not k
        start_x = 3
        end_x = height / 8
        start_y += rect_height - 10
        end_y += rect_height - 10


def im(file, x, y):
    global start
    global step
    image = tk.PhotoImage(file=file)
    list_of_images.append(image)
    canvas.create_image(x, y, image=list_of_images[-1])
    start += 2 * step


start = 45
step = 43.8

end_pos = 595


def draw_figures(mode):
    global start
    for i in range(8):
        if i == 0:
            im("rook_black.png", start, 50)
            im("knight_black.png", start, 50)
            im("bishop_black.png", start, 50)
            im("queen_black.png", start, 50)
            im("king_black.png", start, 50)
            im("bishop_black.png", start, 50)
            im("knight_black.png", start, 50)
            im("rook_black.png", start, 50)

        elif i == 1:

            for j in range(8):
                im("pawn_black.png", start, 130)
        elif i == 6:
            for j in range(8):
                im("pawn_white.png", start, 517)
        elif i == 7:
            im("rook_white.png", start, end_pos)
            im("knight_white.png", start, end_pos)
            im("bishop_white.png.", start, end_pos)
            im("queen_white.png", start, end_pos)
            im("king_white.png", start, end_pos)
            im("bishop_white.png", start, end_pos)
            im("knight_white.png", start, end_pos)
            im("rook_white.png", start, end_pos)
        start = 45


draw_board()
draw_figures(2)


def left_click(event):
    canvas.create_rectangle(*(list_of_rect[2]), fill="red")
    im("bishop_black.png", list_of_rect[2][0] + width / 16, list_of_rect[2][1] + height / 16)


def right_click(event):
    canvas.
    canvas.create_rectangle(*(list_of_rect[5]), fill="white")
    im("bishop_black.png", list_of_rect[5][0] + width / 16, list_of_rect[5][1] + height / 16)


window.bind("<Button-1>", left_click)
window.bind("<Button-2>", right_click)
window.mainloop()
