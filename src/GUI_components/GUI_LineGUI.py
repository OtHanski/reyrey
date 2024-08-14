"""This module implements the LineItem and LineGUI classes, which are used to 
define the GUI elements for holding an optical line and a collection of optical 
lines, respectively. Optical line types to be used are imported into GUI_elems."""

import tkinter as tk
from tkinter import ttk

# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from raycalc.matrices import matrixdicts    # pylint: disable=import-error
    from GUI_OpticalLine import OpticalLine     # pylint: disable=import-error
    from GUI_Cavities import RibbonCavity       # pylint: disable=import-error
else:
    from .raycalc.matrices import matrixdicts
    from .GUI_OpticalLine import OpticalLine
    from .GUI_Cavities import RibbonCavity

debug = False

GUI_elems = {"Optical Line": OpticalLine, "Ring Cavity": RibbonCavity}

class LineItem:
    """tkinter widget for a single line parameter"""
    def __init__(self,              #pylint: disable=dangerous-default-value
                 parent,
                 parentframe: ttk.Frame,
                 compid = 0,
                 location = None,
                 opticalitems = GUI_elems):
        self.parent = parent
        self.compid = compid
        self.hor = tk.IntVar(value=1)
        self.ver = tk.IntVar(value=1)
        if location is None:
            location = (compid,0)


        self.frame = ttk.LabelFrame(parentframe, text=f"Component {self.compid}", relief=tk.RIDGE)
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
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
        self.func = None

        self.component.grid(row=0, column=0, padx=5)
        self.component.current(0)

        self.remove_button = ttk.Button(self.buttonframe,
                                        text="Remove",
                                        command=self.remove)
        self.remove_button.grid(row=0, column=1, padx=5)

        self.itemframe = ttk.Frame(self.frame)
        self.itemframe.grid(row=1, column=0, pady=5, sticky="news")
        self.itemframe.columnconfigure(0, weight=1)
        self.itemframe.rowconfigure(0, weight=1)

        self.fields = {}
        self.init_fields()


    def init_fields(self):
        """Initialize the fields for the optical line"""
        self.item = self.opticalitems[self.get_function()](self.parent,
                                                           self.itemframe,
                                                           compid = 0,
                                                           location = (0,0))

    def remove_fields(self):
        """Wipe old UI elements to replace with new"""
        self.item.frame.destroy()
        del self.item

    def update_fields(self):
        """Update the fields for the optical line to a new configuration"""
        if debug:
            print("Updating fields")
        self.remove_fields()
        self.init_fields()

    def updateID(self, compid): #pylint: disable=invalid-name
        """Update the ID of the component"""
        self.compid = compid
        self.frame.config(text=f"Component {self.compid}")
        # Reposition on grid
        self.frame.grid(row=self.compid, column=0, pady=5, sticky="news")


    def remove(self):
        """Remove the line item from the parent"""
        if debug:
            print(f"Removing {self.compid}")
        self.parent.destroyLineParam(self.compid)


    def get_function(self):
        """Return the current function selected in the combobox"""
        return self.component.get()

    def get_ABCD(self):# pylint: disable=invalid-name
        """Return the ABCD matrix for the current optical line"""
        self.func = matrixdicts[self.get_function()]["func"]
        if debug:
            print(self.func)
        matrixparams = {key: self.fields[f"val{i}"].get()
                        for i, key in enumerate(matrixdicts[self.get_function()]["params"])}
        matrixparams["func"] = self.func
        ABCD = matrixparams #pylint: disable=invalid-name
        if debug:
            print(ABCD)
        return ABCD

    def replot(self, n = 1000):
        """Replot the optical line"""
        # Implemented in child classes
        return self.item.replot(n)

    def savestate(self):
        """Save current state in dict for loading"""
        state = {}
        state["function"] = self.get_function()
        state["fields"] = {}
        state["item"] = self.item.savestate()
        for key in self.fields: # pylint: disable=consider-using-dict-items
            state["fields"][key] = self.fields[key].get()
        return state

    def loadstate(self, state):
        """Load state from dict"""
        self.component.set(state["function"])
        self.update_fields()
        for key in state["fields"]:
            self.fields[key].set(state["fields"][key])
        self.item.loadstate(state["item"])


