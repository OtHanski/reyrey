#pylint: disable=invalid-name
"""Implements the basic OpticalLine class, a class to handle the optical line GUI components.
ATM a bit redundant as it is also the default of GUI_OptLineProto"""

import tkinter as tk

# Import the GUI component prototypes and init functions
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from GUI_OptLineProto import GUI_OptLineProto # pylint: disable=import-error
else:
    try:
        from .GUI_OptLineProto import GUI_OptLineProto
    except ImportError:
        print("ImportError, retrying without relative import")
        from GUI_components.GUI_OptLineProto import GUI_OptLineProto
        print("Import successful")

debug = False

class OpticalLine(GUI_OptLineProto):
    """Default optical beamline implementation"""
    def __init__(self, parent, parentframe,  compid = 0, location = (0,0)): # pylint: disable=useless-super-delegation
        super().__init__(parent, parentframe, compid, location)

def test():
    """Test function for OpticalLine"""
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = OpticalLine(root,root) #pylint: disable=unused-variable
    root.mainloop()

if __name__ == "__main__":
    test()
