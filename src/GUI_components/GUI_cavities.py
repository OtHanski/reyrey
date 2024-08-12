import tkinter as tk
from tkinter import ttk
from math import radians

# Import the GUI component prototypes and init functions 
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from raytracing.matrices import ringCavity, linCavity
    from raytracing.matrixcalc import BeamTrace, calcq, cavityq, buildMatrixList, compositeABCD
else:
    from .raytracing.matrices import ringCavity, linCavity
    from .raytracing.matrixcalc import BeamTrace, calcq, cavityq, buildMatrixList, compositeABCD

debug = False

class RibbonCavity:
    """tkinter widget for a single optical line"""
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self.parent = parent
        self.id = id
        self.frame = ttk.LabelFrame(parentframe, text = "Controls")#, relief=tk.RIDGE)
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        if hasattr(parent, "linesamples"):
            self.samples = parent.linesamples
        else: 
            self.samples = tk.IntVar(value=100)
        
        # Update flag should be a tk.IntVar toggle to tag the plot for update.
        if updateFlag:
            self.updateFlag = updateFlag
        else:
            self.updateFlag = tk.IntVar(value=0)


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
        self.ver = tk.IntVar(value = 1)
        self.ver_check = ttk.Checkbutton(self.button_frame, text="Vertical", variable=self.ver)
        self.ver_check.grid(row=1, column=0, padx=5)
        self.hor = tk.IntVar(value = 1)
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

        # l_focus = 61.6E-3, l_free = 69.3E-3, l_crystal = 15E-3, R = 50E-3, n_crystal = 1.567, theta = radians(18.2)
        self.input = {"lam": tk.DoubleVar(value = 972E-9), # Wavelength
                      "l_focus": tk.DoubleVar(value=61.6E-3), # Distance from waist
                      "l_free": tk.DoubleVar(value=69.3E-3), # Distance from waist
                      "l_crystal": tk.DoubleVar(value=15E-3), # Rayleigh length
                      "R_foc": tk.DoubleVar(value=50E-3), # Rayleigh length
                      "n_SHG": tk.DoubleVar(value=1.567), # Refractive index of SHG crystal
                      "θ (deg)": tk.DoubleVar(value=10), # R mirror Incidence angle
                      #"h": tk.DoubleVar(value=972E-9), # Cavity height
                      "x_offset": tk.DoubleVar(value=0)} # Refractive index
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
        #new_parameter = LineParameter(self, self.componentframe, id)
        #self.parameters.append(new_parameter)
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
        # Calculate the beam shape at the end of the optical line
        if debug:
            print(f"Calculating beam shape with {self.samples.get()} samples")
        
        if self.hor.get():
            if debug: print("Constructing Horizontal")
            # Calculate the fundamental mode waist:
            whor = cavityq(self.horABCD)
            self.horline = BeamTrace(self.matrices_hor, 
                                     whor*1j,
                                     n_points = self.samples.get(), 
                                     lda = self.input["lam"].get())
            self.horline.constructRey()
        if self.ver.get():
            if debug: print("Constructing Vertical")
            wver = cavityq(self.verABCD)
            self.verline = BeamTrace(self.matrices_ver, 
                                        wver*1j,
                                        n_points = self.samples.get(), 
                                        lda = self.input["lam"].get())
            self.verline.constructRey()
        if debug:
            print("Beam shape calculated")
        #self.zrhor = rey.z_r(self.whor, self.input["lam"].get())
        #self.zrver = rey.z_r(self.wver, self.input["lam"].get())

    def replot(self, n = 1000):
        self.samples.set(n)
        self.matrices = ringCavity(l_focus = self.input["l_focus"].get(), # Distance between curved focus mirrors
                                   l_free = self.input["l_free"].get(), # Free arm length (l_cav-l_focus)
                                   l_crystal = self.input["l_crystal"].get(), # SHG crystal length
                                   R = self.input["R_foc"].get(), # Curvature radius of curved mirrors
                                   n_crystal = self.input["n_SHG"].get(), # Refractive index of SHG crystal
                                   theta = radians(self.input["θ (deg)"].get())) # Angle of incidence on curved mirrors
        self.matrices_hor = buildMatrixList(self.matrices["hor"])
        self.matrices_ver = buildMatrixList(self.matrices["ver"])
        self.horABCD = compositeABCD(self.matrices_hor)
        self.verABCD = compositeABCD(self.matrices_ver)

        self.calculate_beamshape()
        self.plotdata = {}
        if self.hor.get():
            self.plotdata["hor"] = {}
            self.plotdata["hor"]["x"] = self.horline.xs + self.input["x_offset"].get()
            self.plotdata["hor"]["w"] = self.horline.ws
        if self.ver.get():
            self.plotdata["ver"] = {}
            self.plotdata["ver"]["x"] = self.verline.xs + self.input["x_offset"].get()
            self.plotdata["ver"]["w"] = self.verline.ws
        if debug: print(f"plotdata keys: {self.plotdata.keys()}")
        if debug: print(f"plotdata: {self.plotdata}")
        return self.plotdata
    
    def savestate(self):
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
        return state
    
    def loadstate(self, state):
        self.name.set(state["name"])
        self.samples.set(state["samples"])
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        for key in self.input:
            self.input[key].set(state["input"][key])
        for param in state["parameters"]:
            self.add_parameter()
            self.parameters[-1].loadstate(param)

