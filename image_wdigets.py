import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *

class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, import_func):
        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=1, sticky="nsew")  # Placed at the bottom
        self.import_func = import_func

        ctk.CTkLabel(self, text='Import Image', font=('Arial', 30)).pack(padx=10, pady=10)

        ctk.CTkButton(self, fg_color=BLUE, text='open image', command=self.open_dialog).pack(expand=True, pady=20)

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief="ridge")
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10, rowspan=3)  # Takes up a third of the window
        self.bind("<Configure>", resize_image)

class CloseOutput(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent,
            command=close_func,
            text="X",
            text_color=WHITE,
            fg_color='transparent',
            width=40, height=40,
            corner_radius=0,
            hover_color=CLOSE_RED,
        )
        self.place(relx=0.99, rely=0.01, anchor="ne")
