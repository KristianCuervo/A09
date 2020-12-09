
import numpy as np
import wingbox_properties as wb
from wingbox_properties import wb_rear_spar_h,wb_front_spar_h, wb_area
import scipy as sp 
from scipy import interpolate
import matplotlib.pyplot as plt
from Torsion_shear import torsion_shear_spar

#K_s calculations using two list and the graph :) -> clamped
A = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4, 4.25, 4.5, 4.75, 5]
Ks = [15, 12.6, 11.5, 11, 10.5, 10, 9.75, 9.75, 9.75, 9.6, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5, 9.5] 

f_Ks = sp.interpolate.interp1d(A,Ks,kind='cubic', fill_value='extrapolate')
E = 68.9 * 10**9
rib_locations = [2, 5, 7,9,13 ] #this can be changed
a = []
halfspan = 27.83/2
b = []
for i in range(len(rib_locations)):#calculates a
    if i == 0:
        a.append(rib_locations[i])
        b.append(wb_front_spar_h(rib_locations[i]/2))
    elif i == (len(rib_locations)-1):
        a.append(halfspan-rib_locations[i])
        b.append(wb_front_spar_h(((halfspan-rib_locations[i])/2)+rib_locations[i]))
        
        
    else:
        a.append(rib_locations[i]-rib_locations[i-1])
        b.append(wb_front_spar_h(((rib_locations[i]-rib_locations[i-1])/2)+rib_locations[i-1]))

rib_locations.append(halfspan)
    
kv = 1.5
    
b_array = np.array(b)
a_array = np.array(a)
a_over_b = a_array/b_array
Ks = f_Ks(a_over_b)
print(Ks)
def Ks(y):
    return 9.5
    # count = 0
    # for i in rib_locations:
        
    #     if y <= i:
    #         return Ks[count]
    #     else:
    #         count +=1

# def b(y):
#     count = 0
#     for i in rib_locations:
        
#         if y <= i:
#             return b_array[count]
#         else:
#             count +=1






    




t_spar = 6* 10**-3      #mm
nu = 0.33




def Torsion_shear_spar_polynomial(y):
    value =  1.89578061e+02*y**5  + -5.44667916e+03 *y**4 +  5.16697098e+04*y**3 + -1.44533126e+05*y**2 + 2.76659218e+05*y + -1.25572498e+07
    return value

def Shear_force_shear(y):
    val = 1.76137017e+08 *y**5 + -1.38718840e+09 *y**4 + 5.85022295e+09 *y**3 + 3.26810067e+11 * y**2 + -1.62640685e+12 *y + -9.29847302e+13
    return val

def total_shear(y):
    var = Torsion_shear_spar_polynomial(y)+Shear_force_shear(y)
    return var


def theta_critical(y):                          #Theta is actually tau 
    theta_critical = (np.pi**2 * Ks(y) * E * (t_spar/wb_front_spar_h(y))**2 )/ (12 *(1- nu**2))
    return theta_critical


def shear_force(y):#for n = 4.3 
    val = -1.56221917 * 10**(-1) * y**5 + 6.39818237 * 10**0 * y**4 + -1.25068922 * 10**2 * y**3 + 7.91787252 * 10**2 * y**2 + 1.98315252 * 10**4 * y + -2.49637912 * 10**5
    return val



#Initial values

t_f = t_spar #this can be changed
t_r = t_spar #this can be changed


    
def shear_stress_average(y):
    h_f = wb_front_spar_h(y)
    h_r = wb_rear_spar_h(y)
    tau_ave = shear_force(y)/(h_f*t_f + h_r*t_r)
    return tau_ave

def tau_max_shear(y):
    tau_max_shear = shear_stress_average(y)*kv
    return tau_max_shear #To import from shear program at root...


span = []
tau_max_shea = []
theta_critica = []
total_shea = []
# for i in np.arange(0, 27.83/2, 0.1):
#     span.append(i)
#     tau_max_shea.append(np.abs(tau_max_shear(i)))
#     theta_critica.append(theta_critical(i))
#     total_shea.append(np.abs(total_shear(i)))

# plt.plot(span, theta_critica,'r')
# plt.plot(span,tau_max_shea,'b')
# plt.show()
# plt.plot(span, theta_critica,'r')
# plt.plot(span, total_shea,'b')
# plt.show()



#The critical Shear stress due to torsion at max so in the spar 
def torsion_shear_new(y):
    torsion_shear  = np.abs(torsion_shear_spar(y)) + np.abs(tau_max_shear(y))
    return torsion_shear


def safety_margin(y):
    safety = theta_critical(y)/torsion_shear_new(y)
    return safety
#Empty lists
span = []
torsion_shear = []
theta_critica = []
safety = []
#Plot
for i in np.arange(0, 27.83/2, 0.1):
    span.append(i)
    torsion_shear.append(np.abs(torsion_shear_new(i)))
    theta_critica.append(theta_critical(i))
    safety.append(safety_margin(i))
# torsion_shear_array = np.array(torsion_shear)
# theta_critica_array = np.array(theta_critica)
# safety = theta_critica_array/torsion_shear_array

plt.plot(span, theta_critica, 'r')
plt.plot(span,torsion_shear,'b')
plt.show()
print(safety_margin)
plt.plot(span, safety)
plt.show()


#


