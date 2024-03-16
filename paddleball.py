import sys
from tkinter import *
import random
import time


class Ball:

    def __init__(self, canvas, paddle, color, points_text):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 20, 20, fill=color)
        self.canvas.move(self.id, 245, 100)
        self.points = 0
        self.points_text = points_text
        # starts = [i for i in range(-3, 4)]
        # random.shuffle(starts)
        # self.x = starts[0]
        self.x = 1
        self.y = -1
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.hit_bottom = False

    def hit_paddle(self, pos):
        global score
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if paddle_pos[1] <= pos[3] <= paddle_pos[3]:
                self.points += 1
                score = self.points
                self.canvas.itemconfig(points_text, text=f'Очки: {self.points}')
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos):
            self.y = -1
        if pos[0] <= 0:
            self.x = 1
        if pos[2] >= self.canvas_width:
            self.x = -1


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, event):
        self.x = -1

    def turn_right(self, event):
        self.x = 1


if __name__ == '__main__':

    def start_game(event):

        canvas.itemconfig(start_text, state='hidden')
        canvas.itemconfig(points_text, state='normal')
        tk.update()
        while 1:
            if not ball.hit_bottom:
                ball.draw()
                paddle.draw()
            else:
                canvas.itemconfig(points_text, state='hidden')
                if score == 1:
                    score_text = 'очко'
                elif 2 <= score <= 4:
                    score_text = 'очка'
                elif 5 <= score <= 20:
                    score_text = 'очков'
                elif 1 <= int(str(score)[-1:]) <= 4:
                    score_text = 'очка'
                else:
                    score_text = 'очков'
                canvas.create_text(250, 350,
                                   text=f'Игра окончена. Вы набрали {score} {score_text}!', font=('Arial', -18))
                tk.update()
                time.sleep(5)
                sys.exit()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.005)


    score = 0

    tk = Tk()
    tk.title("Прыг-скок")
    tk.resizable(False, False)
    tk.wm_attributes("-topmost", 1)
    width = 500
    height = 400
    desktop_width = (tk.winfo_screenwidth() - width) // 2
    desktop_height = (tk.winfo_screenheight() - height) // 2
    tk.geometry(f'{width}x{height}+{desktop_width}+{desktop_height}')
    canvas = Canvas(tk, width=width, height=height, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()

    start_text = canvas.create_text(250, 350, text='Нажмите "Enter" чтобы запустить игру',
                                    font=('Arial', -18))
    points_text = canvas.create_text(250, 350, text='Очки: 0', font=('Arial', -18))
    canvas.itemconfig(points_text, state='hidden')
    tk.update()

    paddle = Paddle(canvas, 'blue')
    ball = Ball(canvas, paddle, 'red', points_text)

    canvas.bind_all('<Return>', start_game)
    mainloop()
