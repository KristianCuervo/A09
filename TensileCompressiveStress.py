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
