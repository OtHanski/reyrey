import raytracing.matrixcalc as rey
import raytracing.matrices as mat
import matplotlib.pyplot as plt
from numpy import argmin

tele = mat.testTelescope
cav = mat.ringCavity()
cavityhorM = rey.buildMatrixList(cav["hor"])
cavityverM = rey.buildMatrixList(cav["ver"])
teleM = rey.buildMatrixList(tele)
horABCD = rey.compositeABCD(cavityhorM)
verABCD = rey.compositeABCD(cavityverM)
teleABCD = rey.compositeABCD(teleM)

whor = rey.cavityq(horABCD)
wver = rey.cavityq(verABCD)
print(whor)

telerey = rey.BeamTrace(teleM, rey.calcq(Z = 0, lam = 972E-9, W = 2E-3, n = 1),n_points = 10000)
telerey.constructRey()
cavhorey = rey.BeamTrace(cavityhorM, rey.calcq(Z = 0, lam = 972E-9, W = whor, n = 1),n_points = 10000)
cavhorey.constructRey()
cavverey = rey.BeamTrace(cavityverM, rey.calcq(Z = 0, lam = 972E-9, W = wver, n = 1),n_points = 10000)
cavverey.constructRey()

minw = 2E-3
mind = 0
for i in range(len(telerey.xs)):
    if telerey.xs[i] >= mat.d4:
        if telerey.ws[i] <= minw:
            minw = telerey.ws[i]
            mind = i

print(f"minw: {minw:.4} at x: {telerey.xs[mind]:.4}")

xoffset = telerey.xs[mind]
plt.plot(telerey.xs,telerey.ws)
plt.plot(cavverey.xs+xoffset-cavverey.xs[-1]/2,cavverey.ws)
plt.plot(cavhorey.xs+xoffset-cavhorey.xs[-1]/2,cavhorey.ws)
plt.show()