from numpy import inf,array
from math import radians, cos

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

def ringCavity(l_focus = 61E-3, l_free = 72E-3, l_crystal = 15E-3, R = 50E-3, n_crystal = 1.567, theta = radians(12)):
    """Returns the dict for a ringCavity"""
    #l_focus = 60.105E-3, l_free = 108E-3, l_crystal = 30E-3, R = 50E-3, n_crystal = 1.567, theta = radians(8)
    l_diagonal=(l_focus+l_free)/(2*cos(2*theta))
    
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
    #l_focus = 60.105E-3, l_free = 108E-3, l_crystal = 30E-3, R = 50E-3, n_crystal = 1.567, theta = radians(8)
    
    cavityhor = [
        {"ABCD": free(l = l_cavity), "label": None},
        {"ABCD": curvedmirrorhor(R = R, theta = 0), "label": f"R = {R*1E3} mm"},
        {"ABCD": free(l = l_cavity), "label": None}
        ]
    
    cavityver = cavityhor
    
    return {"hor": cavityhor, "ver": cavityhor}


lenses = 2
d1 = 50E-3
d2 = 102E-3
d3 = 55E-3
df = 1500E-3

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
    {"ABCD": thinlens(f = 60E-3), "label": "f1 = 40 mm"},
    {"ABCD": free(l = d2), "label": None},
    {"ABCD": thinlens(f = 40E-3), "label": "f3 = 250 mm"},
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