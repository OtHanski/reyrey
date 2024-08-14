# Unit testing

As a tool meant for qualitative use in designing optical lines, there are difficulties 
in designing a quantitative and convenient automated testing suite, since most of the
functionality checks are just sanity checks on whether the resulting optical lines seem 
sensible.

Similarly, testing the GUI elements is best done by eye, since tkinter is a bit of a pain to 
automatically test.
=> Opted for manual testing in the scope of this project. 

GUI elements are defined in their own modules, and test scripts have been implemented 
within the modules => Running each module as a script functions as a unit test for the module.

Tests to run:
- `calctest.py` checks matrix calculations
- `GUI_cavities.py` checks cavity UI elements
- `GUI_OptLineProto` checks Optical line prototype functionality (default open beamline)
- `GUI_OpticalLine.py` checks free beamline element (Currently more or less identical to proto)
. `GUI_PlotOptions.py` 

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
