"""
Define the class prototype for Optical line implements in the GUI.
"""

import tkinter as tk
from tkinter import ttk

# Import the GUI component prototypes and init functions
# format depends on whether this is run as a script for testing or imported as a module
if __name__ == "__main__":
    from raycalc.matrices import matrixdicts, GUI_matrix # pylint: disable=import-error
    from raycalc.matrixcalc import BeamTrace, calcq      # pylint: disable=import-error
    from GUI_PlotOptions import PlotOptions              # pylint: disable=import-error
else:
    try:
        from .raycalc.matrices import matrixdicts, GUI_matrix
        from .raycalc.matrixcalc import BeamTrace, calcq
        from .GUI_PlotOptions import PlotOptions
    except ImportError:
        print("ImportError, retrying without relative import")
        from raycalc.matrices import matrixdicts, GUI_matrix
        from raycalc.matrixcalc import BeamTrace, calcq
        from GUI_PlotOptions import PlotOptions
        print("Import successful")

class LineParameter:
    """tkinter widget for a single optical beamline parameter"""
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

        self.combo_vals = [key for (key,value) in matrixdicts.items()]
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

        self.func = matrixdicts[self.get_function()]["func"]
        self.ABCDhor = None
        self.ABCDver = None

    def init_fields(self):
        """Initialise the default input fields for the component"""
        i = 0
        for param in matrixdicts[self.get_function()]["params"]:
            self.fields[i] = {}
            self.fields[i]["label"] = ttk.Label(self.frame, text=param)
            self.fields[i]["label"].grid(row=i+1, column=0, padx=5)
            self.fields[i]["val"] = tk.DoubleVar(value=1)
            self.fields[i]["elem"] = ttk.Entry(self.frame, textvariable=self.fields[i]["val"])
            self.fields[i]["elem"].grid(row=i+1, column=1, padx=5)
            i += 1

        horver = matrixdicts[self.get_function()]["horver"]
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
        self.func = matrixdicts[self.get_function()]["func"]

        matrixparams = {}
        matrixparams["func"] = self.component.get()
        for key in self.fields: # pylint: disable=consider-using-dict-items
            param = self.fields[key]["label"]["text"]
            matrixparams[param] = self.fields[key]["val"].get()

        matrixparams["hor"] = self.hor.get()
        matrixparams["ver"] = self.ver.get()

        # A bit dirty, should be redone when the matrixcalc functions are rewritten.
        try:
            ABCD = GUI_matrix(matrixparams) # pylint: disable=invalid-name
            self.ABCDhor = ABCD["hor"]
            self.ABCDver = ABCD["ver"]

        except Exception as e: #pylint: disable=broad-except
            print("Error in calc_ABCD:",e)
            self.ABCDhor = None
            self.ABCDver = None

        if self.DEBUG:
            print(f"Matrices in component {self.compid}:\n\
                    ABCDhor: {self.ABCDhor}\n\
                    ABCDver: {self.ABCDver}")

        return (self.ABCDhor, self.ABCDver)

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

