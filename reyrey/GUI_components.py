"""
GUI component prototype dictionaries for dynamic UI handler
"""

from copy import deepcopy
import tkinter as tk
from tkinter import ttk

# Define the prototype dictionaries for the GUI components
def copy_prototype(prototype):
    return deepcopy(prototype)

def tk_var_type(type, val):
    if type == "string":
        return tk.StringVar(value=val)
    elif type == "double":
        return tk.DoubleVar(value=val)
    elif type == "int":
        return tk.IntVar(value=val)

def init_shared(parent_frame, ui_elements: dict):
    """Initialize the shared UI parameter components.
            parent_frame: ttk.Frame
                The parent frame to place the shared UI parameter components.
            ui_elements: dict
                The dictionary of UI elements to be initialized."""
        
    # Add the function dropdown and remove button in the first row
    ui_elements["shared"]["function"]["val"] = tk.StringVar(value = ui_elements["shared"]["function"]["val"][0])
    ui_elements["shared"]["function"]["elem"] = ttk.Combobox(parent_frame, textvariable=ui_elements["shared"]["function"]["val"])
    ui_elements["shared"]["function"]["elem"]['values'] = ui_elements["shared"]["function"]["values"]
    ui_elements["shared"]["function"]["elem"].current(ui_elements["shared"]["function"]["default"])  # Set default value
    ui_elements["shared"]["function"]["elem"].grid(row = ui_elements["shared"]["function"]["location"][0], 
                                                column = ui_elements["shared"]["function"]["location"][1], 
                                                padx = 5, pady = 5)
    #combobox_func should be an app update call
    ui_elements["shared"]["function"]["elem"].bind("<<ComboboxSelected>>", lambda e: ui_elements["shared"]["function"]["combobox_func"](parent_frame, ui_elements))
    
    ui_elements["shared"]["name"]["val"] = tk.StringVar(value = ui_elements["shared"]["name"]["val"][0])
    ui_elements["shared"]["name"]["elem"] = ttk.Entry(parent_frame, textvariable=ui_elements["shared"]["name"]["val"])
    ui_elements["shared"]["name"]["val"].set("New Parameter")
    ui_elements["shared"]["name"]["elem"].grid(row = ui_elements["shared"]["name"]["location"][0], 
                                                column = ui_elements["shared"]["name"]["location"][1], 
                                                padx = 5, pady = 5)
    
    ui_elements["shared"]["remove"]["elem"] = ttk.Button(parent_frame, text="Remove", command=lambda: ui_elements["shared"]["remove"]["func"](parent_frame))
    ui_elements["shared"]["remove"]["elem"].grid(row = ui_elements["shared"]["remove"]["location"][0], 
                                                column = ui_elements["shared"]["remove"]["location"][1], 
                                                padx = 5, pady = 5)

def init_element(parent_frame, ui_elements: dict):
    """Initialize the sine wave GUI component.
            parent_frame: ttk.Frame
                The parent frame to place the sine wave GUI component.
            ui_elements: dict
                The dictionary of UI elements to be initialized."""
    
    # First, initialize the shared UI components
    
    print("\nInitializing shared\n")
    #print(ui_elements)
    for key, value in ui_elements.items():
        if key == "shared":
            init_shared(parent_frame, ui_elements)
            continue
        print(key, value)
        if "label" in value:
            value["label"] = ttk.Label(parent_frame, text=value["label"][0]).grid(row=value["label"][1][0], column=value["label"][1][1], padx=5, pady=5)
        if value["type"] == "dropdown":
            value["val"] = tk_var_type(value["val"][1], value["val"][0])
            value["elem"] = ttk.Combobox(parent_frame, textvariable=value["val"], values=value["values"])
            value["elem"].grid(row=value["location"][0], column=value["location"][1], padx=5, pady=5)
        elif value["type"] == "entry":
            value["val"] = tk_var_type(value["val"][1], value["val"][0])
            value["elem"] = ttk.Entry(parent_frame, textvariable=value["val"])
            value["elem"].grid(row=value["location"][0], column=value["location"][1], padx=5, pady=5)
        elif value["type"] == "button":
            value["elem"] = ttk.Button(parent_frame, text="Remove", command=lambda: value["func"])
            value["elem"].grid(row=value["location"][0], column=value["location"][1], padx=5, pady=5)
        
    print("\nFinishing shared\n")
    #print(ui_elements)

GUI_SHARED_PROTOTYPE = {
                        "function": {"val": ("","string"),
                                    "type": "dropdown",
                                    "combobox_func": lambda parent_frame, ui_elements: None,
                                    "elem": None,#ttk.Combobox(param_frame, textvariable=tk.StringVar(value = "generate_plot_dataA")), 
                                    "plot_func": None, # reference to matching plot function
                                    "location": (0, 0),
                                    "values": ('generate_plot_dataA', 'generate_plot_dataB', 'Optical Line'),
                                    "default": 0
                                    },
                        "name":     {"val": ("New Parameter", "string"),
                                    "type": "entry",
                                    "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = "New Parameter")),
                                    "location": (0, 1),
                                    },
                        "remove":   {"val": None,
                                    "type": "button",
                                    "func": None, # Button function
                                    "elem": None,
                                    "location": (0, 2),
                                    }
                }

GUI_PROTOTYPES = {
    "sine_wave": { 
                "shared": deepcopy(GUI_SHARED_PROTOTYPE),
                "amplitude": {"val": ("1.0","double"), #Double
                              "type": "entry",
                              "elem": None, #ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                              "location": (1, 1),
                              "label": ("Amplitude", (1,0)) # text, loc
                            },
                "frequency": {"val": ("1.0","double"),
                              "type": "entry",
                              "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                              "location": (2, 1),
                              "label": ("Frequency", (2,0))
                            },
                "phase":     {"val": ("1.0","double"),
                              "type": "entry",
                              "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 0.0)),
                              "location": (3, 1),
                              "label": ("Phase", (3,0))
                            },
                        },
    "Optical Line": {
                "shared": deepcopy(GUI_SHARED_PROTOTYPE),
                "lenses": {"val": ("1.0","double"),
                              "type": "entry",
                              "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                              "location": (1, 1),
                              "label": ("Lenses", (1,0))
                            },
                "length": {"val": ("1.0","double"),
                              "type": "entry",
                              "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                              "location": (2, 1),
                              "label": ("Length", (2,0))
                            },
                "wavelength":     {"val": ("1.0","double"),
                              "type": "entry",
                              "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 0.0)),
                              "location": (3, 1),
                              "label": ("Wavelength", (3,0))
                            },
    },
    }

GUI_PROTOTYPE_MAP = {
    "generate_plot_dataA": "sine_wave",
    "generate_plot_dataB": "sine_wave",
    "Optical Line": "Optical Line",
}

def dictest():
    root = tk.Tk()
    frame = ttk.Frame(root)
    frame.grid(row = 0, column = 0)
    ui_elems = deepcopy(GUI_PROTOTYPES["sine_wave"])
    ui_elems["shared"]["remove"]["func"] = print("Remove button clicked")
    init_element(frame, ui_elems)
    frame2 = ttk.Frame(root)
    frame2.grid(row = 1, column = 0)
    ui_elems2 = deepcopy(GUI_PROTOTYPES["sine_wave"])
    ui_elems2["shared"]["remove"]["func"] = print("Remove button clicked")
    init_element(frame, ui_elems2)
    root.mainloop()

if __name__ == "__main__":
    dictest()