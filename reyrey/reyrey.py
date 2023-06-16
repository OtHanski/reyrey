import raytracing.matrixcalc as rey
import matplotlib.pyplot as plt

testrey = rey.BeamTrace(rey.buildMatrixList(test = True), rey.calcq(Z = 0, ZR = 0, lam = 0, W = 0, n = 1))
testrey.constructRey()


plt.plot(testrey.xs,testrey.ws)