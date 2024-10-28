#pylint: disable=invalid-name
"""Implements the Scatterplot class, a class to handle test points for an optical line,
e.g. manual waist measurement points for fitting."""

import tkinter as tk
from tkinter import ttk
import numpy as np

# Import the GUI component prototypes and init functions
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from GUI_OptLineProto import GUI_OptLineProto # pylint: disable=import-error
else:
    from .GUI_OptLineProto import GUI_OptLineProto

debug = False

class ScatterPoint:
    """A class to build the UI element to represent a single point on a scatter plot, offshoot of
    LineParameter from OptLineProto"""
    def __init__(self, parent, parentframe: ttk.Frame, compid = 0, DEBUG = False):
        self.parent = parent
        self.compid = compid
        self.DEBUG = DEBUG

        self.hor = tk.IntVar(value=1)
        self.ver = tk.IntVar(value=1)

        self.frame = ttk.LabelFrame(parentframe, text=f"Component {self.compid}", relief=tk.RIDGE)
        self.frame.grid(row=self.compid, column=0, pady=5, sticky="news")
        # Make the frame expand to fill the parent
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.combo_vals = [key for (key,value) in [("Point", None)]]
        self.component = ttk.Combobox(self.frame, values=self.combo_vals)
        # Bind the combobox to the update_fields function
        self.component.bind("<<ComboboxSelected>>", lambda event: self.update_fields())

        self.component.grid(row=0, column=0, padx=5)
        self.component.current(0)

        self.remove_button = ttk.Button(self.frame, text="Remove", command=self.remove)
        self.remove_button.grid(row=0, column=1, padx=5)

        self.fields = {}
        self.horverchecks = {}
        self.init_fields()

        def dummy():
            print("Dummy function")
        self.func = dummy
        self.ABCDhor = None
        self.ABCDver = None

    def init_fields(self):
        """Initialise the default input fields for the component"""
        i = 0
        for param in ["x", "hor", "ver"]:
            self.fields[i] = {}
            self.fields[i]["label"] = ttk.Label(self.frame, text=param)
            self.fields[i]["label"].grid(row=i+1, column=0, padx=5)
            self.fields[i]["val"] = tk.DoubleVar(value=1)
            self.fields[i]["elem"] = ttk.Entry(self.frame, textvariable=self.fields[i]["val"])
            self.fields[i]["elem"].grid(row=i+1, column=1, padx=5)
            i += 1

        horver = True
        self.horverchecks["hor_check"] = ttk.Checkbutton(self.frame,
                                                         text="Horizontal",
                                                         variable=self.hor)
        self.horverchecks["hor_check"].grid(row=i+1, column=0, padx=5)
        self.horverchecks["ver_check"] = ttk.Checkbutton(self.frame,
                                                         text="Vertical",
                                                         variable=self.ver)
        self.horverchecks["ver_check"].grid(row=i+1, column=1, padx=5)
        # Remove the hor and ver checkbuttons if the component doesn't support them
        if not horver:
            self.horverchecks["hor_check"].destroy()
            self.horverchecks["ver_check"].destroy()

    def remove_fields(self):
        """Remove the input fields for the component"""
        # Wipe old UI elements to replace with new
        if self.DEBUG:
            print("Removing fields")
        for i in list(self.fields):
            for key in list(self.fields[i]):
                if type(self.fields[i][key]) in [ttk.Label, ttk.Entry, ttk.Checkbutton]:
                    if self.DEBUG:
                        print(f"Destroying {key}")
                    self.fields[i][key].destroy()
                del self.fields[i][key]
        if self.DEBUG:
            print("Removing horverchecks")
        for key in list(self.horverchecks):
            if type(self.horverchecks[key]) in [ttk.Checkbutton]:
                if self.DEBUG:
                    print(f"Destroying {key}")
                self.horverchecks[key].destroy()
            del self.horverchecks[key]

    def update_fields(self):
        """Update the input fields for the component upon selection of a new component type"""
        if self.DEBUG:
            print("Updating fields")
        self.remove_fields()
        self.init_fields()


    def remove(self):
        """Destroy the optical line"""
        self.parent.destroyLineParam(self.compid)


    def get_function(self):
        """Get the current function selected in the combobox"""
        return self.component.get()

    def calc_ABCD(self): # pylint: disable=invalid-name
        """Calculate the ABCD matrices for the component"""
        return (None, None)
    
    def get_vals(self):
        """Get the current values of the component"""
        vals = {}
        vals["x"] = self.fields[0]["val"].get()
        if self.hor:
            vals["hor"] = self.fields[1]["val"].get()
        else:
            vals["hor"] = None
        if self.ver:
            vals["ver"] = self.fields[2]["val"].get()
        else:
            vals["ver"] = None

    def savestate(self):
        """Save current component state in a dictionary"""
        try:
            state = {}
            state["function"] = self.component.get()
            state["hor"] = self.hor.get()
            state["ver"] = self.ver.get()
            state["fields"] = {}
            for key in self.fields: # pylint: disable=consider-using-dict-items
                state["fields"][key] = self.fields[key]["val"].get()
            return state
        except Exception as e: #pylint: disable=broad-except
            print("Error in savestate:",e)
            print("State:",state)
            print("Fields:",self.fields)

    def loadstate(self, state):
        """Load a component state from a dictionary"""
        self.component.set(state["function"])
        self.update_fields()
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        if self.DEBUG:
            print(f"Loading state: {state}")
            print(f"Fields: {self.fields}")
        for key in self.fields: #pylint: disable=consider-using-dict-items
            if self.DEBUG:
                print(f"Setting field {key} to {state['fields'][str(key)]}")
                print(f"Field: {self.fields[key]['val']}")
            self.fields[key]["val"].set(state["fields"][str(key)])
            print(self.fields[key]["val"].get())

