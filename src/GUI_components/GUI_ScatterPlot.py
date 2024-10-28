#pylint: disable=invalid-name
"""Implements the Scatterplot class, a class to handle test points for an optical line,
e.g. manual waist measurement points for fitting."""

import tkinter as tk

# Import the GUI component prototypes and init functions
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from GUI_OptLineProto import GUI_OptLineProto # pylint: disable=import-error
else:
    from .GUI_OptLineProto import GUI_OptLineProto

debug = False

class ScatterPlot(GUI_OptLineProto):
    """Default optical beamline implementation"""
    def __init__(self, parent, parentframe,  compid = 0, location = (0,0)): # pylint: disable=useless-super-delegation
        super().__init__(parent, parentframe, compid, location)
    
    def replot(self, n = 1000):
        """Overwrite the replot function to plot the scatter points"""
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

def test():
    """Test function for OpticalLine"""
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = ScatterPlot(root,root) #pylint: disable=unused-variable
    root.mainloop()

if __name__ == "__main__":
    test()
