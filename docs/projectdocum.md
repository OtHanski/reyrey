# Feature list

## GUI
- DONE (Jan 2024, not uploaded): Create a simple GUI which can display matplotlib plots generated from the script
- DONE (Aug 2024): Build a basic framework for dynamic UI elements in Tkinter to easily generate optical components/beamlines
- DONE (Aug 2024): Update the GUI to support designing beamlines and cavities previously designed via the old script
- TODO: Check if anything can be done bout terrible performance/flickering. Works for now tho => not prio.

## Beam calc
- DONE (2022): Convert the previous Jupyter Notebook into a script
- DONE (2023, Pre-GUI): Calculate beam waists for a beam in a ribbon cavity
- DONE (2023, Pre-GUI): Configure and calculate beam waists for an open optical beam line with basic optical components
- TODO: Implement linear cavity designs
- TODO: Add more supported optical components
- TODO: Calculate actual quantitative coupling of laser power into cavity mode. Pain in the ass, will have to wait for more free time.
- TODO: Rewrite calculations in C if performance ever proves an issue.

## QoL changes
- DONE (Aug 2024): Implement savestates for the system to be able to easily resume work on a previous system config.
- DONE (Aug 2024): Implement color chooser for plots, the automatic colouring is 1. Ugly 2. Confusing. 
- TODO: Add component labels to plot
- TODO: Add ability to lock cavity to a chosen focus of OpticalLine => Automatically adjusts cavity position to optimize coupling


# Unit testing

## Design & description
As a tool meant for qualitative use in designing optical lines, there are difficulties 
in designing a quantitative and convenient automated testing suite, since most of the
functionality checks are just sanity checks on whether the resulting optical lines seem 
sensible.

Similarly, testing the GUI elements is best done by eye, since tkinter is a bit of a pain to 
automatically test.
=> Opted for manual testing in the scope of this project. 

GUI elements are defined in their own modules, and test scripts have been implemented 
within the modules => Running each module as a script functions as a unit test for the module.

Tests to run in order:
- `calctest.py` checks matrix calculations
- `GUI_PlotOptions.py` checks the plotoptions window
- `GUI_OptLineProto` checks Optical line prototype functionality (default open beamline)
- `GUI_OpticalLine.py` checks free beamline element (Currently more or less identical to proto)
- `GUI_cavities.py` checks cavity UI elements
- `GUI_LineGUI.py` checks the optical line list
- Finally run `main.py` and load in the preset sample setups to see that the whole program functions as it should.

## Test results

- `calctest.py` - Passed (14.08.2024)
- `GUI_PlotOptions.py` - 
- `GUI_OptLineProto` -
- `GUI_OpticalLine.py` -
- `GUI_cavities.py` -
- `GUI_LineGUI.py` -
- `main.py`- Passed (14.08.2024)

# Linter used: Pylint for VSCode

Pylint settings:

--disable=invalid-name

Since it's a personal project and I dislike the Python naming schemes anyway, I use my own naming scheme regardless of whether it's considered a good habit => disabled name warnings.


Remaining Linter reports:

Import errors on the submodules
- Result of Python requiring different syntax for importing submodules depending on whether the file is run as main or module => disabled errors.
"Consider iterating using dict.items()"
- Considered, decided against => disabled warnings. 
Unused variable warnings on tkinter objects
- Still good to assign the objects somewhere sensible for future ease of use => disabled warnings.
Invalid name (Not conforming to Python naming schemes)
- Since it's a personal project and I dislike the Python naming schemes anyway, I use my own naming scheme regardless of whether it's considered a good habit, ignored warnings.