class ScatterPlot(GUI_OptLineProto):
    """Default optical beamline implementation"""
    def __init__(self, parent, parentframe,  compid = 0, location = (0,0), DEBUG = 0): # pylint: disable=useless-super-delegation
        self.input = {}
        super().__init__(parent, parentframe, compid, location, inputDict=self.input, DEBUG = DEBUG)
    
    def add_parameter(self):
        """Add a new component to the optical line"""
        newcompid = len(self.parameters)
        new_parameter = ScatterPoint(parent = self,
                                      parentframe = self.componentframe,
                                      compid = newcompid,
                                      DEBUG = self.DEBUG)
        self.parameters.append(new_parameter)
        self.componentframe.rowconfigure(self.compid, weight=1)

    def replot(self, n = 1000):
        """Overwrite the replot function to plot the scatter points"""
        self.samples.set(n)
        points = []
        for point in self.parameters:
            points.append(point.get_vals())
        self.plotdata = {}
        if "x_offset" in self.input:
            offset = self.input["x_offset"].get()
        else:
            offset = 0
        if self.hor.get():
            self.plotdata["hor"] = {}
            xs = []
            ws = []
            for point in points:
                if point["hor"] is not None:
                    xs.append(point["x"] + offset)
                    ws.append(point["hor"])
            xs = np.array(xs)
            ws = np.array(ws)
            # Check whether the x_offset parameter exists in current input
            self.plotdata["hor"]["x"] = xs + offset
            self.plotdata["hor"]["w"] = ws
        if self.ver.get():
            self.plotdata["ver"] = {}
            xs = []
            ws = []
            for point in points:
                if point["ver"] is not None:
                    xs.append(point["x"] + offset)
                    ws.append(point["ver"])
            xs = np.array(xs)
            ws = np.array(ws)
            self.plotdata["ver"]["x"] = xs + offset
            self.plotdata["ver"]["w"] = ws
        self.plotdata["plotoptions"] = self.plotoptions
        if self.DEBUG:
            print(f"plotdata keys: {self.plotdata.keys()}")
        if self.DEBUG:
            print(f"plotdata: {self.plotdata}")
        return self.plotdata

def test():
    """Test function for OpticalLine"""
    root = tk.Tk()
    root.title("Scatterplot Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = ScatterPlot(root,root) #pylint: disable=unused-variable
    root.mainloop()

if __name__ == "__main__":
    test()
