from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from raytracing.matrices import matrixdicts, ringCavity, linCavity

class LineParameter:
    """tkinter widget for a single line parameter"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Parameter Set", relief=tk.RIDGE).grid(row=0, column=0, pady=5, fill=tk.X)

        self.combo_vals = [key for (key,value) in matrixdicts.items()]
        self.component = ttk.Combobox(self.frame, values=self.combo_vals).grid(row=0, column=0, padx=5)

        self.remove_button = ttk.Button(self.frame, text="Remove", command=self.remove).grid(row=0, column=1, padx=5)

        self.fields = {}

    def remove(self):
        self.frame.destroy()

    def get_function(self):
        return self.component.get()

class OpticalLine:
    """tkinter widget for a single optical line"""
    def __init__(self, parent):
        self.button_frame = ttk.Frame(parent)
        self.button_frame.pack(pady=5, fill=tk.X)

        self.name = tk.StringVar(value = "New Optical Line")
        self.namefield = ttk.Entry(self.button_frame, textvariable=self.name)
        self.namefield.grid(row=0, column=0, padx=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.grid(row=0, column=1, padx=5)

        self.showhide_button = ttk.Button(self.button_frame, text="Show/Hide", command=self.showhide)
        self.showhide_button.grid(row=0, column=2, padx=5)
        
        # Add ver and hor plot tickboxes
        self.ver = tk.IntVar()
        self.ver_check = ttk.Checkbutton(self.button_frame, text="Ver", variable=self.ver)
        self.ver_check.grid(row=1, column=0, padx=5)
        self.hor = tk.IntVar()
        self.hor_check = ttk.Checkbutton(self.button_frame, text="Horizontal", variable=self.hor)
        self.hor_check.grid(row=1, column=1, padx=5)

        self.componentframe = ttk.LabelFrame(parent, text="Optical Line", relief=tk.RIDGE)
        self.componentframe.pack(pady=5, fill=tk.X)

    def add_parameter(self):
        pass
    
    def showhide(self):
        pass

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    optical_line = OpticalLine(root)
    root.mainloop()

if __name__ == "__main__":
    test()
    
    