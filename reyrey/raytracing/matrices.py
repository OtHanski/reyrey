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

