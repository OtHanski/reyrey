import numpy as np
from math import pi
import raytracing.matrices as ma

def parseOSYS():
    return 1

def buildMatrixList(test = False):
    """Build list of matrices from input list"""
    MatrixList = []
    
    if test:
        for M in ma.testSystem:
            MatrixList.append(M["ABCD"])
        return MatrixList

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

class BeamTrace:
    def __init__(self,matrexes,q_in,z0=0,n_points=1000):
        self.n_points = n_points
        self.z0 = z0 #distance from q_in point to 0, needed only for convinience
        self.matrexes = matrexes # array of matrixes or labels - strings (names) at wich to calculate q-parameter
        self.xs = [] # x coordinates
        self.ws = [] # beam waists vs. xs
        self.qz_to_print = [] # future array of (label,q) for labels in matrexes
        self.q_in = q_in # initial q-parameter of the beam
        
    def constructRey(self):
        """Function that construct waists vs x posision"""
        self.xs = []
        self.ws = []
        self.qs_to_print = []
        q_in = self.q_in
        print(f"q_in: {q_in}")
        direction = 1 # direction of the beam (if mirror comes it changes the direction)
        for M in self.matrexes:
            
            if type(M) == str: # it is a label to save current beam parameter
                    self.qs_to_print.append((M,get_w(q_in,lda),q_in))
                    print(self.qs_to_print[-1])
                    continue
                    
            if M[0][1] != 0: # it is free space matrix 
                xs = np.linspace(0,M[0][1],self.n_points)
                ws = w_z(xs+real(q_in),lda=lda,zr=imag(q_in)) # calculates waists
                #print(ws)
                
                if self.xs != []: # point where if stoped in previous matrix
                    extr = self.xs[-1]
                else :
                    extr = self.z0
                    
                self.xs.extend(direction*xs+extr)
                self.ws.extend(ws)
                
            elif M[0][1] == 0 and M[1][0] == 0: # ones matrix means a mirror - change of the direction
                direction *= -1
                continue
            q_in = transformq(M,q_in) #calculate new q-parameter for the next matrix


