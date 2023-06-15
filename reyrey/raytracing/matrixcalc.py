import numpy as np
from math import pi

def compositeABCD(matrixList = []):
    """Takes as input an ordered list of numpy matrices, 
       returns their product"""
    
    # Reverse list for correct multiplication order
    matrixList.reverse()
    result = np.array([[1,0],
                    [0,1]])
    
    for M in matrixList:
        result = np.matmul(M,result)
    
    return result

def calcq(Z, ZR = 0, lam = 0, W = 0, n = 1):
    """Calculate Q parameter, Z = Distance from waist, ZR = Rayleigh length, 
       lam = wavelength, W = Beam waist, n = Refractive index"""
    # If no parameters given, return NaN
    if ZR == lam == W == 0:
        return np.nan
    # If ZR not given, calculate it
    elif ZR == 0:
        ZR = pi*n*W**2/lam
        
    return Z+1j*ZR

def transformq(ABCD, q1):
    """Calculate changes to q parameter via ABCD matrix"""
    q2 = (ABCD[0,0]*q1+ABCD[0,1])/(ABCD[1,0]*q1+ABCD[1,1])
    return q2