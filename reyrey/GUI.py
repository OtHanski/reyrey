import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Import the GUI component prototypes and init functions
from GUI_prototypes import *
from GUI_lineslist import *

def generate_plot_dataA(x, ui_elements):
    amplitude = ui_elements["amplitude"]["val"].get()
    frequency = ui_elements["frequency"]["val"].get()
    return amplitude * np.sin(frequency * x)

def generate_plot_dataB(x, ui_elements):
    amplitude = ui_elements["amplitude"]["val"].get()
    frequency = ui_elements["frequency"]["val"].get()
    phase = ui_elements["phase"]["val"].get()
    return amplitude * np.cos(frequency * x + phase)

def Optical_Line(x, ui_elements):
    return x

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
        self.add_button = ttk.Button(button_frame, text="Add Optical Line", command=self.add_optical_line)
        self.add_button.grid(row=0, column=0, padx=5)
        self.update_button = ttk.Button(button_frame, text="Update", command=self.update_plot)
        self.update_button.grid(row=0, column=1, padx=5)

        # Add ver and hor plot tickboxes
        self.ver = tk.IntVar()
        self.ver_check = ttk.Checkbutton(button_frame, text="Vertical", variable=self.ver)
        self.ver_check.grid(row = 1, column = 0, padx=5)
        self.hor = tk.IntVar()
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

        self.updateFlag = tk.IntVar(value=0)
        # Bind the updateFlag to the updateFlag_test function
        self.updateFlag.trace_add("write", self.updateFlag_test)
        self.lineslist = LineGUI(self, self.parameters_frame, id = 0, updateFlag = self.updateFlag)

        # List to hold parameter entries
        self.parameters = []

        # Create a figure and axis
        self.fig, self.ax = plt.subplots()
        self.x = np.linspace(0, 2 * np.pi, 100)
        self.lines = []

        # Create a canvas and add the figure to it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add the Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Frame to hold the sample control
        sample_frame = ttk.Frame(self.main_frame)
        sample_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Label(sample_frame, text="Number of Samples:").pack(side=tk.LEFT, padx=5)
        self.sample_var = tk.IntVar(value=100)
        self.sample_entry = ttk.Entry(sample_frame, textvariable=self.sample_var)
        self.sample_entry.pack(side=tk.LEFT, padx=5)

    def update_plot(self):
        self.lines = []
        num_samples = self.sample_var.get()
        xydat = self.lineslist.get_lines(num_samples)
        for data in xydat:
            # Plot vertical and/or horizontal as provided
            for horver in data:
                line = self.ax.plot(data["x"], data["y"])
                self.lines.append(line)
        
        """
        self.x = np.linspace(0, 2 * np.pi, num_samples)
        for line, (param_frame, ui_elements) in zip(self.lines, self.parameters):
            function_var = ui_elements["shared"]["function"]["val"]
            plot_function = self.get_selected_function(function_var.get())
            y = plot_function(self.x, ui_elements)
            line.set_ydata(y)
        """

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
    
    def updateFlag_test(self):
        print(f"Flag updated: {self.updateFlag.get()}")
        self.updateFlag.set(0)
        print(f"Flag reset: {self.updateFlag.get()}")

    def on_frame_configure(self, event):
        self.paramcanvas.configure(scrollregion=self.paramcanvas.bbox("all"))

    def on_closing(self):
        # Properly close the Matplotlib figure
        plt.close(self.fig)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()