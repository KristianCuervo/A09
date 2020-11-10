from txtreader import filereader
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import interpolate, integrate

def interpolation(x_coor, array_x, array_y):
    f = sp.interpolate.interp1d(array_x, array_y, kind = 'cubic', fill_value = 'extrapolate') 
    return f(x_coor)
#### INPUTS
span = filereader("MainWing_a10.00_v10.00ms.txt")[0]
chord = filereader("MainWing_a10.00_v10.00ms.txt")[1]
CL = filereader("MainWing_a10.00_v10.00ms.txt")[3]
rho = 1.225
speed = 100 #m/s
q = 0.5*rho*speed**2

def L_accent(y):  #y is location that we're interested in, CL is array, c = chord array, q is constant = 1/2rhoV**2, span = span array
    CL_y = interpolation(y, span, CL)
    c_y = interpolation(y, span, chord)
    L_accent = CL_y*q*c_y
    return L_accent

L_accent_array = np.array([])
span_array = np.array([])

for i in np.arange(0, 13.916, .001):
    span_array = np.append(span_array, i)
    L_accent_array = np.append(L_accent_array, L_accent(i))

#plt.plot(span_array, L_accent_array)
#plt.show()
total_lift, error = sp.integrate.quad(L_accent, 0, 13.916)
print('total_lift', total_lift*2, 'N')

######### True lift
CL_true = 1.0307
S = 78.91
L_True = CL_true*q*S

print('true lift', L_True, 'N')
print('difference', (L_True-(total_lift*2))/L_True*100, 'percent')


