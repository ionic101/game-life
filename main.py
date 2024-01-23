import tkinter as tk
from tkinter import ttk
from game import GameLife


class Setting:
    def __init__(self, StartWindowInstance, root, text, max_value, step):
        self.StartWindowInstance = StartWindowInstance
        self.root = root
        self.text = text
        self.max_value = max_value

        self.step = step
        self.variable = tk.IntVar()
        self.variable.set(0)

    def update_max_value(self, new_max_value):
        self.max_value = new_max_value
        self.setting_scale.configure(to=new_max_value)
        self.variable.set(new_max_value)

    def update_step(self, new_step):
        self.step = new_step

    def get_variable(self):
        return self.variable.get()

    def scale_change(self, value: float):

        def value_round(num, step):
            return min(self.max_value, (num // step + round(num % step / step)) * step)

        def change_max_value(max_value):
            SCREEN_WIDTH = self.StartWindowInstance.SCREEN_WIDTH
            SCREEN_HEIGHT = self.StartWindowInstance.SCREEN_HEIGHT
            new_step = max(1, max_value//100)
            self.StartWindowInstance.width_setting.update_max_value(SCREEN_WIDTH//max_value)
            self.StartWindowInstance.width_setting.update_step(new_step)
            self.StartWindowInstance.height_setting.update_max_value(SCREEN_HEIGHT//max_value)
            self.StartWindowInstance.height_setting.update_step(new_step)

        new_value = value_round(float(value), self.step)
        if self is self.StartWindowInstance.cell_setting:
            change_max_value(new_value)
        self.variable.set(new_value)
        self.StartWindowInstance.update_screen()

    def spawn_setting(self):
        setting_frame = tk.Frame(self.root)
        setting_label = tk.Label(setting_frame, text=self.text, font=('Robot', 16))
        self.setting_scale = ttk.Scale(
            setting_frame,
            orient=tk.HORIZONTAL,
            variable=self.variable,
            length=200,
            from_=self.step,
            to=self.max_value,
            command=self.scale_change)
        self.value_label = tk.Label(setting_frame, textvariable=self.variable)
        setting_label.grid(row=0, column=0)
        self.setting_scale.grid(row=0, column=1, padx=20)
        self.value_label.grid(row=1, column=1)
        setting_frame.pack(pady=5, anchor=tk.E)


class StartWindow:
    def __init__(self):
        self.create_window()
        self.get_system_settings()
        self.spawn_widgets()
        self.root.mainloop()

    def get_system_settings(self):
        self.SCREEN_WIDTH = self.root.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.root.winfo_screenheight()

    def spawn_title(self):
        title_label = tk.Label(text='Game Life', font=('Robot', 32))
        title_label.pack(pady=30)

    def spawn_setting(self, text, max_value, step):
        setting = Setting(self, self.settings_frame, text, max_value, step=step)
        setting.spawn_setting()
        return setting

    def spawn_screen_size(self):
        self.screen_size = tk.StringVar()
        screen_size_label = tk.Label(text='1920x1080', font=('Robot', 16), textvariable=self.screen_size)
        self.update_screen()
        screen_size_label.pack()

    def update_screen(self):
        self.SCALE, self.WIDTH, self.HEIGHT = map(lambda x: x.get_variable(), self.settings)
        self.screen_size.set(f'{self.SCALE*self.WIDTH}x{self.SCALE*self.HEIGHT}')

    def spawn_button(self):
        start_button = tk.Button(
            self.root,
            text='START GAME',
            font=('Robot', 16),
            width=20,
            height=2,
            borderwidth=0,
            bg='blue',
            fg='white',
            command=self.start_game
        )
        start_button.pack(pady=20)

    def spawn_widgets(self):
        self.spawn_title()

        self.settings_frame = tk.Frame(self.root)
        self.cell_setting = self.spawn_setting('Cell size', 100, step=5)
        self.width_setting = self.spawn_setting('Number of cells horizontally', self.SCREEN_WIDTH, step=10)
        self.height_setting = self.spawn_setting('Number of cells vertically', self.SCREEN_HEIGHT, step=10)
        self.settings = [
            self.cell_setting,
            self.width_setting,
            self.height_setting
            ]
        self.settings_frame.pack()

        self.spawn_screen_size()

        self.spawn_button()

    def create_window(self):
        self.root = tk.Tk()
        self.root.geometry(f'{800}x{500}')
        self.root.title('Game Life Settings')
        self.root.resizable(False, False)

    def start_game(self):
        self.root.destroy()
        GameLife(*map(lambda x: x.get_variable(), self.settings))


if __name__ == '__main__':
    StartWindow()
