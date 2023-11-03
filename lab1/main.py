from tkinter import *
from tkinter import colorchooser
import colorsys
from math import floor

class ColorPicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Color Picker")
        self.color = None
        self.rgb_label = None
        self.cmyk_label = None
        self.hls_label = None
        self.create_widgets()

    def create_widgets(self):
        self.color_button = Button(self.master, text="Pick a Color", command=self.pick_color)
        self.color_button.pack(pady=10)

        self.rgb_label = Label(self.master, text="RGB: (0, 0, 0)")
        self.rgb_label.pack(pady=5)

        self.cmyk_label = Label(self.master, text="CMYK: (0, 0, 0, 100)")
        self.cmyk_label.pack(pady=5)

        self.hls_label = Label(self.master, text="HLS: (0, 0%, 0%)")
        self.hls_label.pack(pady=5)

        self.selected_color_label = Label(self.master, text="Selected Color: None", bd=1, relief=SUNKEN, anchor=W)
        self.selected_color_label.pack(side=BOTTOM, fill=X)

    def pick_color(self):
        color = colorchooser.askcolor()[0]
        if color is not None:
            self.color = tuple(map(floor, color))
            self.update_labels()
            self.selected_color_label.config(text=f"Selected Color: {self.rgb_to_hex(self.color)}", bg=self.rgb_to_hex(self.color))

    def update_labels(self):
        rgb = self.color
        cmyk = self.rgb_to_cmyk(rgb)
        hls = self.rgb_to_hls(rgb)
        self.rgb_label.config(text=f"RGB: {rgb}")
        self.cmyk_label.config(text=f"CMYK: {cmyk}")
        self.hls_label.config(text=f"HLS: {hls}")

    def rgb_to_cmyk(self, rgb):
        r, g, b = [x / 255 for x in rgb]
        k = 1 - max(r, g, b)
        if k == 1:
            c, m, y = 0, 0, 0
        else:
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        cmyk = tuple(map(lambda x: floor(x * 100), (c, m, y, k)))
        return cmyk

    def rgb_to_hls(self, rgb):
        r, g, b = [x / 255 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        hls = (floor(h * 360), floor(l * 100), floor(s * 100))
        return hls

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

root = Tk()
root.geometry("256x256")
color_picker = ColorPicker(root)
root.mainloop()