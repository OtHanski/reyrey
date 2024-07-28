from copy import deepcopy
import tkinter as tk
from tkinter import ttk

class LineParameters:
    """tkinter widget for a single line parameter"""
    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text="Parameter Set", relief=tk.RIDGE).grid(row=0, column=0, pady=5, fill=tk.X)

        self.combo_vals = ["sine_wave", "cosine_wave"]
        self.function = ttk.Combobox(self.frame, values=self.combo_vals).grid(row=0, column=0, padx=5)

        self.remove_button = ttk.Button(self.frame, text="Remove", command=self.remove).grid(row=0, column=1, padx=5)

        self.fields = {}

    def remove(self):
        self.frame.destroy()

    def get_function(self):
        return self.function.get()

class OpticalLine:
    """tkinter widget for a single optical line"""
    def __init__(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=5)

        self.name = tk.StringVar()
        self.namefield = ttk.Entry(button_frame, textvariable=self.name)
        self.namefield.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.showhide_button = ttk.Button(button_frame, text="Show/Hide", command=self.showhide)
        self.showhide_button.pack(side=tk.LEFT, padx=5)

        self.componentframe = ttk.LabelFrame(parent, text="Optical Line", relief=tk.RIDGE)
        self.componentframe.pack(pady=5, fill=tk.X)


    
    