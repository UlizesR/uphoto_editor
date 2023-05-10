import customtkinter as ctk
from image_wdigets import *
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from menu import Menu

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.geometry('1000x600')
        self.title('UPhoto Editor')
        self.minsize(800, 500)
        self.init_parameters()
        self.configure_layout()

        self.image_import = ImageImport(self, self.import_image)
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

        combined_vars = list(self.pos_var.values()) + list(self.color_vars.values()) + list(self.effect_vars.values())
        for var in combined_vars:
            var.trace('w', self.manipulate_image)

    def configure_layout(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

    def manipulate_image(self, *args):
        self.image = self.original
        self.apply_transformations()
        self.place_image()

    def apply_transformations(self):
        self.apply_position_transformations()
        self.apply_color_transformations()
        self.apply_effect_transformations()

    def apply_position_transformations(self):
        if self.pos_var['rotate'].get() != ROTATE_DEFAULT:
            self.image = self.image.rotate(self.pos_var['rotate'].get())

        if self.pos_var['zoom'].get() != ZOOM_DEFAULT:
            self.image = ImageOps.crop(self.image, border=self.pos_var['zoom'].get())

        flip_option = self.pos_var['flip'].get()
        if flip_option != FLIP_OPTIONS[0]:
            if flip_option in (FLIP_OPTIONS[1], FLIP_OPTIONS[3]):
                self.image = ImageOps.mirror(self.image)
            if flip_option in (FLIP_OPTIONS[2], FLIP_OPTIONS[3]):
                self.image = ImageOps.flip(self.image)

    def apply_color_transformations(self):
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT or self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image)
            self.image = brightness_enhancer.enhance(self.color_vars['brightness'].get()) 
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['vibrance'].get())

        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)

        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)

    def apply_effect_transformations(self):
        blur, contrast, effect = self.effect_vars['blur'].get(), self.effect_vars['contrast'].get(), self.effect_vars['effect'].get()
        if blur != BLUR_DEFAULT or contrast != CONTRAS_DEFAULT or effect != EFFECT_OPTIONS[0]:
            self.image = self.image.filter(ImageFilter.GaussianBlur(blur))
            self.image = self.image.filter(ImageFilter.UnsharpMask(contrast))

        match effect:
            case 'Emboss': self.image = self.image.filter(ImageFilter.EMBOSS)
            case 'Find edges': self.image = self.image.filter(ImageFilter.FIND_EDGES)
            case 'Contour': self.image = self.image.filter(ImageFilter.CONTOUR)
            case 'Edge enhance': self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)

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
        canvas_ratio = event.width / event.height

        self.canvas_width = event.width
        self.canvas_height = event.height

        if canvas_ratio > self.image_ratio: 
            self.image_height = event.height
            self.image_width = int(self.image_height * self.image_ratio)
        else: 
            self.image_width = event.width
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def place_image(self):
        self.image_output.delete("all")
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

    def export_image(self, name, file, path):
        export_string = f'{path}/{name}.{file}'
        self.image.save(export_string)

App()