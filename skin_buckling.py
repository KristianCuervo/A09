#COnstsnats
import numpy as np
import scipy as sp
from scipy import interpolate
from wingbox_properties import wb_front_spar_h,wb_rear_spar_h
import wingbox_properties as wb
import matplotlib.pyplot as plt
from TensileCompressiveStress import sigma_comp
t_skin = 2*10**-3           #m
E = 68.9 * 10**9
nu = 0.33



#List for the kc
a_over_b_list = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0]
k_c_list = [8, 7.5, 7.7, 7, 7.15, 7, 7, 7.15, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
rib_locations = [1,2,3,4,5.2,6.4,7.6,8.8,10.4,12]



#Finding the kc HELP!! I am soooo not happy :( Potverdorie!
f_Kc = sp.interpolate.interp1d(a_over_b_list, k_c_list, kind='cubic', fill_value='extrapolate')

a = []
b = []
halfspan = 27.83/2


for i in range(len(rib_locations)+1):#calculates a
    if i == 0:
        a.append(rib_locations[i])
        b.append(wb_front_spar_h(rib_locations[i]/2))
    elif i == (len(rib_locations)):
        a.append(halfspan-rib_locations[i-1])
        b.append(wb_front_spar_h(((halfspan-rib_locations[i-1])/2)+rib_locations[i-1]))
        
        
    else:
        a.append(rib_locations[i]-rib_locations[i-1])
        b.append(wb_front_spar_h(((rib_locations[i]-rib_locations[i-1])/2)+rib_locations[i-1]))

rib_locations.append(halfspan)
    
kv = 1.5
print(a)    
b_array = np.array(b)
a_array = np.array(a)
a_over_b = a_array/b_array
Ks_array = f_Kc(a_over_b)

def Kc_return(y):
    
    count = 0
    for i in rib_locations:
        if y <= i:
            return Ks_array[count]
        else:
            count +=1
    

def b_return(y):
    count = 0
    for i in rib_locations:
        
        if y <= i:
            return b_array[count]
        else:
            count +=1





def t_over_b(y):
    t_over_b = t_skin / wb_front_spar_h(y)
    return t_over_b

def sigma_critical(y):
    sigma = (np.pi**2*Kc_return(y)*E*t_over_b(y))/12*(1-nu**2)
    return sigma

#Empty lists
span = []
sigma_list = []
compressive = []

for i in np.arange(0, 27.83/2, 0.1):
    span.append(i)
    sigma_list.append(np.abs(sigma_critical(i)))
    compressive.append(np.abs(sigma_comp(i)))
    
pl1 = np.polyfit(span, sigma_list, 5)
plt.plot(span,sigma_list ,'r')
plt.plot(span, compressive, 'b')
# plt.plot(span, np.polyval(pl1, span))
plt.show()




#Safety margin = failure stress/applied stress
def failure_stress_skin(y):
    failure_stress = sigma_critical(y)
    return failure_stress


def applied_stress_skin(y):              #use stress due to compressive forces
    applied_stress = sigma_comp(y)
    return applied_stress


def Safety_margin_skin(y):
    val = np.abs(sigma_critical(y)/sigma_comp(y))
    return val

span = []
safety_margin = []
for i in np.arange(0,27.83/2,0.1):
    span.append(i)
    safety_margin.append(Safety_margin_skin(i))


plt.plot(span, safety_margin)
plt.show()


