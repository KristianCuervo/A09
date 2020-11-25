import scipy as sp
from scipy import interpolate, integrate
import numpy as np
import matplotlib.pyplot as plt
from NormalShearMomentDiagrams import Momentforce
from wingbox_properties import I_xx, I_xx_str


# # # # # # # DEFLECTION # # # # # # # # 



# import moment diagrams (maybe change format depending on input)

M1 = [0,2,4,6,8,10]     # y location
M2 = [10,9,8,7,6,5]     # value

M = sp.interpolate.interp1d(M1,M2,kind="linear",fill_value="extrapolate")     # makes a function of M1 and M2 (if step-wise "previous" else "linear")


# import moment of inertia

I1 = [0,5,10]     # y location
I2 = [1,1,1]     # value
def I(c):
    return I_xx(c) + I_xx_str(c) # makes a function of I1 and I2


# constants

b = 29.8
v_max = 0.15*b



def f(y):       # right-hand side of formula
    E = 10
    return Momentforce(y) / (I(y)*E)

def dvdy(y):    # left-hand side of formula
    a,b = sp.integrate.quad(f, 0, y)
    return -1*a

def v(y):       # integral of dvdy
    v_spef,err = sp.integrate.quad(dvdy, 0, y)
    return v_spef

v_list = np.arange(0, b, 0.1)    # deflection as function of y (steps of 1)
v_values = []

for i in v_list:
    v_values.append(v(i))

print("total deflection equals: ", v_values[-1])

#######SAME BUT WITH FUEL


def f1(y):       # right-hand side of formula
    E = 10
    return Momentforce1(y) / (I(y)*E)

def dvdy1(y):    # left-hand side of formula
    a,b = sp.integrate.quad(f1, 0, y)
    return -1*a

def v1(y):       # integral of dvdy
    v_spef,err = sp.integrate.quad(dvdy1, 0, y)
    return v_spef

v1_list = np.arange(0, b, 0.1)    # deflection as function of y (steps of 1)
v1_values = []

for i in v1_list:
    v1_values.append(v1(i))

print("total deflection equals: ", v1_values[-1]) 
### MOST CRITICAL CASE

print("most critical case deflection is:", max(v_values[-1], v1_values[-1]))







# # # # # # # TORSION # # # # # # # # 



# import torsion diagrams


T1 = [0,2,4,6,8,10]     # y location
T2 = [5,5,5,5,5,5]     # value

T = sp.interpolate.interp1d(T1,T2,kind="linear",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")


# import torsional moment of inertia


J1 = [0,2,4,6,8,10]     # y location
J2 = [1,1,1,1,1,1]     # value

J = sp.interpolate.interp1d(J1,J2,kind="previous",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")


def g(y):       # right-hand side of formula
    G = 10
    return T(y) / (G * J(y))

def theta(y):   # left-hand side of formula
    bla,err2 = sp.integrate.quad(g, 0, y)
    return bla


theta_list = np.arange(0, b, 0.1)       # range of numbers
theta_values = []                       # empty list for twist values
for i in theta_list:                    # calculate twist values
    theta_values.append(theta(i))

print("total twist equals: ", theta_values[-1])


plt.plot(v_list, v_values)              # plot graphs (comment one out if you want one alone)
plt.plot(theta_list, theta_values)
plt.show()
