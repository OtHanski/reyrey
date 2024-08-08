from copy import deepcopy
import tkinter as tk
from tkinter import ttk

from raytracing.matrices import matrixdicts, ringCavity, linCavity, GUI_matrix
import raytracing.matrixcalc as rey

debug = True

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
        print("Removing fields")
        for i in list(self.fields):
            for key in list(self.fields[i]):
                if type(self.fields[i][key]) in [ttk.Label, ttk.Entry, ttk.Checkbutton]:
                    print(f"Destroying {key}")
                    self.fields[i][key].destroy()
                del self.fields[i][key]
        print("Removing horverchecks")
        for key in list(self.horverchecks):
            if type(self.horverchecks[key]) in [ttk.Checkbutton]:
                print(f"Destroying {key}")
                self.horverchecks[key].destroy()
            del self.horverchecks[key]
    
    def update_fields(self):
        print("Updating fields")
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

        try:
            if self.hor.get():
                self.ABCDhor = GUI_matrix(matrixparams)
            else:
                # If the component doesn't support horizontal, set ABCDhor to identity matrix
                self.ABCDhor = GUI_matrix({"func": "identity"})
            if self.ver.get():
                self.ABCDver = GUI_matrix(matrixparams)
            else:
                # If the component doesn't support vertical, set ABCDver to identity matrix
                self.ABCDver = GUI_matrix({"func": "identity"})
    
        except Exception as e:
            print("Error in calc_ABCD:",e)
            self.ABCDhor = None
            self.ABCDver = None

        if debug:
            print(f"Matrices in component {self.id}:\nABCDhor: {self.ABCDhor}\nABCDver: {self.ABCDver}")

        return (self.ABCDhor, self.ABCDver)
    
    def savestate(self):
        state = {}
        state["function"] = self.component.get()
        state["hor"] = self.hor.get()
        state["ver"] = self.ver.get()
        state["fields"] = {}
        for key in self.fields:
            state["fields"][key] = self.fields[key]["val"].get()
        return state
    
    def loadstate(self, state):
        self.component.set(state["function"])
        self.update_fields()
        self.hor.set(state["hor"])
        self.ver.set(state["ver"])
        if debug: 
            print(f"Loading state: {state}")
            print(f"Fields: {self.fields}")
        for key in self.fields:
            self.fields[key]["val"].set(state["fields"][str(key)])
        self.update_fields()


class OpticalLine:
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
        # Calculate the beam shape at the end of the optical line
        if debug:
            print(f"Calculating beam shape with {self.samples.get()} samples")
        
        if self.hor.get():
            if debug: print("Constructing Horizontal")
            self.horline = rey.BeamTrace(self.matrices_hor, 
                                     rey.calcq(Z = self.input["Zhor"].get(), lam = self.input["lam"].get(), W = self.input["Whor"].get(), n = self.input["n"].get()),
                                     n_points = self.samples.get(), 
                                     lda = self.input["lam"].get())
            self.horline.constructRey()
        if self.ver.get():
            if debug: print("Constructing Vertical")
            self.verline = rey.BeamTrace(self.matrices_ver, 
                                        rey.calcq(Z = self.input["Zver"].get(), lam = self.input["lam"].get(), W = self.input["Wver"].get(), n = self.input["n"].get()),
                                        n_points = self.samples.get(), 
                                        lda = self.input["lam"].get())
            self.verline.constructRey()
        if debug:
            print("Beam shape calculated")
        #self.zrhor = rey.z_r(self.whor, self.input["lam"].get())
        #self.zrver = rey.z_r(self.wver, self.input["lam"].get())

    def replot(self):
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
    optical_line = OpticalLine(root)
    root.mainloop()

if __name__ == "__main__":
    test()
    
    