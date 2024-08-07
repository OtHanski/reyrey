from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from raytracing.matrices import matrixdicts, ringCavity, linCavity
from GUI_OpticalLine import OpticalLine
import raytracing.matrixcalc as rey


class paramsine:
    # Prototype for sine wave
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self. parent = parent
        # Create simple frame with sample tkinter components
        self.frame = ttk.LabelFrame(parentframe, text="Sine Wave", relief=tk.RIDGE)
        self.frame.grid(row=0, column=0, pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.amplitude = tk.DoubleVar(value=1)
        self.amplitude_label = ttk.Label(self.frame, text="Amplitude")
        self.amplitude_label.grid(row=0, column=0, padx=5)
        self.amplitude_entry = ttk.Entry(self.frame, textvariable=self.amplitude)
        self.amplitude_entry.grid(row=0, column=1, padx=5)

        self.frequency = tk.DoubleVar(value=1)
        self.frequency_label = ttk.Label(self.frame, text="Frequency")
        self.frequency_label.grid(row=1, column=0, padx=5)
        self.frequency_entry = ttk.Entry(self.frame, textvariable=self.frequency)
        self.frequency_entry.grid(row=1, column=1, padx=5)

class paramcosine:
    # Prototype for cosine wave
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self. parent = parent
        # Create simple frame with sample tkinter components
        self.frame = ttk.LabelFrame(parentframe, text="Cosine Wave", relief=tk.RIDGE)
        self.frame.grid(row=0, column=0, pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.amplitude = tk.DoubleVar(value=1)
        self.amplitude_label = ttk.Label(self.frame, text="Amplitude")
        self.amplitude_label.grid(row=0, column=0, padx=5)
        self.amplitude_entry = ttk.Entry(self.frame, textvariable=self.amplitude)
        self.amplitude_entry.grid(row=0, column=1, padx=5)

        self.frequency = tk.DoubleVar(value=1)
        self.frequency_label = ttk.Label(self.frame, text="Frequency")
        self.frequency_label.grid(row=1, column=0, padx=5)
        self.frequency_entry = ttk.Entry(self.frame, textvariable=self.frequency)
        self.frequency_entry.grid(row=1, column=1, padx=5)
    
class paramtan:
    # Prototype for tangent wave
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self. parent = parent
        # Create simple frame with sample tkinter components
        self.frame = ttk.LabelFrame(parentframe, text="Tangent Wave", relief=tk.RIDGE)
        self.frame.grid(row=0, column=0, pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.amplitude = tk.DoubleVar(value=1)
        self.amplitude_label = ttk.Label(self.frame, text="Amplitude")
        self.amplitude_label.grid(row=0, column=0, padx=5)
        self.amplitude_entry = ttk.Entry(self.frame, textvariable=self.amplitude)
        self.amplitude_entry.grid(row=0, column=1, padx=5)

        self.frequency = tk.DoubleVar(value=1)
        self.frequency_label = ttk.Label(self.frame, text="Frequency")
        self.frequency_label.grid(row=1, column=0, padx=5)
        self.frequency_entry = ttk.Entry(self.frame, textvariable=self.frequency)
        self.frequency_entry.grid(row=1, column=1, padx=5)


opticalitems = {"sine_wave": paramsine, "cosine_wave": paramcosine, "tangent_wave": paramtan, "Optical Line": OpticalLine}

class LineItem:
    """tkinter widget for a single line parameter"""
    def __init__(self, parent, parentframe: ttk.Frame, id = 0, location = (0,0), updateFlag = None, opticalitems = opticalitems):
#   def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self.parent = parent
        self.id = id
        self.hor = tk.IntVar(value=1)
        self.ver = tk.IntVar(value=1)

        self.updateFlag = updateFlag

        self.frame = ttk.LabelFrame(parentframe, text=f"Component {id}", relief=tk.RIDGE)
        self.frame.grid(row=id, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1) 
        
        self.buttonframe = ttk.Frame(self.frame)
        self.buttonframe.grid(row=0, column=0, pady=5, sticky="news")
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)

        self.opticalitems = opticalitems
        self.combo_vals = [key for (key,value) in opticalitems.items()]
        self.component = ttk.Combobox(self.buttonframe, values=self.combo_vals)
        # Bind the combobox to the update_fields function
        self.component.bind("<<ComboboxSelected>>", lambda event: self.update_fields())

        self.component.grid(row=0, column=0, padx=5)
        self.component.current(0)

        self.remove_button = ttk.Button(self.buttonframe, text="Remove", command=self.remove).grid(row=0, column=1, padx=5)

        self.itemframe = ttk.Frame(self.frame)
        self.itemframe.grid(row=1, column=0, pady=5, sticky="news")

        self.fields = {}
        self.init_fields()
        
     
    def init_fields(self):
        self.fieldframe = ttk.Frame(self.frame)
        self.fieldframe.grid(row=1, column=0, pady=5, sticky="news")
        self.fieldframe.columnconfigure(0, weight=1)
        self.fieldframe.columnconfigure(1, weight=1)
        self.fieldframe.columnconfigure(2, weight=1)
        self.fieldframe.rowconfigure(0, weight=1)
        self.fieldframe.rowconfigure(1, weight=1)
        self.fieldframe.rowconfigure(2, weight=1)

        i = len(self.fields)
        self.fields[i] = self.opticalitems[self.get_function()](self.parent, self.fieldframe, id = i, location = (0,0), updateFlag = None)
    
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

    def updateID(self, id):
        self.id = id
        self.frame.config(text=f"Component {id}")
        # Reposition on grid
        self.frame.grid(row=id, column=0, pady=5, sticky="news")
        

    def remove(self):
        print(f"Removing {self.id}")
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


class LineGUI:
    """tkinter widget for creating, editing and destroying optical lines"""
    def __init__(self, parent, parentframe, id = 0, location = (0,0), updateFlag: tk.IntVar = None):
        """updateFlag is a flag that can be set to trigger an update"""
        self.parent = parent
        self.id = id
        self.frame = ttk.LabelFrame(parentframe, text=f"Optical Beams")
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.updateFlag = updateFlag

        ### BUTTON FRAME ###
        self.button_frame = ttk.Frame(self.frame)
        self.button_frame.grid(row=0, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)

        #self.name = tk.StringVar(value = "New Optical Line")
        #self.namefield = ttk.Entry(self.button_frame, textvariable=self.name)
        #self.namefield.grid(row=0, column=0, padx=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Line", command=self.add_parameter)
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
        self.inputframe = ttk.LabelFrame(self.frame, text="Plotting parameters", relief=tk.RIDGE)
        self.inputframe.grid(row=1, column=0, pady=5, sticky="news")
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.rowconfigure(0, weight=1)

        # (Z = 0, ZR = 0, lam = 0, W = 0, n = 1)
        self.input = {"Samples": tk.IntVar(value=1000)} # Refractive index
        self.input_widgets = {}
        i = 0
        for key in self.input:
            self.input_widgets[key] = ttk.Label(self.inputframe, text=key)
            self.input_widgets[key].grid(row=i, column=0, padx=5)
            self.input_widgets[f"{key}_entry"] = ttk.Entry(self.inputframe, textvariable=self.input[key])
            self.input_widgets[f"{key}_entry"].grid(row=i, column=1, padx=5)
            i += 1

        ### COMPONENT FRAME ###
        self.componentframe = ttk.LabelFrame(self.frame, text="Optical Line Drawer")#, relief=tk.RIDGE)
        self.componentframe.grid(row=2, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.opticalLines = []
        ### END COMPONENT FRAME ###

    def add_parameter(self):
        id = len(self.opticalLines)
        location = (id, 0)
        new_opticalLine = LineItem(self, self.componentframe, id, location, updateFlag = self.updateFlag)
        self.opticalLines.append(new_opticalLine)
        self.componentframe.rowconfigure(id, weight=1)
    
    def destroyLineParam(self, id):
        line = self.opticalLines.pop(id)
        line.frame.destroy()
        del line
        # Renumber and reposition the parameters
        for i, optLine in enumerate(self.opticalLines):
            optLine.updateID(id = i)
    
    def showhide(self):
        # Show or hide the optical line
        if self.componentframe.winfo_ismapped():
            self.componentframe.grid_remove()
        else:
            self.componentframe.grid()

    def calculate_beamshape(self):
        pass

    def get_lines(self):
        xydat = {}
        i = 0
        for line in self.opticalLines:
            xydat[i] = line.get_plot()
            i += 1
        return xydat

    def replot(self):
        self.matrices = []
        for param in self.parameters:
            self.matrices.append(param.get_ABCD())

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = LineGUI(root, root, location=(0,0))
    root.mainloop()

if __name__ == "__main__":
    test()
    
    