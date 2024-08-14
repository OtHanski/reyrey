"""
Define the class prototype for Optical line implements in the GUI.
"""

import tkinter as tk
from tkinter import ttk

# Import the GUI component prototypes and init functions 
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from raycalc.matrices import matrixdicts, GUI_matrix
    from raycalc.matrixcalc import BeamTrace, calcq
    from GUI_plotoptions import PlotOptions
else:
    from .raycalc.matrices import matrixdicts, GUI_matrix
    from .raycalc.matrixcalc import BeamTrace, calcq
    from .GUI_plotoptions import PlotOptions

debug = False

class LineParameter:
    """tkinter widget for a single optical beamline parameter"""
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
        self.horverchecks = {}
        self.init_fields()
        
     
    def init_fields(self):
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
        self.horverchecks["hor_check"] = ttk.Checkbutton(self.frame, text="Horizontal", variable=self.hor)
        self.horverchecks["hor_check"].grid(row=i+1, column=0, padx=5)
        self.horverchecks["ver_check"] = ttk.Checkbutton(self.frame, text="Vertical", variable=self.ver)
        self.horverchecks["ver_check"].grid(row=i+1, column=1, padx=5)
        # Remove the hor and ver checkbuttons if the component doesn't support them
        if not horver:
            self.horverchecks["hor_check"].destroy()
            self.horverchecks["ver_check"].destroy()
    
    def remove_fields(self):
        # Wipe old UI elements to replace with new
        if debug: ("Removing fields")
        for i in list(self.fields):
            for key in list(self.fields[i]):
                if type(self.fields[i][key]) in [ttk.Label, ttk.Entry, ttk.Checkbutton]:
                    if debug: print(f"Destroying {key}")
                    self.fields[i][key].destroy()
                del self.fields[i][key]
        if debug: print("Removing horverchecks")
        for key in list(self.horverchecks):
            if type(self.horverchecks[key]) in [ttk.Checkbutton]:
                if debug: print(f"Destroying {key}")
                self.horverchecks[key].destroy()
            del self.horverchecks[key]
    
    def update_fields(self):
        if debug: print("Updating fields")
        self.remove_fields()
        self.init_fields()


    def remove(self):
        self.parent.destroyLineParam(self.id)


    def get_function(self):
        return self.component.get()
    
    def calc_ABCD(self):
        self.func = matrixdicts[self.get_function()]["func"]

        matrixparams = {}
        matrixparams["func"] = self.component.get()
        for key in self.fields:
            param = self.fields[key]["label"]["text"]
            matrixparams[param] = self.fields[key]["val"].get()

        matrixparams["hor"] = self.hor.get()
        matrixparams["ver"] = self.ver.get()

        try:
            ABCD = GUI_matrix(matrixparams)
            self.ABCDhor = ABCD["hor"]
            self.ABCDver = ABCD["ver"]
    
        except Exception as e:
            print("Error in calc_ABCD:",e)
            self.ABCDhor = None
            self.ABCDver = None

        if debug:
            print(f"Matrices in component {self.id}:\nABCDhor: {self.ABCDhor}\nABCDver: {self.ABCDver}")

        return (self.ABCDhor, self.ABCDver)
    
    def savestate(self):
        try:
            state = {}
            state["function"] = self.component.get()
            state["hor"] = self.hor.get()
            state["ver"] = self.ver.get()
            state["fields"] = {}
            for key in self.fields:
                state["fields"][key] = self.fields[key]["val"].get()
            return state
        except Exception as e:
            print("Error in savestate:",e)
            print("State:",state)
            print("Fields:",self.fields)
    
    def loadstate(self, state):
        self.component.set(state["function"])
        self.update_fields()
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        if debug: 
            print(f"Loading state: {state}")
            print(f"Fields: {self.fields}")
        for key in self.fields:
            if debug:
                print(f"Setting field {key} to {state['fields'][str(key)]}")
                print(f"Field: {self.fields[key]["val"]}")
            self.fields[key]["val"].set(state["fields"][str(key)])
            print(self.fields[key]["val"].get())

