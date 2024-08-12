## HOW TO RUN

1. Create and activate virtual env, and install dependencies (Windows example below), or install dependency packages from `requirements.txt` in your global env.
```
../reyrey > python -m venv myenv
../reyrey > myenv\Scripts\activate
../reyrey (myenv) > pip install -r requirements.txt
```

2. Run GUI.py
```
../reyrey (myenv) > python src\GUI.py
```

3. Exit venv when done
```
../reyrey (myenv) > deactivate
```

## User instructions

The program is a GUI interface for designing optical beamlines for reshaping of laser beams based on [Ray transfer matrix analysis](https://en.wikipedia.org/wiki/Ray_transfer_matrix_analysis). The program provides the following functionality:

- Design a beam shaping line by inserting optical components and setting the input beam parameters
- Design linear and ribbon cavities (Or add your own)
- Calculate and plot beam waist transformations based on the optical line components
- Save & Load optical line configurations for future use

In the `savestates/samples` folder there are example setups for playing around.

Note that if cavity parameters are unstable, currently the cavity calculations simply fail and produce null output (no plot). To get a stable cavity to start optimizing parameters from one can use as an initial guess `l_focus = l_free = 1.2 * R_focus` and `theta = 10 deg`.

Explanation of the UI:

TODO

## Credit

Credit to Artem Golovizin for providing the basis for the ray transfer calculations.