import raytracing.matrixcalc as rey
import matplotlib.pyplot as plt

testrey = rey.BeamTrace(rey.buildMatrixList(test = True), rey.calcq(Z = 0, lam = 972E-9, W = 2E-3, n = 1),n_points = 10000)
testrey.constructRey()

print("asd")
plt.plot(testrey.xs,testrey.ws)
plt.show()