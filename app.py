import customtkinter as ctk
from image_wdigets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from menu import Menu

class App(ctk.CTk):
    def __init__(self):
        # Setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry('1000x600')
        self.title('UPhoto Editor')
        self.minsize(800, 500)
         # parameters
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0

        # widgets
        self.image_import = ImageImport(self, self.import_image)

        # run
        self.mainloop()

    def init_parameters(self):
        self.pos_var = {
            'rotate': ctk.DoubleVar(value=ROTATE_DEFAULT),
            'zoom': ctk.DoubleVar(value=ZOOM_DEFAULT),
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0]),
        }
        self.color_vars = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
            'grayscale': ctk.DoubleVar(value=GRAYSCALE_DEFAULT),
            'invert': ctk.DoubleVar(value=INVERT_DEFAULT), 
        }
        self.effect_vars = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.DoubleVar(value=CONTRAS_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0]),
        }

        # tracing
        combined_vars = list(self.pos_var.values()) + list(self.color_vars.values()) + list(self.effect_vars.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        self.image = self.original

        # rotate
        if self.pos_var['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_var['rotate'].get())
        # zoom
        if self.pos_var['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(image = self.image, border = self.pos_var['zoom'].get())
        # flip
        if self.pos_var['flip'].get() != FLIP_OPTIONS[0]:
            if self.pos_var['flip'].get() == FLIP_OPTIONS[1]: 
                self.image = ImageOps.mirror(self.image)
            if self.pos_var['flip'].get() == FLIP_OPTIONS[2]:
                self.image = ImageOps.flip(self.image)
            if self.pos_var['flip'].get() == FLIP_OPTIONS[3]:
                self.image = ImageOps.mirror(self.image)
                self.image = ImageOps.flip(self.image)

        # brightness & vibrance
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT or self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.color_vars['brightness'].get()) 
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['vibrance'].get())

        # grayscale & invert
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)
        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

        # blur & contrast
        if self.effect_vars['blur'].get() != BLUR_DEFAULT or self.effect_vars['contrast'].get() != CONTRAS_DEFAULT or self.effect_vars['effect'].get() != EFFECT_OPTIONS[0]:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
            self.image = self.image.filter(ImageFilter.UnsharpMask(self.effect_vars['contrast'].get()))
        match self.effect_vars['effect'].get():
            case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'Find edges': self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case 'Contour': self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'Edge enhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)


        self.place_image() 

    def import_image(self, path):
        self.original = Image.open(path)
        self.image = self.original
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output = ImageOutput(self, self.resize_image)
        self.close_output = CloseOutput(self, self.close_edit)
        self.menu = Menu(self, self.pos_var, self.color_vars, self.effect_vars, self.export_image)

    def close_edit(self):
        self.image_output.grid_forget()
        self.close_output.grid_forget()
        self.menu.grid_forget()
        self.image_import = ImageImport(self, self.import_image)

    def resize_image(self, event):

        # current canvas ratio
        canvas_ratio = event.width / event.height

        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        # resize
        if canvas_ratio > self.image_ratio: # canvas is wider than image 
            self.image_height = event.height
            self.image_width = int(self.image_height * self.image_ratio)
        else: # canvas is taller than image
            self.image_width = event.width
            self.image_height = int(self.image_width / self.image_ratio)

        # place image
        self.place_image()

    def place_image(self):
        self.image_output.delete("all")
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image = self.image_tk)

    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)

App()