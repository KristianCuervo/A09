import scipy as sp
from scipy import interpolate, integrate
import numpy as np
import matplotlib.pyplot as plt
import math
from multiprocessing import Process
from wingbox_properties import I_xx, I_xx_str, J
from NormalShearMomentDiagrams import Momentforce, TorqueFunc

# # # # # # # # DEFLECTION # # # # # # # # 



# import moment diagrams (maybe change format depending on input)

M1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]     # y location
M2 = []
for i in M1:
    M2.append(Momentforce(i))

M = sp.interpolate.interp1d(M1,M2,kind="linear",fill_value="extrapolate")     # makes a function of M1 and M2 (if step-wise "previous" else "linear")


# import moment of inertia

I1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]     # y location
I2 = []
for i in I1:
    I2.append(I_xx(i, 0.008, 0.005) + I_xx_str(i, 0.0005))

I = sp.interpolate.interp1d(I1,I2,kind="linear",fill_value="extrapolate")     # makes a function of I1 and I2


# constants

b = 13
v_max = -0.15*b



def f(y):       # right-hand side of formula
    E = 68900000000
    return M(y) / (I(y)*E)

def dvdy(y):    # left-hand side of formula
    a,b = sp.integrate.quad(f, 0, y)
    return a

def v(y):       # integral of dvdy
    v_spef,err = sp.integrate.quad(dvdy, 0, y)
    return v_spef

# v_list = np.arange(0, b, 0.1)    # deflection as function of y (steps of 1)
# v_values = []

# # for i in v_list:
# #     v_values.append(v(i))
# #     print(i)
# #     print(v(i))

stress = M(0.1)*0.581/I(0.1)

print("total deflection equals: ", v(b))
print("maximum allowable deflection equals: ", v_max/1.5)
print()
print("stress at root equals = ", stress)



# # # # # # # TORSION # # # # # # # # 



# import torsion diagrams


T1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]     # y location
T2 = []
for i in T1:
    T2.append(TorqueFunc(i))

print(T2)
T = sp.interpolate.interp1d(T1,T2,kind="linear",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")


# import torsional moment of inertia


J1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]     # y location
J2 = []
for i in J1:
    J2.append(J(i, 0.001, 0.001))


J = sp.interpolate.interp1d(J1,J2,kind="linear",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")


def g(y):       # right-hand side of formula
    G = 26000000000
    return T(y) / (G * J(y))

def theta(y):   # left-hand side of formula
    bla,err2 = sp.integrate.quad(g, 0, y)
    return bla




print("total twist equals: ", ((theta(b)))/(2*math.pi)*360, " deg")
print("maximum allowable twist equals: -10 deg")

# plt.plot(v_list, v_values)              # plot graphs (comment one out if you want one alone)
# plt.plot(theta_list, theta_values)
# plt.show()
