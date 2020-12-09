#COnstsnats
import numpy as np
from wingbox_properties import wb_front_spar_h,wb_rear_spar_h
import wingbox_properties as wb
import matplotlib.pyplot as plt
from TensileCompressiveStress import sigma_comp
t_skin = 1*10**-3           #m
E = 68.9 * 10**9
nu = 0.33
Kc = 7.5


def t_over_b(y):
    t_over_b = t_skin / wb_front_spar_h(y)
    return t_over_b

def sigma_critical(y):
    sigma = (np.pi**2*Kc*E*t_over_b(y))/12*(1-nu**2)
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


