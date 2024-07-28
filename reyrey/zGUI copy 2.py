import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

# Import the GUI component prototypes and init functions
from GUI_components import GUI_PROTOTYPES, init_element

def generate_plot_dataA(x, amplitude, frequency, phase):
    return amplitude * np.sin(frequency * x)

def generate_plot_dataB(x, amplitude, frequency, phase):
    return amplitude * np.cos(frequency * x + phase)



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
        self.add_button = ttk.Button(button_frame, text="Add Parameter", command=self.add_parameter)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.update_button = ttk.Button(button_frame, text="Update", command=self.update_plot)
        self.update_button.pack(side=tk.LEFT, padx=5)

        # Scrollable canvas for parameters
        self.paramcanvas = tk.Canvas(self.sidebar, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self.sidebar, orient="vertical", command=self.paramcanvas.yview)
        self.parameters_frame = ttk.Frame(self.paramcanvas)
        self.parameters_frame.bind("<Configure>", self.on_frame_configure)
        self.paramcanvas.create_window((0, 0), window=self.parameters_frame, anchor="nw")
        self.paramcanvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.paramcanvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


        # Frame to hold parameter entries
        #self.parameters_frame = ttk.Frame(self.paramcanvas)
        #self.parameters_frame.pack(pady=10)

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

    def add_parameter(self):
        """
        Add a new parameter to GUI with default ui_elements
        """
        param_frame = ttk.LabelFrame(self.parameters_frame, text="Parameter Set", relief=tk.RIDGE)
        param_frame.pack(pady=5, fill=tk.X)

        # Initialize for default element, for now genplotA
        ui_elements = {"shared": {
                                "function": {"val": tk.StringVar(),
                                            "elem": None,#ttk.Combobox(param_frame, textvariable=tk.StringVar(value = "generate_plot_dataA")), 
                                            "location": (0, 0),
                                            "values": ('generate_plot_dataA', 'generate_plot_dataB')
                                            },
                                "name":     {"val": tk.StringVar(value = "New Parameter"),
                                            "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = "New Parameter")),
                                            "location": (0, 1),
                                            },
                                "remove":   {"elem": ttk.Button(param_frame, text="Remove", command=lambda: self.remove_parameter(param_frame)),
                                            "location": (0, 2),
                                            },
                                },
                        "private": {
                                "amplitude": {"val": tk.DoubleVar(value = 1.0),
                                            "elem": None, #ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                                            "location": (1, 1),
                                            "label": ttk.Label(param_frame, text="Amplitude:").grid(row=1, column=0, padx=5, pady=5)
                                            },
                                "frequency": {"val": tk.DoubleVar(value = 1.0),
                                            "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 1.0)),
                                            "location": (2, 1),
                                            "label": ttk.Label(param_frame, text="Frequency:").grid(row=2, column=0, padx=5, pady=5)
                                            },
                                "phase":     {"val": tk.DoubleVar(value = 1.0),
                                            "elem": None,#ttk.Entry(param_frame, textvariable=tk.StringVar(value = 0.0)),
                                            "location": (3, 1),
                                            "label": ttk.Label(param_frame, text="Phase:").grid(row=3, column=0, padx=5, pady=5)
                                            },
                                }
                        }

        # Add the function dropdown and remove button in the first row
        ui_elements["shared"]["function"]["elem"] = ttk.Combobox(param_frame, textvariable=ui_elements["shared"]["function"]["val"])
        ui_elements["shared"]["function"]["elem"]['values'] = ('generate_plot_dataA', 'generate_plot_dataB')
        ui_elements["shared"]["function"]["elem"].current(0)  # Set default value
        ui_elements["shared"]["function"]["elem"].grid(row = ui_elements["shared"]["function"]["location"][0], 
                                                    column = ui_elements["shared"]["function"]["location"][1], 
                                                    padx = 5, pady = 5)
        ui_elements["shared"]["function"]["elem"].bind("<<ComboboxSelected>>", lambda e: self.update_parameters(param_frame, ui_elements))

        ui_elements["shared"]["name"]["elem"] = ttk.Entry(param_frame, textvariable=ui_elements["shared"]["name"]["val"])
        ui_elements["shared"]["name"]["val"].set("New Parameter")
        ui_elements["shared"]["name"]["elem"].grid(row = ui_elements["shared"]["name"]["location"][0], 
                                                    column = ui_elements["shared"]["name"]["location"][1], 
                                                    padx = 5, pady = 5)
        
        ui_elements["shared"]["remove"]["elem"].grid(row = ui_elements["shared"]["remove"]["location"][0], 
                                                    column = ui_elements["shared"]["remove"]["location"][1], 
                                                    padx = 5, pady = 5)

        # Add amplitude in the second row
        ui_elements["private"]["amplitude"]["elem"] = ttk.Entry(param_frame, textvariable=ui_elements["private"]["amplitude"]["val"])
        ui_elements["private"]["amplitude"]["elem"].grid(row = ui_elements["private"]["amplitude"]["location"][0], 
                                                    column = ui_elements["private"]["amplitude"]["location"][1], 
                                                    padx = 5, pady = 5)

        # Add frequency in the third row
        ui_elements["private"]["frequency"]["elem"] = ttk.Entry(param_frame, textvariable=ui_elements["private"]["frequency"]["val"])
        ui_elements["private"]["frequency"]["elem"].grid(row = ui_elements["private"]["frequency"]["location"][0], 
                                                    column = ui_elements["private"]["frequency"]["location"][1], 
                                                    padx = 5, pady = 5)

        # Add phase in the fourth row (initially hidden for generate_plot_dataA)
        ui_elements["private"]["phase"]["elem"] = ttk.Entry(param_frame, textvariable=ui_elements["private"]["phase"]["val"])
        ui_elements["private"]["phase"]["elem"].grid(row = ui_elements["private"]["phase"]["location"][0], 
                                                    column = ui_elements["private"]["phase"]["location"][1], 
                                                    padx = 5, pady = 5)

        self.parameters.append((param_frame, ui_elements))

        # Add a new line to the plot
        plot_function = self.get_selected_function(ui_elements["shared"]["function"]["val"].get())
        y = plot_function(self.x, \
                          ui_elements["private"]["amplitude"]["val"].get(), \
                          ui_elements["private"]["frequency"]["val"].get(), \
                          ui_elements["private"]["phase"]["val"].get())
        line, = self.ax.plot(self.x, y)
        self.lines.append(line)

        self.update_plot()

    def update_parameters(self, param_frame, ui_elements):
        function_var = ui_elements["shared"]["function"]["val"]
        if function_var.get() == 'generate_plot_dataB':
            phase_label = ui_elements["private"]["phase"]["label"]
            phase_entry = ui_elements["private"]["phase"]["elem"]
            phase_label.grid(row=3, column=0, padx=5, pady=5)
            phase_entry.grid(row=3, column=1, padx=5, pady=5)
        elif function_var.get() == 'generate_plot_dataA':
            phase_label = ui_elements["private"]["phase"]["label"]
            phase_entry = ui_elements["private"]["phase"]["elem"]
            phase_label.grid_forget()
            phase_entry.grid_forget()
        elif function_var.get() == 'Optical Line':
            pass
        else:
            phase_label.grid_forget()
            phase_entry.grid_forget()

    def remove_parameter(self, param_frame):
        for i, (frame, amplitude, frequency, phase, function_var) in enumerate(self.parameters):
            if frame == param_frame:
                # Remove the corresponding line from the plot
                line = self.lines.pop(i)
                line.remove()
                self.parameters.pop(i)
                frame.destroy()
                break

        self.update_plot()

    def update_plot(self):
        num_samples = self.sample_var.get()
        self.x = np.linspace(0, 2 * np.pi, num_samples)
        for line, (param_frame, ui_elements) in zip(self.lines, self.parameters):
            function_var = ui_elements["shared"]["function"]["val"]
            amplitude = ui_elements["private"]["amplitude"]["val"]
            frequency = ui_elements["private"]["frequency"]["val"]
            phase = ui_elements["private"]["phase"]["val"]
            plot_function = self.get_selected_function(function_var.get())
            if function_var.get() == 'generate_plot_dataA':
                y = plot_function(self.x, amplitude.get(), frequency.get(), 0)
            else:
                y = plot_function(self.x, amplitude.get(), frequency.get(), phase.get())
            line.set_ydata(y)

        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def get_selected_function(self, function_name):
        if function_name == 'generate_plot_dataA':
            return generate_plot_dataA
        else:
            return generate_plot_dataB

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