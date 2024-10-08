"""Implements matrices for ray calculations"""

from math import radians, cos, sin
from numpy import inf,array

def identity():
    """Identity matrix"""
    return array([[1,0],
                  [0,1]])

def free(l = 0):
    """Free space matrix, l - optical path [meters] = d*n, n-reflactive index, d-real distance"""
    return array([[1,l],
                  [0,1]])

def thinlens(f = inf):
    """Thin lens matrix, f - rear focal distance [meters]"""
    return array([[1,0],
                  [-1/f,1]])

def curvedmirrorhor(R = inf, theta = radians(8)):
    """Horizontal curved mirror matrix¨, R - Radius of curvature, theta - incoming beam angle"""
    return array([[1,0],
                  [-2/(R*cos(theta)),1]])

def curvedmirrorver(R = inf, theta = radians(8)):
    """Horizontal curved mirror matrix¨, R - Radius of curvature, theta - incoming beam angle"""
    return array([[1,0],
                  [-2*cos(theta)/(R),1]])

def thicklens():
    """Not implemented yet"""
    return array([[1,0],
                  [0,1]])

def flatrefraction(n1 = 1, n2 = 1):
    """Refraction at flat surface, n1 and n2 refractive indices of initial and final medium"""
    return array([[1,0],
                  [0,n1/n2]])

def ringCavity(l_focus = 61.6E-3,
               l_free = 69.3E-3,
               l_crystal = 15E-3,
               R = 50E-3,
               n_crystal = 1.567,
               theta = radians(18.2)):
    """Returns the dict for a ringCavity"""
    l_diagonal=(l_focus+l_free)/(2*cos(2*theta))
    print(f"Cavity height: {sin(theta)*l_diagonal}")

    cavityhor = [
        {"ABCD": free(l = l_crystal/(2*n_crystal)), "label": None},
        {"ABCD": free(l = (l_focus-l_crystal)/2), "label": None},
        {"ABCD": curvedmirrorhor(R = R, theta = theta), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = (2*l_diagonal+l_free)/2), "label": None},
        {"ABCD": free(l = (2*l_diagonal+l_free)/2), "label": None},
        {"ABCD": curvedmirrorhor(R = R, theta = theta), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = (l_focus-l_crystal)/2), "label": None},
        {"ABCD": free(l = l_crystal/(2*n_crystal)), "label": None}
        ]

    cavityver = [
        {"ABCD": free(l = l_crystal/(2*n_crystal)), "label": None},
        {"ABCD": free(l = (l_focus-l_crystal)/2), "label": None},
        {"ABCD": curvedmirrorver(R = R, theta = theta), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = (2*l_diagonal+l_free)/2), "label": None},
        {"ABCD": free(l = (2*l_diagonal+l_free)/2), "label": None},
        {"ABCD": curvedmirrorver(R = R, theta = theta), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = (l_focus-l_crystal)/2), "label": None},
        {"ABCD": free(l = l_crystal/(2*n_crystal)), "label": None}
        ]

    return {"hor": cavityhor, "ver": cavityver}

def linCavity(l_cavity = 75E-3, R = 50E-3):
    """Returns the dict for a linCavity (curved plus flat mirror)"""
    cavityhor = [
        {"ABCD": free(l = l_cavity), "label": None},
        {"ABCD": curvedmirrorhor(R = R, theta = 0), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = l_cavity), "label": None}
        ]

    cavityver = cavityhor

    return {"hor": cavityhor, "ver": cavityver}


lenses = 2
d1 = 50E-3
d2 = 201.8E-3
d3 = 55E-3
df = 2000E-3

# Working two lens: 40mm + 40 mm, distance 81.225mm

if lenses == 1:
    testTelescope = [
    {"ABCD": free(l = d1), "label": None},
    {"ABCD": thinlens(f = 500E-3), "label": "f3 = 250 mm"},
    {"ABCD": free(l = df), "label": None}
    ]
    d4 = d1
if lenses == 2:
    testTelescope = [
    {"ABCD": free(l = d1), "label": None},
    {"ABCD": thinlens(f = 150E-3), "label": "f1 = 40 mm"},
    {"ABCD": free(l = d2), "label": None},
    {"ABCD": thinlens(f = 50E-3), "label": "f3 = 250 mm"},
    {"ABCD": free(l = df), "label": None}
    ]
    d4 = d1+d2
if lenses == 3:
    testTelescope = [
    {"ABCD": free(l = d1), "label": None},
    {"ABCD": thinlens(f = 100E-3), "label": "f1 = 40 mm"},
    {"ABCD": free(l = d2), "label": None},
    {"ABCD": thinlens(f = 40E-3), "label": "f2 = 40 mm"},
    {"ABCD": free(l = d3), "label": None},
    {"ABCD": thinlens(f = 40E-3), "label": "f3 = 250 mm"},
    {"ABCD": free(l = df), "label": None}
    ]
    d4 = d1+d2+d3
testCavity = None

# Remember to keep parameters in correct order for the funcs.
matrixdicts = {
    "free": {"func": free,
             "params": ["l"],
             "label": "Free space",
             "horver": False
            },
    "thinlens": {"func": thinlens,
             "params": ["f"],
             "label": "Thin lens",
             "horver": True
            },
    "curvedmirror": {"func": {"hor": curvedmirrorhor, "ver": curvedmirrorver},
             "params": ["R", "θ"],
             "label": "Curved mirror",
             "horver": True
            },
    "thicklens": {"func": thicklens,
             "params": [],
             "label": "Thick lens (not implemented)",
             "horver": True
            },
    "flatrefraction": {"func": flatrefraction,
             "params": ["n1", "n2"],
             "label": "Flat refraction",
             "horver": False
            },
    }


def GUI_matrix(params: dict):
    """Return the hor/ver matrices for the GUI element"""
    func = params["func"]
    match func:
        case "free":
            mat = {"hor": free(l = params["l"]), "ver": free(l = params["l"])}
            if not params["hor"]:
                mat["hor"] = identity()
            if not params["ver"]:
                mat["ver"] = identity()
        case "thinlens":
            mat = {"hor": thinlens(f = params["f"]), "ver": thinlens(f = params["f"])}
            if not params["hor"]:
                mat["hor"] = identity()
            if not params["ver"]:
                mat["ver"] = identity()
        case "curvedmirror":
            mat = {"hor": curvedmirrorhor(R = params["R"], theta = params["θ"]),
                   "ver": curvedmirrorver(R = params["R"], theta = params["θ"])}
            if not params["hor"]:
                mat["hor"] = identity()
            if not params["ver"]:
                mat["ver"] = identity()
        case "thicklens":
            mat = {"hor": thicklens(), "ver": thicklens()}
            if not params["hor"]:
                mat["hor"] = identity()
            if not params["ver"]:
                mat["ver"] = identity()
        case "flatrefraction":
            mat = {"hor": flatrefraction(n1 = params["n1"], n2 = params["n2"]),
                   "ver": flatrefraction(n1 = params["n1"], n2 = params["n2"])}
            if not params["hor"]:
                mat["hor"] = identity()
            if not params["ver"]:
                mat["ver"] = identity()
        case _:
            mat = {"hor": identity(), "ver": identity()}
    return mat