class LineGUI:
    """tkinter widget for creating, editing and destroying optical lines"""
    def __init__(self, parent, parentframe, compid = 0, location = (0,0)):
        """parent: parent widget, 
        parentframe: parent frame, 
        compid: id of the widget, 
        location: grid location"""
        self.parent = parent
        self.compid = compid
        self.frame = ttk.LabelFrame(parentframe, text="Optical Beams")
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

        #self.name = tk.StringVar(value = "New Optical Line")
        #self.namefield = ttk.Entry(self.button_frame, textvariable=self.name)
        #self.namefield.grid(row=0, column=0, padx=5)

        self.add_button = ttk.Button(self.button_frame, text="Add Line", command=self.add_parameter)
        self.add_button.grid(row=0, column=1, padx=5)

        self.showhide_button = ttk.Button(self.button_frame,
                                          text="Show/Hide",
                                          command=self.showhide)
        self.showhide_button.grid(row=0, column=2, padx=5)

        # Replot button
        self.replot_button = ttk.Button(self.button_frame, text="Replot", command=self.replot)
        self.replot_button.grid(row=1, column=2, padx=5)
        ### END BUTTON FRAME ###

        ### INPUT BEAM FRAME###
        self.inputframe = ttk.LabelFrame(self.frame, text="Plotting parameters", relief=tk.RIDGE)
        self.inputframe.grid(row=1, column=0, pady=5, sticky="news")
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.rowconfigure(0, weight=1)

        self.samples = tk.IntVar(value=1000)
        self.samples_label = ttk.Label(self.inputframe, text="Samples per interval")
        self.samples_label.grid(row=0, column=0, padx=5)
        self.samples_entry = ttk.Entry(self.inputframe, textvariable=self.samples)
        self.samples_entry.grid(row=0, column=1, padx=5)
        # (Z = 0, ZR = 0, lam = 0, W = 0, n = 1)
        self.input = {} # List of inputs, example: "Samples": tk.IntVar(value=1000)
        self.input_widgets = {}
        i = 1
        for key in self.input: # pylint: disable=consider-using-dict-items
            self.input_widgets[key] = ttk.Label(self.inputframe, text=key)
            self.input_widgets[key].grid(row=i, column=0, padx=5)
            self.input_widgets[f"{key}_entry"] = ttk.Entry(self.inputframe,
                                                           textvariable=self.input[key])
            self.input_widgets[f"{key}_entry"].grid(row=i, column=1, padx=5)
            i += 1

        ### COMPONENT FRAME ###
        self.componentframe = ttk.LabelFrame(self.frame,
                                             text="Optical Line Drawer")
        self.componentframe.grid(row=2, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.opticalLines = [] #pylint: disable=invalid-name
        ### END COMPONENT FRAME ###

        ### COLOR LIST ###
        # Initialize 20 colors for plot defaults
        self.colors = ["red", "blue", "green", "orange", "purple", "brown",
                       "pink", "cyan", "magenta", "yellow", "black", "grey",
                       "lightblue", "lightgreen", "lightyellow", "lightgrey",
                       "darkblue", "darkgreen", "darkred", "darkgrey"]
        self.colorid = 0

    def add_parameter(self):
        """Add a new optical line component"""
        newcompid = len(self.opticalLines)
        location = (newcompid, 0)
        new_optLine = LineItem(self, self.componentframe, newcompid, location)
        self.opticalLines.append(new_optLine)
        self.componentframe.rowconfigure(newcompid, weight=1)

    def destroyLineParam(self, compid):
        """Destroy the optical line component with the given id"""
        line = self.opticalLines.pop(compid)
        line.frame.destroy()
        del line
        # Renumber and reposition the parameters
        for i, optLine in enumerate(self.opticalLines):
            optLine.updateID(compid = i)

    def showhide(self):
        """Show or hide the optical line"""
        if self.componentframe.winfo_ismapped():
            self.componentframe.grid_remove()
        else:
            self.componentframe.grid()

    def calculate_beamshape(self):
        """Calculate the beam shape for the optical line, currently implemented in child classes"""
        return 1

    def givecolor(self, n = 1):
        """Returns a list of n colors, cycling through the color list"""
        color = []
        for i in range(n): #pylint: disable=unused-variable
            # Continue from current loop location.
            color.append(self.colors[(self.colorid)%len(self.colors)])
            self.colorid += 1
            if self.colorid == len(self.colors):
                self.colorid = 0
        return color

    """def get_lines(self):
        xydat = {}
        i = 0
        for line in self.opticalLines:
            xydat[i] = line.replot()
            i += 1
        return xydat"""

    def replot(self):
        """Replot the optical lines"""
        plotdata = {}
        i = 0
        for optLine in self.opticalLines:
            plotdata[i] = optLine.replot(n = self.samples.get())
            i+=1
        if debug:
            print(f"Replot done in LineGUI, keys: {plotdata.keys()}")
        if debug:
            print(f"Replot done in LineGUI, values: {plotdata[0].keys()}")
        return plotdata

    def savestate(self):
        """Save the current state of the GUI in a dict"""
        state = {}
        state["input"] = {}
        state["Samples"] = self.samples.get()
        for key in self.input: # pylint: disable=consider-using-dict-items
            state["input"][key] = self.input[key].get()
        state["opticalLines"] = [optLine.savestate() for optLine in self.opticalLines]
        return state

    def loadstate(self, state):
        """Load the state of the GUI from a dict"""
        # First ask whether to remove pre-existing elements
        if tk.messagebox.askyesno("Warning", "Remove pre-existing optical lines?"):
            while self.opticalLines:
                self.destroyLineParam(0)
        # Set samples and input parameters
        self.samples.set(state["Samples"])
        for key in state["input"]:
            self.input[key].set(state["input"][key])
        # Load optical lines
        for optLine in state["opticalLines"]:
            self.add_parameter()
            self.opticalLines[-1].loadstate(optLine)

def test():
    """Test function for LineGUI"""
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = LineGUI(root, root, location=(0,0)) #pylint: disable=unused-variable
    root.mainloop()

if __name__ == "__main__":
    test()
