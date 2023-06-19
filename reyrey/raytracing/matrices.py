from numpy import inf,array


def free(l = 0):
    """Free space matrix, l - optical path [meters] = d*n, n-reflactive index, d-real distance"""
    return array([[1,l],
                  [0,1]])

def thinlens(f = inf):
    """Thin lens matrix, f - rear focal distance [meters]"""
    return array([[1,0],
                  [-1/f,1]])
                  

def thicklens():
    """Not implemented yet"""
    return array([[1,0],
                  [0,1]])

def flatrefraction(n1 = 1, n2 = 1):
    """Refraction at flat surface, n1 and n2 refractive indices of initial and final medium"""
    return array([[1,0],
                  [0,n1/n2]])


testSystem = [
{"ABCD": free(l = 20E-3), "label": None},
{"ABCD": thinlens(f = 40E-3), "label": "f1 = 40 mm"},
{"ABCD": free(l = 90E-3), "label": None},
{"ABCD": thinlens(f = 40E-3), "label": "f2 = 40 mm"},
{"ABCD": free(l = 60E-3), "label": None},
{"ABCD": thinlens(f = 250E-3), "label": "f3 = 250 mm"},
{"ABCD": free(l = 300E-3), "label": None}
]