class GUI_OptLineProto:
    """tkinter widget prototype for Optical Line style elements"""
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), inputDict = None):
        """Initialise the Optical Line widget
        parent: parent widget
        parentframe: parent frame to place the widget in
        id: id of the widget
        location: grid location of the widget
        inputDict: dictionary of input parameters for the optical line, format: {"param": tk.DoubleVar(value = 0)}
        """

        self.parent = parent
        self.id = id
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

        self.add_button = ttk.Button(self.button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.grid(row=0, column=1, padx=5)

        self.showhide_button = ttk.Button(self.button_frame, text="Show/Hide", command=self.showhide)
        self.showhide_button.grid(row=0, column=2, padx=5)
        
        # Add ver and hor plot tickboxes
        self.plotoptions["ver"]["plot"] = tk.IntVar(value = 1)
        self.ver_check = ttk.Checkbutton(self.button_frame, text="Vertical", variable=self.plotoptions["ver"]["plot"])
        self.ver_check.grid(row=1, column=0, padx=5)
        self.plotoptions["hor"]["plot"] = tk.IntVar(value = 1)
        self.hor_check = ttk.Checkbutton(self.button_frame, text="Horizontal", variable=self.plotoptions["hor"]["plot"])
        self.hor_check.grid(row=1, column=1, padx=5)
        # Set up references to hor and ver for convenience
        self.hor = self.plotoptions["hor"]["plot"]
        self.ver = self.plotoptions["ver"]["plot"]

        # Plot config button
        self.replot_button = ttk.Button(self.button_frame, text="Plot config", command=self.plotconfig)
        self.replot_button.grid(row=1, column=2, padx=5)
        ### END BUTTON FRAME ###

        ### INPUT BEAM FRAME###
        self.inputframe = ttk.LabelFrame(self.frame, text="Cavity parameters", relief=tk.RIDGE)
        self.inputframe.grid(row=1, column=0, pady=5, sticky="news")
        self.inputframe.columnconfigure(0, weight=1)
        self.inputframe.rowconfigure(0, weight=1)

        if inputDict is None:
            # Default to open beamline
            # l_focus = 61.6E-3, l_free = 69.3E-3, l_crystal = 15E-3, R = 50E-3, n_crystal = 1.567, theta = radians(18.2)
            self.input = {"Zhor": tk.DoubleVar(value=0), # Distance from waist
                          "Zver": tk.DoubleVar(value=0), # Distance from waist
                          "ZRhor": tk.DoubleVar(value=0), # Rayleigh length
                          "ZRver": tk.DoubleVar(value=0), # Rayleigh length
                          "Whor": tk.DoubleVar(value=1E-3), # Beam waist
                          "Wver": tk.DoubleVar(value=1E-3), # Beam waist
                          "lam": tk.DoubleVar(value=972E-9), # Wavelength
                          "n": tk.DoubleVar(value=1)} # Refractive index
        else:
            self.input = inputDict
        self.input_widgets = {}
        i = 0
        for key in self.input:
            self.input_widgets[key] = ttk.Label(self.inputframe, text=key)
            self.input_widgets[key].grid(row=int(i/2), column=2*(i%2), padx=5)
            self.input_widgets[f"{key}_entry"] = ttk.Entry(self.inputframe, textvariable=self.input[key])
            self.input_widgets[f"{key}_entry"].grid(row=int(i/2), column=2*(i%2)+1, padx=5)
            i += 1

        ### END INPUT BEAM FRAME ###

        ### COMPONENT FRAME ###
        self.componentframe = ttk.LabelFrame(self.frame, text="Optical Line")#, relief=tk.RIDGE)
        self.componentframe.grid(row=2, column=0, pady=5, sticky="news")
        self.componentframe.columnconfigure(0, weight=1)

        self.parameters = []
        ### END COMPONENT FRAME ###


    def add_parameter(self):
        id = len(self.parameters)
        new_parameter = LineParameter(self, self.componentframe, id)
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
        # Show or hide the optical line components
        if self.componentframe.winfo_ismapped():
            self.componentframe.grid_remove()
        else:
            self.componentframe.grid()

    def calcqs(self):
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
        # Calculate the beam shape at the end of the optical line
        if debug:
            print(f"Calculating beam shape with {self.samples.get()} samples")
        
        # Calculate qhor and qver
        self.calcqs()

        if self.plotoptions["hor"]["plot"].get():
            if debug: print("Constructing Horizontal")
            # Calculate the fundamental mode waists:
            self.horline = BeamTrace(self.matrices_hor, 
                                     self.qhor,
                                     n_points = self.samples.get(), 
                                     lda = self.input["lam"].get())
            self.horline.constructRey()
        if self.plotoptions["ver"]["plot"].get():
            if debug: print("Constructing Vertical")
            self.verline = BeamTrace(self.matrices_ver, 
                                        self.qver,
                                        n_points = self.samples.get(), 
                                        lda = self.input["lam"].get())
            self.verline.constructRey()
        if debug:
            print("Beam shape calculated")
    
    def buildMatrixList(self):
        # Fetch the ABCD matrices from the components and build the matrix list
        self.matrices_hor = []
        self.matrices_ver = []
        for param in self.parameters:
            hor, ver = param.calc_ABCD()
            self.matrices_hor.append(hor)
            self.matrices_ver.append(ver)
        if debug:
            print(self.matrices_hor)
            print(self.matrices_ver)
    
    def update_options(self):
        # Update the plotoptions to current values before replotting
        self.plotoptions["hor"]["title"] = f"{self.name.get()} hor"
        self.plotoptions["ver"]["title"] = f"{self.name.get()} ver"

    def replot(self, n = 1000):
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
        if debug: print(f"plotdata keys: {self.plotdata.keys()}")
        if debug: print(f"plotdata: {self.plotdata}")
        return self.plotdata

    def plotconfig(self):
        if self.PlotOptWindow is None:
            self.PlotOptWindow = PlotOptions(parent = self, plotoptions = self.plotoptions)
        else:
            self.PlotOptWindow.root.lift()
    
    def setplotoptions(self, plotoptions):
        print(self.plotoptions)
    
    def savestate(self):
        state = {}
        state["name"] = self.name.get()
        state["samples"] = self.samples.get()
        state["hor"] = self.hor.get()
        state["ver"] = self.ver.get()
        state["plotoptions"] = self.plotoptions
        state["input"] = {}
        for key in self.input:
            state["input"][key] = self.input[key].get()
        state["parameters"] = []
        for param in self.parameters:
            state["parameters"].append(param.savestate())
        return state
    
    def loadstate(self, state):
        self.name.set(state["name"])
        self.samples.set(state["samples"])
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        if "plotoptions" in state:
            self.plotoptions = state["plotoptions"]
        for key in self.input:
            self.input[key].set(state["input"][key])
        for param in state["parameters"]:
            self.add_parameter()
            self.parameters[-1].loadstate(param)