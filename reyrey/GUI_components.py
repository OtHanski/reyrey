from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from raytracing.matrices import matrixdicts, ringCavity, linCavity

class LineParameter:
    """tkinter widget for a single line parameter"""
    def __init__(self, parent, parentframe: ttk.Frame, id = 0):
        self.parent = parent
        self.id = id

        self.frame = ttk.LabelFrame(parentframe, text=f"Component {id}", relief=tk.RIDGE)
        self.frame.grid(row=id, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.combo_vals = [key for (key,value) in matrixdicts.items()]
        self.component = ttk.Combobox(self.frame, values=self.combo_vals)
        # Bind the combobox to the update_fields function
        self.component.bind("<<ComboboxSelected>>", lambda event: self.update_fields())

        self.component.grid(row=0, column=0, padx=5)
        self.component.current(0)

        self.remove_button = ttk.Button(self.frame, text="Remove", command=self.remove).grid(row=0, column=1, padx=5)

        self.fields = {}
        self.init_fields()
        
     
    def init_fields(self):
        i = 1
        for key, value in matrixdicts[self.get_function()].items():
            print(key, value)
            self.fields[key] = {}
            self.fields[key]["label"] = ttk.Label(self.frame, text=key)
            self.fields[key]["label"].grid(row=i, column=0, padx=5)
            self.fields[key]["val"] = tk.StringVar(value=str(value))
            self.fields[key]["elem"] = ttk.Entry(self.frame, textvariable=self.fields[key]["val"])
            self.fields[key]["elem"].grid(row=i, column=1, padx=5)

            i += 1
    
    def remove_fields(self):
        keys = list(self.fields.keys())
        print(keys)
        for key in list(self.fields):
            self.fields[key]["label"].destroy()
            self.fields[key]["elem"].destroy()
            del self.fields[key]
    
    def update_fields(self):
        print("Updating fields")
        self.remove_fields()
        self.init_fields()


    def remove(self):
        self.parent.destroyLineParam(self.id)


    def get_function(self):
        return self.component.get()


class OpticalLine:
    """tkinter widget for a single optical line"""
    def __init__(self, parent, id = 0, location = (0,0)):
        self.parent = parent
        self.id = id
        self.frame = ttk.LabelFrame(parent, text=f"Optical Line {id}", relief=tk.RIDGE)
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.grid(row=0, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        self.name = tk.StringVar(value = "New Optical Line")
        self.namefield = ttk.Entry(self.button_frame, textvariable=self.name)
        self.namefield.grid(row=0, column=0, padx=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.grid(row=0, column=1, padx=5)

        self.showhide_button = ttk.Button(self.button_frame, text="Show/Hide", command=self.showhide)
        self.showhide_button.grid(row=0, column=2, padx=5)
        
        # Add ver and hor plot tickboxes
        self.ver = tk.IntVar()
        self.ver_check = ttk.Checkbutton(self.button_frame, text="Vertical", variable=self.ver)
        self.ver_check.grid(row=1, column=0, padx=5)
        self.hor = tk.IntVar()
        self.hor_check = ttk.Checkbutton(self.button_frame, text="Horizontal", variable=self.hor)
        self.hor_check.grid(row=1, column=1, padx=5)
        # Replot button
        self.replot_button = ttk.Button(self.button_frame, text="Replot", command=self.replot)
        self.replot_button.grid(row=1, column=2, padx=5)

        self.componentframe = ttk.LabelFrame(self.frame, text="Optical Line", relief=tk.RIDGE)
        self.componentframe.grid(row=1, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.parameters = []

    def add_parameter(self):
        id = len(self.parameters)
        new_parameter = LineParameter(self, self.componentframe, id)
        new_parameter
        self.parameters.append(new_parameter)
        self.componentframe.rowconfigure(id, weight=1)
    
    def destroyLineParam(self, id):
        param = self.parameters.pop(id)
        param.frame.destroy()
        del param
        # Renumber the parameters
        for i, param in enumerate(self.parameters):
            param.id = i
    
    def showhide(self):
        pass

    def replot(self):
        pass

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = OpticalLine(root)
    root.mainloop()

if __name__ == "__main__":
    test()
    
    