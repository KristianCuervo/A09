import numpy as np
import scipy as sp


# relevant dimensions 

ts = 0.008 #m spar thickness
tk = 0.005 #m web thickness

# import inertia stuff and geomtry

from wingbox_properties import *

# import momentforce from NormalShearMomentDiagram

from DiagramsWP4 import Moment_positive_n, Moment_negative_n    # change Moment_positive_n to negative when calculating for n = -2.259

# calculate sigma functions for tension and compression
def dz(y): #offset of vertical position of te spar
    c = (dz_0-dz_1) / wingspan/2
    dz = c*y+dz_0
    return dz

def sigma_ten(y):
    if y < 0:
        return 0
    if y > wingspan/2:
        return 0
    z  = wb_centroid(y)[1]
    sigma = Moment_positive_n(y)*z / (I_xx(y, ts, tk) + I_xx_str(y, A_str))

    return sigma


def sigma_comp(y):
    if y < 0:
        return 0
    if y > wingspan/2:
        return 0
    z = wb_centroid(y)[1] - (wb_rear_spar_h(y) + dz(y))
    sigma = Moment_positive_n(y)*z / (I_xx(y, ts, tk) + I_xx_str(y, A_str))
    return sigma

# for loop to make it into an array
span = np.arange(0, wingspan/2, 0.1)

sigma_ten_array = np.array([])
for i in span:
    sigma_ten_array = np.append(sigma_ten_array, sigma_ten(i))

sigma_com_array = np.array([])
for i in span:
    sigma_com_array = np.append(sigma_com_array, sigma_comp(i))

# make graph


# make polynomial formula

# buckling formulae


def col_buck(I_str, A):
    critical_stress= K*3.141592*E*(I_str) / (A * (wingspan/2)^2)
    return critical_stress


#stringers 

t = 0.002 #m thickness

# centroid, inertia, area of J section stringer

J = [1,2,3,4]

def centroid_y_J(J):
    y = (J[1]**2/2 + J[1]*J[2] + J[1]*J[3] - J[3]**2) / (sum(J))
    return y

def I_J(J):
    I_a = J[0]*(centroid_y_J(J))**2
    I_b = 1/12 * J[1]**3 *t + (J[1]/2 - centroid_y_J(J))**2*J[1]*t
    I_c = (J[1] - centroid_y_J(J))**2*J[2]*t
    I_d = 1/12 * J[3]**3 *t + (J[1] - J[3]/2 - centroid_y_J(J))**2*J[3]*t
    return I_a + I_b + I_c +I_d

def A_J(J):
    return t*(sum(J))

# centroid, inertia, area of L section stringer

T = [1,2]

def centroid_y_L(L):
    y =  L[1]**2 / 2 / (sum(L))
    return y

def I_L(L):
    I_a = L[0]*(centroid_y_L(L))**2
    I_b = 1/12 * L[1] **3 + (L[1]/2 - centroid_y_L(L))**2*L[1]*t
    return I_a + I_b 

def A_L(L):
    return t*sum(L)