class LinCavity:
    """tkinter widget for a single optical line"""
    def __init__(self, parent, parentframe,  id = 0, location = (0,0), updateFlag = None):
        self.parent = parent
        self.id = id
        self.frame = ttk.LabelFrame(parentframe, text = "Controls")#, relief=tk.RIDGE)
        self.frame.grid(row=location[0], column=location[1], pady=5, sticky="news")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        if hasattr(parent, "linesamples"):
            self.samples = parent.linesamples
        else: 
            self.samples = tk.IntVar(value=100)
        
        # Update flag should be a tk.IntVar toggle to tag the plot for update.
        if updateFlag:
            self.updateFlag = updateFlag
        else:
            self.updateFlag = tk.IntVar(value=0)


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
        self.ver = tk.IntVar(value = 1)
        self.ver_check = ttk.Checkbutton(self.button_frame, text="Vertical", variable=self.ver)
        self.ver_check.grid(row=1, column=0, padx=5)
        self.hor = tk.IntVar(value = 1)
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
        self.input = {"Zhor": tk.DoubleVar(value=0), # Distance from waist
                      "Zver": tk.DoubleVar(value=0), # Distance from waist
                      "ZRhor": tk.DoubleVar(value=0), # Rayleigh length
                      "ZRver": tk.DoubleVar(value=0), # Rayleigh length
                      "Whor": tk.DoubleVar(value=1E-3), # Beam waist
                      "Wver": tk.DoubleVar(value=1E-3), # Beam waist
                      "lam": tk.DoubleVar(value=972E-9), # Wavelength
                      "n": tk.DoubleVar(value=1)} # Refractive index
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
        # Calculate the beam shape at the end of the optical line
        if debug:
            print(f"Calculating beam shape with {self.samples.get()} samples")
        
        if self.hor.get():
            if debug: print("Constructing Horizontal")
            self.horline = BeamTrace(self.matrices_hor, 
                                     calcq(Z = self.input["Zhor"].get(), lam = self.input["lam"].get(), W = self.input["Whor"].get(), n = self.input["n"].get()),
                                     n_points = self.samples.get(), 
                                     lda = self.input["lam"].get())
            self.horline.constructRey()
        if self.ver.get():
            if debug: print("Constructing Vertical")
            self.verline = BeamTrace(self.matrices_ver, 
                                        calcq(Z = self.input["Zver"].get(), lam = self.input["lam"].get(), W = self.input["Wver"].get(), n = self.input["n"].get()),
                                        n_points = self.samples.get(), 
                                        lda = self.input["lam"].get())
            self.verline.constructRey()
        if debug:
            print("Beam shape calculated")
        #self.zrhor = rey.z_r(self.whor, self.input["lam"].get())
        #self.zrver = rey.z_r(self.wver, self.input["lam"].get())

    def replot(self, n = 1000):
        self.samples.set(n)
        self.matrices_hor = []
        self.matrices_ver = []
        for param in self.parameters:
            hor, ver = param.calc_ABCD()
            self.matrices_hor.append(hor)
            self.matrices_ver.append(ver)
        if debug:
            print(self.matrices_hor)
            print(self.matrices_ver)

        self.matrices_hor.reverse()
        self.matrices_ver.reverse()
        self.calculate_beamshape()
        self.plotdata = {}
        if self.hor.get():
            self.plotdata["hor"] = {}
            self.plotdata["hor"]["x"] = self.horline.xs
            self.plotdata["hor"]["w"] = self.horline.ws
        if self.ver.get():
            self.plotdata["ver"] = {}
            self.plotdata["ver"]["x"] = self.verline.xs
            self.plotdata["ver"]["w"] = self.verline.ws
        if debug: print(f"plotdata keys: {self.plotdata.keys()}")
        return self.plotdata
    
    def savestate(self):
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
        return state
    
    def loadstate(self, state):
        self.name.set(state["name"])
        self.samples.set(state["samples"])
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        for key in self.input:
            self.input[key].set(state["input"][key])
        for param in state["parameters"]:
            self.add_parameter()
            self.parameters[-1].loadstate(param)

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    ribbon = RibbonCavity(root, root, id = 0, location = (0,0))
    lin = LinCavity(root, root, id = 1, location = (0,1))
    root.mainloop()

if __name__ == "__main__":
    test()
    
    