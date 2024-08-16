"""Implements the PlotOptions class, a class to handle 
the plot options window for optical line plotting"""

import tkinter as tk
from tkinter import ttk

from tkinter import colorchooser

class PlotOptions:
    """PlotOptions, a class to handle the plot options window. UNFINISHED"""
    # Init either in given parentframe or if not given, new top level window
    def __init__(self, parent=None, plotoptions: dict = None):
        self.root = tk.Toplevel()
        self.root.geometry("250x150")
        self.root.title("Plot Options")
        self.root.attributes("-topmost", True)
        # Set on_closing to run when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.parent = parent

        if plotoptions is not None:
            self.plotoptions = plotoptions
        else:
            self.plotoptions = {
                    "hor": {"color": "red"},
                    "ver": {"color": "blue"}
                }
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        ### COLOR PICKER ###
        self.colorframes = {"hor": None, "ver": None}
        # Square with current color
        self.colorframes["hor"] = tk.Frame(self.frame)
        self.colorframes["hor"].grid(row=0, column=0, padx=5, pady=5)
        self.colorframes["hor"].config(width=25, height=25)
        self.colorframes["hor"].config(background=self.plotoptions["hor"]["color"])
        # Button to open color picker
        self.horcolorbutton = ttk.Button(self.frame,
                                         text="Hor color",
                                         command= lambda: self.choose_color("hor"))
        self.horcolorbutton.grid(row=0, column=1, padx=5, pady=5)

        # Same with vertical
        self.colorframes["ver"] = tk.Frame(self.frame)
        self.colorframes["ver"].grid(row=1, column=0, padx=5, pady=5)
        self.colorframes["ver"].config(width=25, height=25)
        self.colorframes["ver"].config(background=self.plotoptions["ver"]["color"])
        # Button to open color picker
        self.horcolorbutton = ttk.Button(self.frame,
                                         text="Ver color",
                                         command=lambda: self.choose_color("ver"))
        self.horcolorbutton.grid(row=1, column=1, padx=5, pady=5)

        ### OK and Cancel
        self.okbutton = ttk.Button(self.frame, text="OK", command=self.on_closing)
        self.okbutton.grid(row=2, column=0, padx=5, pady=5)
        self.cancelbutton = ttk.Button(self.frame, text="Cancel", command=self.cancel)

    def choose_color(self, horver):
        """Open a color picker dialog and set the color of the given line"""
        color_code = colorchooser.askcolor(title="Choose color")
        if color_code:
            self.plotoptions[horver]["color"] = color_code[1]
            self.colorframes[horver].config(background=color_code[1])

    def cancel(self):
        """Cancel the changes and close the window. TODO: Implement"""
        self.plotoptions = None
        self.on_closing()

    def on_closing(self):
        """Close the window and set the plotoptions in the parent window"""
        if hasattr(self.parent, "setplotoptions"):
            self.parent.setplotoptions(self.plotoptions)
        print(self.parent)
        # Remove reference to the window in the parent when closing.
        if self.parent is not None:
            self.parent.PlotOptWindow = None
        self.root.destroy()




def test():
    """Test function to run the PlotOptions window"""
    root = tk.Tk()
    app = PlotOptions(root)
    root.mainloop()
    print(app.plotoptions)

if __name__ == "__main__":
    test()
