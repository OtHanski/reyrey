import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Import the GUI component prototypes and init functions
from GUI_components.GUI_lineslist import *

# Import filehandler
import utils.FileHandler as fh

debug = False

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter with Matplotlib")

        # Bind the window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Create a main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create a sidebar frame
        self.sidebar = ttk.Frame(root, width=200)
        self.sidebar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame to hold the add and remove buttons
        button_frame = ttk.Frame(self.sidebar)
        button_frame.pack(pady=5)

        # Add buttons to add and remove parameter lines
        self.add_button = ttk.Button(button_frame, text="Save", command=self.savestate)
        self.add_button.grid(row=0, column=0, padx=5)
        self.add_button = ttk.Button(button_frame, text="Load", command=self.loadstate)
        self.add_button.grid(row=0, column=1, padx=5)
        self.update_button = ttk.Button(button_frame, text="Replot", command=self.update_plot)
        self.update_button.grid(row=0, column=2, padx=5)

        # Add ver and hor plot tickboxes
        self.ver = tk.IntVar(value = 1)
        self.ver_check = ttk.Checkbutton(button_frame, text="Vertical", variable=self.ver)
        self.ver_check.grid(row = 1, column = 0, padx=5)
        self.hor = tk.IntVar(value = 1)
        self.hor_check = ttk.Checkbutton(button_frame, text="Horizontal", variable=self.hor)
        self.hor_check.grid(row = 1, column = 1, padx=5)

        # Scrollable canvas for parameters
        self.paramcanvas = tk.Canvas(self.sidebar, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.sidebar, orient="vertical", command=self.paramcanvas.yview)
        self.parameters_frame = ttk.Frame(self.paramcanvas)
        self.parameters_frame.bind("<Configure>", self.on_frame_configure)
        self.paramcanvas.create_window((0, 0), window=self.parameters_frame, anchor="nw")
        self.paramcanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.paramcanvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add the lineslist element to hold the actual optical lines
        self.lineslist = LineGUI(self, self.parameters_frame, id = 0)

        # List to hold parameter entries
        self.parameters = []

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.lines = []
        # Add X and Y labels
        self.ax.set_xlabel("Distance (m)")
        self.ax.set_ylabel("Beam Waist (mm)")

        # Create a canvas and add the figure to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_plot(self):
        # Clear the current plot
        for line in self.ax.get_lines():
            line.remove()
        # Create/reset an object to hold the lines
        self.lines = []
        xydat = self.lineslist.replot()
        if debug:
            print(f"xydat keys: {xydat.keys()}")
            print(f"xydat values: {xydat[0]}")
        for optline in xydat:
            # Plot vertical and/or horizontal as provided
            for horver in xydat[optline]:
                line = self.ax.plot(np.array(xydat[optline][horver]["x"]), np.array(xydat[optline][horver]["w"])*1E3)
                self.lines.append(line)
        
        # Add legend to the legend frame
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)

        # Redraw the plot
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def on_frame_configure(self, event):
        self.paramcanvas.configure(scrollregion=self.paramcanvas.bbox("all"))

    def on_closing(self):
        # Properly close the Matplotlib figure
        plt.close(self.fig)
        self.root.destroy()
    
    def savestate(self):
        # Save the state of the GUI in dict for loading
        state = {}
        state["horver"] = (self.hor.get(), self.ver.get())
        state["OptLines"] = self.lineslist.savestate()
        if debug: print(state)

        fh.WriteJson(fh.SaveFileAs("./savestates"), state)
    
    def loadstate(self):
        # Load the state of the GUI from a dict
        state = fh.ReadJson(fh.ChooseSingleFile(initdir = "./savestates"))
        self.hor.set(state["horver"][0])
        self.ver.set(state["horver"][1])
        self.lineslist.loadstate(state["OptLines"])
        self.update_plot()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()