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

print(horABCD)

whor = rey.cavityq(horABCD)
wver = rey.cavityq(verABCD)
print(whor)

telerey = rey.BeamTrace(teleM, rey.calcq(Z = 0, lam = 972E-9, W = 2E-3, n = 1),n_points = 10000)
telerey.constructRey()
cavhorey = rey.BeamTrace(cavityhorM, q_in = 1j*whor ,n_points = 20000)
cavhorey.constructRey()
cavverey = rey.BeamTrace(cavityverM, q_in = 1j*wver ,n_points = 20000)
cavverey.constructRey()

minw = 2E-3
mind = 0
for i in range(len(telerey.xs)):
    if telerey.xs[i] >= mat.d4:
        if telerey.ws[i] <= minw:
            minw = telerey.ws[i]
            mind = i
print(len(cavhorey.ws)/2)
print(f"minw: {minw:.4} at x: {telerey.xs[mind]-mat.d4:.4}\nhorfoc: {cavhorey.ws[0]*1E6:.6}, hormatch: {cavhorey.ws[int(len(cavhorey.ws)/2)]*1E6:.6}\nverfoc: {cavverey.ws[0]*1E6:.4}, vermatch: {cavverey.ws[int(len(cavverey.ws)/2)]*1E6:.4}\ndiff: {(cavhorey.ws[int(len(cavhorey.ws)/2)]-cavverey.ws[int(len(cavverey.ws)/2)])*1E6:.4}")

xoffset = telerey.xs[mind]
plt.plot(telerey.xs,telerey.ws, label = "Coupling beam")
plt.plot(cavverey.xs+xoffset-cavverey.xs[-1]/2,cavverey.ws, label = "cavver")
plt.plot(cavhorey.xs+xoffset-cavhorey.xs[-1]/2,cavhorey.ws, label = "cavhor")
plt.legend()
plt.show()