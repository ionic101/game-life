import tkinter as tk


class GameLife:
    def __init__(self, SCALE, WIDTH, HEIGHT):
        self.SCALE = SCALE
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.SCREEN_WIDTH = WIDTH*SCALE
        self.SCREEN_HEIGHT = HEIGHT*SCALE

        self.lifes = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

        self.create_window()

        self.root.mainloop()

    def create_window(self):
        self.root = tk.Tk()
        self.root.geometry(f'{self.SCREEN_WIDTH}x{self.SCREEN_HEIGHT}')
        self.root.title('Game Life')
        self.root.resizable(False, False)

        self.root.bind('<B1-Motion>', self.spawn)
        self.root.bind('<B3-Motion>', self.delete)
        self.root.bind('<Button-1>', self.spawn)
        self.root.bind('<Button-3>', self.delete)
        self.root.bind('<Return>', self.start_game)

        self.window = tk.Canvas(width=self.SCREEN_WIDTH, height=self.SCREEN_HEIGHT, bg='white')
        self.window.pack()

    def spawn(self, event):
        x, y = min(self.SCREEN_WIDTH, event.x), min(self.SCREEN_WIDTH, event.y)
        print(x, y )
        x //= self.SCALE
        y //= self.SCALE
        self.lifes[y][x] = 1
        x *= self.SCALE
        y *= self.SCALE
        self.window.create_rectangle(x, y, x+self.SCALE, y+self.SCALE, fill='black', outline='')

    def delete(self, event):
        x, y = min(self.SCREEN_WIDTH, event.x), min(self.SCREEN_WIDTH, event.y)
        x //= self.SCALE
        y //= self.SCALE
        self.lifes[y][x] = 0
        x *= self.SCALE
        y *= self.SCALE
        self.window.create_rectangle(x, y, x+self.SCALE, y+self.SCALE, fill='white', outline='')

    def find_near_alive(self, x, y):
        near_alive = 0
        for x_change in range(-1, 2):
            for y_change in range(-1, 2):
                if x_change == 0 and y_change == 0:
                    continue
                new_x = x + x_change
                new_y = y + y_change
                if new_x < 0 or new_y < 0 or new_x >= self.WIDTH or new_y >= self.HEIGHT:
                    continue
                near_alive += self.lifes[new_y][new_x]
        return near_alive

    def live(self, x, y, life):
        near_alive = self.find_near_alive(x, y)
        if life:
            return (near_alive in (2, 3))
        else:
            return (near_alive == 3)

    def draw(self, x, y):
        x *= self.SCALE
        y *= self.SCALE
        self.window.create_rectangle(x, y, x+self.SCALE, y+self.SCALE, fill='black', outline='')

    def update_screen(self, x, y):
        self.draw(0, 0)
        self.window.create_rectangle()
        self.update_game()

    def update_game(self):
        self.window.delete('all')
        new_lifes = [[0 for x in range(self.WIDTH)] for y in range(self.HEIGHT)]
        for y, line in enumerate(self.lifes):
            for x, life in enumerate(line):
                new_life = self.live(x, y, life)
                new_lifes[y][x] = int(new_life)
                if new_life:
                    self.draw(x, y)
        self.lifes = new_lifes
        self.root.after(100, self.update_game)

    def start_game(self, event):
        self.update_game()
