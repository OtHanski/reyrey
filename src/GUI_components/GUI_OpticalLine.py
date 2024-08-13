import tkinter as tk
from tkinter import ttk

# Import the GUI component prototypes and init functions 
# format depends on whether this is run as a script or imported as a module
if __name__ == "__main__":
    from GUI_OptLineProto import GUI_OptLineProto
else:
    from .GUI_OptLineProto import GUI_OptLineProto

debug = False

class OpticalLine(GUI_OptLineProto):
    def __init__(self, parent, parentframe,  id = 0, location = (0,0)):
        super().__init__(parent, parentframe, id, location)

def test():
    root = tk.Tk()
    root.title("Optical Line Test")
    tk.Grid.rowconfigure(root, 0, weight=1)
    tk.Grid.columnconfigure(root, 0, weight=1)
    optical_line = OpticalLine(root)
    root.mainloop()

if __name__ == "__main__":
    test()
    
    