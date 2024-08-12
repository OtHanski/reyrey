import tkinter as tk
from tkinter import ttk

from tkinter import colorchooser

class PlotOptions:
    # Init either in given parentframe or if not given, new top level window
    def __init__(self, parent=None, plotoptions: dict = None):
        if parent is None:
            self.root = tk.Toplevel()
        else:
            self.root = parent
        self.root.title("Plot Options")
    
        if plotoptions is not None:
            self.plotoptions = plotoptions
        else:
            self.plotoptions = {
                "vertical": 1,
                "horizontal": 1,
                "color": "red"
            }

        ### COLOR PICKER ###
        # Square with current color
        self.colorframe = tk.Frame(self.root)
        self.colorframe.pack(pady=5)
        self.colorframe.pack_propagate(0)
        self.colorframe.config(width=50, height=50)
        self.colorframe.config(background=self.plotoptions["color"])
        # Button to open color picker
        self.colorbutton = ttk.Button(self.colorframe, text="Color", command=self.choose_color)
        self.colorbutton.pack(pady=5)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.plotoptions["color"] = color_code[1]
            self.colorframe.config(background=color_code[1])


def test():
    root = tk.Tk()
    app = PlotOptions(root)
    root.mainloop()

if __name__ == "__main__":
    test()