import tkinter as tk
from tkinter import ttk
from math import radians

# Import the GUI component prototypes and init functions 
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from raycalc.matrices import ringCavity, linCavity
    from raycalc.matrixcalc import cavityq, buildMatrixList, compositeABCD
    from GUI_OptLineProto import GUI_OptLineProto
else:
    from .raycalc.matrices import ringCavity, linCavity
    from .raycalc.matrixcalc import  cavityq, buildMatrixList, compositeABCD
    from .GUI_OptLineProto import GUI_OptLineProto

debug = False

class RibbonCavity(GUI_OptLineProto):
    def __init__(self, parent, parentframe,  id = 0, location = (0,0)):
        self.input = {"lam": tk.DoubleVar(value = 972E-9), # Wavelength
                      "l_focus": tk.DoubleVar(value=61.6E-3), # Distance from waist
                      "l_free": tk.DoubleVar(value=69.3E-3), # Distance from waist
                      "l_crystal": tk.DoubleVar(value=15E-3), # Rayleigh length
                      "R_foc": tk.DoubleVar(value=50E-3), # Rayleigh length
                      "n_SHG": tk.DoubleVar(value=1.567), # Refractive index of SHG crystal
                      "θ (deg)": tk.DoubleVar(value=10), # R mirror Incidence angle
                      "x_offset": tk.DoubleVar(value=0)} # Refractive index
        super().__init__(parent, parentframe, id, location, inputDict=self.input)
        self.add_button.destroy()

    def showhide(self):
        # Override default behaviour to show/hide the inputframe instead of lineparams
        if self.inputframe.winfo_ismapped():
            self.inputframe.grid_remove()
        else:
            self.inputframe.grid()
    
    def calcqs(self):
        # Override default q calculation, based on the cavityq function
        whor = cavityq(self.horABCD)
        wver = cavityq(self.verABCD)

        self.qhor = whor*1j
        self.qver = wver*1j
    
    def buildMatrixList(self):
        # Override default Matrixlist building to handle the ringCavity format
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


def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    ribbon = RibbonCavity(root, root, id = 0, location = (0,0))
    #lin = LinCavity(root, root, id = 1, location = (0,1))
    root.mainloop()

if __name__ == "__main__":
    test()
    
    