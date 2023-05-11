import customtkinter as ctk
from PIL import Image, ImageTk
from settings import *
import os
import warnings

class LandingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.grid(column=0, columnspan=3, row=0, sticky="nsew")

        self.image_original = Image.open(os.path.join("assets", "logo-nbg.png"))
        self.image_ratio = self.image_original.size[0] / self.image_original.size[1]

        self.canvas = ctk.CTkCanvas(self, bd=0, highlightthickness=0, relief="ridge", bg=BACKGROUND_COLOR)
        self.canvas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)  # Make the first column expandable
        self.grid_columnconfigure(1, weight=4)  # Make the second column expandable
        self.grid_columnconfigure(2, weight=1)  # Make the third column expandable
        self.grid_rowconfigure(0, weight=1)  # Make the first row expandable

        self.canvas.bind("<Configure>", self.resize_img)

    def resize_img(self, event):
        # Resize the image to fit the canvas
        self.new_width = event.width
        self.new_height = event.height
        resized_image = self.image_original.resize((self.new_width, self.new_height))
        resized_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor="nw", image=resized_tk)

        # Keep a reference to prevent the image from being garbage collected
        self.canvas.ctk_resized_image = resized_tk

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
