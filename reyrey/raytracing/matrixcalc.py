import numpy as np
from math import *
from scipy.optimize import root
import raytracing.matrices as ma

def parseOSYS():
    return 1



def buildMatrixList(systemDicts):
    """Build list of matrices from input list"""
    MatrixList = []
    
    for M in systemDicts:
        MatrixList.append(M["ABCD"])
    return MatrixList
    
    
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

def calcq(Z = 0, ZR = 0, lam = 0, W = 0, n = 1):
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


### REPLACE EVERYTHING UNDER ###

def cavityq(ABCD):
    """Returns the waist value of cavity fundamental"""
    W = root(lambda x: abs(transformq(ABCD,1j*x)-1j*x),35e-6)
    
    return W.x[0]

def z_r(w0,lda):
    """Calculates rayleigh range [m], w0 - waist [m], lda - wavelength [m]"""
    return (pi*w0**2/lda)

def w_z(z,lda,zr=None,w0=None,z0=0):
    """calculates beam radius [m] based on z_r - rayleigh range [m] or waist radios w0 [m],lda - wavelength [m]"""
    if zr == None:
        zr = z_r(w0,lda)
    try:
        return (lda / pi * zr)**(1/2)*(1 + (z-z0)**2/zr**2)**(1/2)
    except:
        print(f"lda:{lda}\nzr: {zr}\nz: {z}")
        print(zr)
        print(lda)
        
        return 0

class BeamTrace:
    def __init__(self,matrexes,q_in,z0=0, n_points=1000):
        self.n_points = n_points
        self.z0 = z0 #distance from q_in point to 0, needed only for convinience
        self.matrexes = matrexes # array of matrixes or labels - strings (names) at wich to calculate q-parameter
        self.xs = [] # x coordinates
        self.ws = [] # beam waists vs. xs
        self.qz_to_print = [] # future array of (label,q) for labels in matrexes
        self.q_in = q_in # initial q-parameter of the beam
        
    def constructRey(self,lda = 972E-9):
        """Function that construct waists vs x posision"""
        self.xs = []
        self.ws = []
        self.qs_to_print = []
        q_in = self.q_in
        print(f"q_in: {q_in}")
        direction = 1 # direction of the beam (if mirror comes it changes the direction)
        self.matrexes.reverse()
        for M in self.matrexes:
            
            if type(M) == str: # it is a label to save current beam parameter
                    self.qs_to_print.append((M,w_z(q_in,lda),q_in))
                    print(self.qs_to_print[-1])
                    continue
                    
            if M[0][1] != 0: # it is free space matrix 
                xs = np.linspace(0,M[0][1],self.n_points)
                ws = w_z(xs+np.real(q_in),lda=lda,zr=np.imag(q_in)) # calculates waists
                #print(ws)
                
                if self.xs != []: # point where if stoped in previous matrix
                    extr = self.xs[-1]
                else :
                    extr = self.z0
                    
                self.xs.extend(direction*xs+extr)
                #print(f"wsl: {self.ws}")
                #print(f"ws: {ws}")
                self.ws.extend(ws)
                
            elif M[0][1] == 0 and M[1][0] == 0: # ones matrix means a mirror - change of the direction
                direction *= 1
                continue
            q_in = transformq(M,q_in) #calculate new q-parameter for the next matrix


