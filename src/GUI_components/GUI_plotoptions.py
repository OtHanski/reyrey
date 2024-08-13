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
                "color": "red"
            }

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        ### COLOR PICKER ###
        # Square with current color
        self.colorframe = tk.Frame(self.frame)
        self.colorframe.grid(row=0, column=0, padx=5, pady=5)
        self.colorframe.config(width=25, height=25)
        self.colorframe.config(background=self.plotoptions["color"])
        # Button to open color picker
        self.colorbutton = ttk.Button(self.frame, text="Plot color", command=self.choose_color)
        self.colorbutton.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ### OK and Cancel
        self.okbutton = ttk.Button(self.frame, text="OK", command=self.on_closing)
        self.okbutton.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.cancelbutton = ttk.Button(self.frame, text="Cancel", command=self.cancel)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.plotoptions["color"] = color_code[1]
            self.colorframe.config(background=color_code[1])
    
    def cancel(self):
        self.plotoptions = None
        self.on_closing()

    def on_closing(self):
        self.root.destroy()




def test():
    root = tk.Tk()
    app = PlotOptions(root)
    root.mainloop()
    print(app.plotoptions)

if __name__ == "__main__":
    test()