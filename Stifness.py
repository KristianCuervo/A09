import scipy as sp
from scipy import interpolate, integrate
import numpy as np



# import moment diagrams (maybe change format depending on input)

M1 = [0,2,4,6,8,10]     # y location
M2 = [10,9,8,7,6,5]     # value

M = sp.interpolate.interp1d(M1,M2,kind="linear",fill_value="extrapolate")     # makes a function of M1 and M2 (if step-wise "previous" else "linear")


# import moment of inertia

I1 = [0,5,10]     # y location
I2 = [1,1,1]     # value

I = sp.interpolate.interp1d(I1,I2,kind="previous",fill_value="extrapolate")     # makes a function of I1 and I2


# constants

b = 10
v_max = 0.15*b



def f(y):       # right-hand side of formula
    E = 10
    return M(y) / (I(y)*E)

def dvdy(y):    # left-hand side of formula
    a,b = sp.integrate.quad(f, 0, y)
    return -1*a

def v(y):       # integral of dvdy
    v_spef,err = sp.integrate.quad(dvdy, 0, y)
    return v_spef

v_list = []     # deflection as function of y (steps of 1)
for i in range(0,b+1,1):
    v_list.append(v(i))

print(v_list)






# import torsion diagrams


T1 = [0,2,4,6,8,10]     # y location
T2 = [10,9,8,6,4,0]     # value

T = sp.interpolate.interp1d(M1,M2,kind="linear",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")

# import torsional moment of inertia


J1 = [0,2,4,6,8,10]     # y location
J2 = [10,9,8,6,4,0]     # value

J = sp.interpolate.interp1d(M1,M2,kind="previous",fill_value="extrapolate")     # make a function of M1 and M2 (if step-wise "previous" else "linear")
