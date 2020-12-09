from txtreader import filereader
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import *




#function to convert torsion to shear stress
#t_shear = Torsion/(2*t*Am)
#input: polynomial function dependent on y called torsion_polynomial
#positive torsion: ccw shear flow
#### constants ############################################################################


##Inital values
# span = filereader('MainWing_a0.00_v10.00ms.txt')[0]
# chord = filereader('MainWing_a0.00_v10.00ms.txt')[1]
# f_chord = sp.interpolate.interp1d(span, chord, kind='linear', fill_value='extrapolate')

root_le_h = 581.88/1000 #Height of leading edge of wingbox at root
root_te_h = 553.5/1000 #Height of trailing edge of wingbox at root
root_l = 1784/1000 #Length of wingbox at root
    
tip_le_h = 157.31/1000 #Height of leading edge of wingbox at tip
tip_te_h = 148.66/1000 #Height of trailing edge of wingbox at tip
tip_l = 484/1000 #Length of wingbox at tip
    
root_area = 0.5 * (root_le_h+root_te_h) * root_l #area of wingbox at root
tip_area = 0.5 * (tip_le_h+tip_te_h) * tip_l #area of winbox at tip
wingspan =  27.83   #m



#values that can be changed
t_spar = 6*10**-3 #m
t_skin = 1*10**-3 #m



def torsion_polynomial(y):#for n=4.3 can be changed to negative too
    val = 1.90933009 * y**4 +  -6.74551747 * 10**1 * y**3 +  6.42107820 * 10**2 * y**2 + 4.33475502 * 10**3 * y +  -7.54677093 * 10**4
    return val


def wb_area(y): #Calculates enclosed are of wingbox at a span location b in mm
    #linear regression for area along wingspan
    
    m = -(root_area - tip_area)/(wingspan/2)
    c = root_area
    
    area = m*y + c
    
    return area
    
    


    
def torsion_shear_spar(y):
    torsion_y = torsion_polynomial(y)    
    torsion_shear_spar = torsion_y/(2*wb_area(y)*t_spar)
    return torsion_shear_spar

    
def torsion_shear_skin(y):
    torsion_y = torsion_polynomial(y)    
    torsion_shear_skin = torsion_y/(2*wb_area(y)*t_skin)
    return torsion_shear_skin

# span  = []
# spar_shear = []
# skin_shear = []

# for i in np.arange(0, 27.83/2, 0.1):
#     span.append(i)
#     spar_shear.append(torsion_shear_spar(i))
#     skin_shear.append(torsion_shear_skin(i))
# span_array = np.array(span)
# spar_shear_array = np.array(spar_shear)
# skin_shear_array = np.array(skin_shear)


# # pl1 = np.polyfit(span_array, spar_shear_array,5)
# # pl2 = np.polyfit(span_array, skin_shear_array,5)

# plt.plot(span_array, spar_shear_array )#,  xlabel = 'span [m]', ylabel = 'shear stress [Pa]', title = 'Spanwise shear stress of the spar')
# # plt.plot(span_array, np.polyval(pl1, span_array))
# plt.show()
# plt.plot(span_array, skin_shear_array) #, xlabel = 'span [m]', ylabel = 'shear stress [Pa]', title = 'Spanwise shear stress of the skin')
# # plt.plot(span_array, np.polyval(pl2, span_array))
# plt.show()

def spar_shear_polynomial(y):
    value =  1.89578061e+02*y**5  + -5.44667916e+03 *y**4 +  5.16697098e+04*y**3 + -1.44533126e+05*y**2 + 2.76659218e+05*y + -1.25572498e+07
    return value

def skin_shear_polynomial(y):
    val = 5.68734182e+02*y**5 + -1.63400375e+04 *y**4 + 1.55009129e+05 *y**3 +  -4.33599378e+05 *y**2 + 8.29977653e+05 *y + -3.76717493e+07
    return val
    