class GUI_OptLineProto: # pylint: disable=invalid-name
    """tkinter widget prototype for Optical Line style elements"""
    def __init__(self,
                 parent,
                 parentframe,
                 compid = 0,
                 location = (0,0),
                 inputDict = None,
                 DEBUG = False):
        """Initialise the Optical Line widget
        parent: parent widget
        parentframe: parent frame to place the widget in
        compid: id of the widget
        location: grid location of the widget
        inputDict: dictionary of input parameters for the optical line, 
                   format: {"param": tk.DoubleVar(value = 0)}
        """

        self.parent = parent
        self.compid = compid
        self.DEBUG = DEBUG
        self.frame = ttk.LabelFrame(parentframe, text = "Controls")
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        ### PLOT OPTIONS ###
        self.PlotOptWindow = None
        self.plotoptions = {
            "hor": {"color": "red"},
            "ver": {"color": "blue"}
        }

        if hasattr(parent, "linesamples"):
            self.samples = parent.linesamples
        else:
            self.samples = tk.IntVar(value=100)

        if hasattr(parent, "givecolor"):
            # If available, fetch line colors from parent
            colors = parent.givecolor(n = 2)
            self.plotoptions["hor"]["color"] = colors[0]
            self.plotoptions["ver"]["color"] = colors[1]


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

        self.add_button = ttk.Button(self.button_frame,
                                     text="Add Parameter",
                                     command=self.add_parameter)
        self.add_button.grid(row=0, column=1, padx=5)

        self.showhide_button = ttk.Button(self.button_frame,
                                          text="Show/Hide",
                                          command=self.showhide)
        self.showhide_button.grid(row=0, column=2, padx=5)

        # Add ver and hor plot tickboxes
        self.plotoptions["ver"]["plot"] = tk.IntVar(value = 1)
        self.ver_check = ttk.Checkbutton(self.button_frame,
                                         text="Vertical",
                                         variable=self.plotoptions["ver"]["plot"])
        self.ver_check.grid(row=1, column=0, padx=5)
        self.plotoptions["hor"]["plot"] = tk.IntVar(value = 1)
        self.hor_check = ttk.Checkbutton(self.button_frame,
                                         text="Horizontal",
                                         variable=self.plotoptions["hor"]["plot"])
        self.hor_check.grid(row=1, column=1, padx=5)
        # Set up references to hor and ver for convenience
        self.hor = self.plotoptions["hor"]["plot"]
        self.ver = self.plotoptions["ver"]["plot"]

        # Plot config button
        self.replot_button = ttk.Button(self.button_frame,
                                        text="Plot config",
                                        command=self.plotconfig)
        self.replot_button.grid(row=1, column=2, padx=5)
        ### END BUTTON FRAME ###

        ### INPUT BEAM FRAME###
        self.inputframe = ttk.LabelFrame(self.frame, text="Input beam parameters", relief=tk.RIDGE)
        self.inputframe.grid(row=1, column=0, pady=5, sticky="news")
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.rowconfigure(0, weight=1)

        if inputDict is None:
            # Default to open beamline
            self.input = {"Zhor": tk.DoubleVar(value=0), # Distance from waist
                          "Zver": tk.DoubleVar(value=0), # Distance from waist
                          "ZRhor": tk.DoubleVar(value=0), # Rayleigh length
                          "ZRver": tk.DoubleVar(value=0), # Rayleigh length
                          "Whor": tk.DoubleVar(value=1E-3), # Beam waist
                          "Wver": tk.DoubleVar(value=1E-3), # Beam waist
                          "lam": tk.DoubleVar(value=972E-9), # Wavelength
                          "n": tk.DoubleVar(value=1), # Refractive index
                          "x_offset": tk.DoubleVar(value=0)} # Offset in x
        else:
            self.input = inputDict
        self.input_widgets = {}
        i = 0
        for key in self.input:
            self.input_widgets[key] = ttk.Label(self.inputframe, text=key)
            self.input_widgets[key].grid(row=int(i/2), column=2*(i%2), padx=5)
            self.input_widgets[f"{key}_entry"] = ttk.Entry(self.inputframe,
                                                           textvariable=self.input[key])
            self.input_widgets[f"{key}_entry"].grid(row=int(i/2), column=2*(i%2)+1, padx=5)
            i += 1

        ### END INPUT BEAM FRAME ###

        ### COMPONENT FRAME ###
        self.componentframe = ttk.LabelFrame(self.frame, text="Optical Line")#, relief=tk.RIDGE)
        self.componentframe.grid(row=2, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.parameters = []
        ### END COMPONENT FRAME ###

        ### Matrix calc variables ###
        # Starting q values
        self.qhor = 0
        self.qver = 0
        # ABCD matrices for the optical line
        self.matrices_hor = []
        self.matrices_ver = []
        # BeamTrace objects for the optical line
        # Will be initialized on first replot
        self.horline = None
        self.verline = None
        # Plot data for the optical line, stored in dictionary along with plotoptions
        self.plotdata = {}


    def add_parameter(self):
        """Add a new component to the optical line"""
        newcompid = len(self.parameters)
        new_parameter = LineParameter(parent = self,
                                      parentframe = self.componentframe,
                                      compid = newcompid,
                                      DEBUG = self.DEBUG)
        self.parameters.append(new_parameter)
        self.componentframe.rowconfigure(self.compid, weight=1)

    def destroyLineParam(self, compid):
        """Destroy a component in the optical line"""
        param = self.parameters.pop(compid)
        param.frame.destroy()
        del param
        # Renumber the parameters
        for i, param in enumerate(self.parameters):
            param.compid = i

    def showhide(self):
        """Show or hide the optical line components"""
        if self.componentframe.winfo_ismapped():
            self.componentframe.grid_remove()
        else:
            self.componentframe.grid()

    def calcqs(self):
        """Calculate the q parameters for the optical line"""
        self.qhor = calcq(Z = self.input["Zhor"].get(),
                          ZR = self.input["ZRhor"].get(),
                          lam = self.input["lam"].get(),
                          W = self.input["Whor"].get(),
                          n = self.input["n"].get())
        self.qver = calcq(Z = self.input["Zver"].get(),
                          ZR = self.input["ZRver"].get(),
                          lam = self.input["lam"].get(),
                          W = self.input["Wver"].get(),
                          n = self.input["n"].get())
        print(f"qhor: {self.qhor}, qver: {self.qver}")

    def calculate_beamshape(self):
        """Calculate the beam shape of the optical line"""
        if self.DEBUG:
            print(f"Calculating beam shape with {self.samples.get()} samples")

        # Calculate qhor and qver
        self.calcqs()

        if self.plotoptions["hor"]["plot"].get():
            if self.DEBUG:
                print("Constructing Horizontal")
            # Calculate the fundamental mode waists:
            self.horline = BeamTrace(self.matrices_hor,
                                     self.qhor,
                                     n_points = self.samples.get(),
                                     lda = self.input["lam"].get())
            self.horline.constructRey()
        if self.plotoptions["ver"]["plot"].get():
            if self.DEBUG:
                print("Constructing Vertical")
            self.verline = BeamTrace(self.matrices_ver,
                                        self.qver,
                                        n_points = self.samples.get(),
                                        lda = self.input["lam"].get())
            self.verline.constructRey()
        if self.DEBUG:
            print("Beam shape calculated")

    def buildMatrixList(self):
        """Fetch the ABCD matrices from the components and build the matrix list"""
        self.matrices_hor = []
        self.matrices_ver = []
        for param in self.parameters:
            hor, ver = param.calc_ABCD()
            self.matrices_hor.append(hor)
            self.matrices_ver.append(ver)
        if self.DEBUG:
            print(self.matrices_hor)
            print(self.matrices_ver)

    def update_options(self):
        """Update the plotoptions to current values before replotting"""
        self.plotoptions["hor"]["title"] = f"{self.name.get()} hor"
        self.plotoptions["ver"]["title"] = f"{self.name.get()} ver"

    def replot(self, n = 1000):
        """Replot the optical line"""
        self.samples.set(n)
        self.buildMatrixList()
        self.calculate_beamshape()
        self.update_options()
        self.plotdata = {}
        if "x_offset" in self.input:
            offset = self.input["x_offset"].get()
        else:
            offset = 0
        if self.hor.get():
            self.plotdata["hor"] = {}
            # Check whether the x_offset parameter exists in current input
            self.plotdata["hor"]["x"] = self.horline.xs + offset
            self.plotdata["hor"]["w"] = self.horline.ws
        if self.ver.get():
            self.plotdata["ver"] = {}
            self.plotdata["ver"]["x"] = self.verline.xs + offset
            self.plotdata["ver"]["w"] = self.verline.ws
        self.plotdata["plotoptions"] = self.plotoptions
        if self.DEBUG:
            print(f"plotdata keys: {self.plotdata.keys()}")
        if self.DEBUG:
            print(f"plotdata: {self.plotdata}")
        return self.plotdata

    def plotconfig(self):
        """Open the plot configuration window"""
        print(self.PlotOptWindow)
        if self.PlotOptWindow is None:
            self.PlotOptWindow = PlotOptions(parent = self, plotoptions = self.plotoptions)
        else:
            self.PlotOptWindow.root.lift()

    def savestate(self):
        """Save the state of the optical line and components in a dictionary"""
        state = {}
        state["name"] = self.name.get()
        state["samples"] = self.samples.get()
        state["hor"] = self.hor.get()
        state["ver"] = self.ver.get()
        state["input"] = {}
        for key in self.input:
            state["input"][key] = self.input[key].get()
        state["parameters"] = []
        for param in self.parameters:
            state["parameters"].append(param.savestate())
        # For saving the plotoptions, convert the tk.IntVar to int
        state["plotoptions"] = {"hor":{
                                    "plot": self.plotoptions["hor"]["plot"].get(),
                                    "color": self.plotoptions["hor"]["color"],
                                    "title": self.plotoptions["hor"]["title"]},
                                "ver":{
                                    "plot": self.plotoptions["ver"]["plot"].get(),
                                    "color": self.plotoptions["ver"]["color"],
                                    "title": self.plotoptions["ver"]["title"]}
                                }
        for horver in state["plotoptions"]:
            state["plotoptions"][horver]["plot"] = self.plotoptions[horver]["plot"].get()
        return state

    def loadstate(self, state):
        """Load the state of the optical line and components from a dictionary"""
        self.name.set(state["name"])
        self.samples.set(state["samples"])
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        # For loading the plotoptions, convert the int to tk.IntVar
        if "plotoptions" in state:
            for horver in state["plotoptions"]:
                self.plotoptions[horver]["plot"].set(state["plotoptions"][horver]["plot"])
                self.plotoptions[horver]["color"] = state["plotoptions"][horver]["color"]
                self.plotoptions[horver]["title"] = state["plotoptions"][horver]["title"]
        for key in self.input:
            self.input[key].set(state["input"][key])
        for param in state["parameters"]:
            self.add_parameter()
            self.parameters[-1].loadstate(param)

def test():
    """Test function for the Optical Line widget"""
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optline = GUI_OptLineProto(root, root, compid = 0, location = (0,0)) # pylint: disable=unused-variable
    root.mainloop()

if __name__ == "__main__":
    test()
