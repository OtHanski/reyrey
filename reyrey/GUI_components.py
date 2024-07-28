from copy import deepcopy
import tkinter as tk
from tkinter import ttk

class OpticalLine:
    """tkinter widget for a single optical line"""
    def __init__(self, parent):
        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=5)

        self.add_button = ttk.Button(button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.showhide_button = ttk.Button(button_frame, text="Show/Hide", command=self.showhide)
        self.showhide_button.pack(side=tk.LEFT, padx=5)

        self.componentframe = ttk.LabelFrame(parent, text="Optical Line", relief=tk.RIDGE)
        self.componentframe.pack(pady=5, fill=tk.X)
    
    