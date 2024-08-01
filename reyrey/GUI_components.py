from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from raytracing.matrices import matrixdicts, ringCavity, linCavity
import raytracing.matrixcalc as rey

class LineParameter:
    """tkinter widget for a single line parameter"""
    def __init__(self, parent, parentframe: ttk.Frame, id = 0):
        self.parent = parent
        self.id = id
        self.hor = tk.IntVar(value=1)
        self.ver = tk.IntVar(value=1)

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
        i = 0
        for param in matrixdicts[self.get_function()]["params"]:
            self.fields[f"label{i}"] = ttk.Label(self.frame, text=param)
            self.fields[f"label{i}"].grid(row=i+1, column=0, padx=5)
            self.fields[f"val{i}"] = tk.DoubleVar(value=0)
            self.fields[f"elem{i}"] = ttk.Entry(self.frame, textvariable=self.fields[f"val{i}"])
            self.fields[f"elem{i}"].grid(row=i+1, column=1, padx=5)
            i += 1
        
        horver = matrixdicts[self.get_function()]["horver"]
        self.fields["hor_check"] = ttk.Checkbutton(self.frame, text="Horizontal", variable=self.hor)
        self.fields["hor_check"].grid(row=i+1, column=0, padx=5)
        self.fields["ver_check"] = ttk.Checkbutton(self.frame, text="Vertical", variable=self.ver)
        self.fields["ver_check"].grid(row=i+1, column=1, padx=5)
        # Remove the hor and ver checkbuttons if the component doesn't support them
        if not horver:
            self.fields["hor_check"].destroy()
            self.fields["ver_check"].destroy()
    
    def remove_fields(self):
        # Wipe old UI elements to replace with new
        for key in list(self.fields):
            print(type(self.fields[key]))
            if type(self.fields[key]) in [ttk.Label, ttk.Entry, ttk.Checkbutton]:
                print(f"Destroying {key}")
                self.fields[key].destroy()
            del self.fields[key]
    
    def update_fields(self):
        print("Updating fields")
        self.remove_fields()
        self.init_fields()


    def remove(self):
        self.parent.destroyLineParam(self.id)


    def get_function(self):
        return self.component.get()
    
    def get_ABCD(self):
        self.func = matrixdicts[self.get_function()]["func"]
        print(self.func)
        matrixparams = {key: self.fields[f"val{i}"].get() for i, key in enumerate(matrixdicts[self.get_function()]["params"])}
        matrixparams["func"] = self.func
        ABCD = matrixparams#matrixdicts[self.get_function()]["func"](**{key: self.fields[f"val{i}"].get() for i, key in enumerate(matrixdicts[self.get_function()]["params"])})
        print(ABCD)
        return ABCD


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


        ### BUTTON FRAME ###
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
        ### END BUTTON FRAME ###

        ### INPUT BEAM FRAME###
        self.inputframe = ttk.LabelFrame(self.frame, text="Input Beam", relief=tk.RIDGE)
        self.inputframe.grid(row=1, column=0, pady=5, sticky="news")
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.rowconfigure(0, weight=1)

        # (Z = 0, ZR = 0, lam = 0, W = 0, n = 1)
        self.input = {"Z": tk.DoubleVar(value=0), # Distance from waist
                      "ZR": tk.DoubleVar(value=0), # Rayleigh length
                      "lam": tk.DoubleVar(value=972E-9), # Wavelength
                      "W": tk.DoubleVar(value=1E-3), # Beam waist
                      "n": tk.DoubleVar(value=1)} # Refractive index
        self.input_widgets = {}
        i = 0
        for key in self.input:
            self.input_widgets[key] = ttk.Label(self.inputframe, text=key)
            self.input_widgets[key].grid(row=i, column=0, padx=5)
            self.input_widgets[f"{key}_entry"] = ttk.Entry(self.inputframe, textvariable=self.input[key])
            self.input_widgets[f"{key}_entry"].grid(row=i, column=1, padx=5)
            i += 1

        ### COMPONENT FRAME ###
        self.componentframe = ttk.LabelFrame(self.frame, text="Optical Line", relief=tk.RIDGE)
        self.componentframe.grid(row=2, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.parameters = []
        ### END COMPONENT FRAME ###

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
        # Show or hide the optical line
        if self.componentframe.winfo_ismapped():
            self.componentframe.grid_remove()
        else:
            self.componentframe.grid()

    def calculate_beamshape(self):
        pass

    def replot(self):
        self.matrices = []
        for param in self.parameters:
            self.matrices.append(param.get_ABCD())

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = OpticalLine(root)
    root.mainloop()

if __name__ == "__main__":
    test()
    
    