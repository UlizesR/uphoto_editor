import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *
from PIL import Image, ImageTk
import webbrowser
import os
import warnings

class LandingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.grid(column=0, columnspan=2, row=0, sticky="nsew")

        ctk.CTkLabel(self, text='URPhoto Editor', font=('Arial', 50)).pack(padx=10, pady=30)
        ctk.CTkLabel(self, text='A simple photo editor', font=('Arial', 20)).pack(padx=10, pady=10)

class LandingMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.grid(column=0, columnspan=1, row=0, sticky="nsew")

        image_path = os.path.join("assets", "settings.png")  # Construct the image path
        image = Image.open(image_path)  # Open the image
        image.thumbnail((20, 20))  # Scale the image to fit within 20x20 pixels
        ctk_image = ImageTk.PhotoImage(image)  # Convert PIL Image to CTkImage

        # Suppress warnings temporarily
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            button = ctk.CTkButton(self, text='', image=ctk_image, width=20, height=20)
        
        button.place(x=20, y=20)  # Position the button on the top left corner

        # Keep a reference to prevent the image from being garbage collected
        button.image = ctk_image
