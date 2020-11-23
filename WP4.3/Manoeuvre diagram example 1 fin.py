# importing the required module
import matplotlib.pyplot as plt
from math import *
from GustTools import TempPresRho

# naming the x axis
plt.xlabel('V')
# naming the y axis
plt.ylabel('n')

# giving a title to my graph
plt.title('Manuovering; MTOW & Alt')

# constants
S=78.906
C_lmaxclean=1.514
C_lmax=2.154
n_min=-1
MTOW = 262631.8937
rho0 = 1.2252
T0 = 273.15 + 15
P0 = 101325
lr = -0.0065
# R = 8.314         # This is the universal gas constant
R = 287.05
g = 9.80665
M = 0.0289644
gamma = 1.4
V_C_TAS = 250.80782

# def T(hm):
#     if hm<11000:
#         return T0 + lr*hm
#     else:
#         return 273.15-56
#
# def P(hm):
#     if hm < 11000:
#         return P0*(T0/(T0+lr*hm))**((g*M)/((R*lr)))
#     else:
#         return P0*e**((-g*M*hm)/(R*T0))
#
# def rho(P, T):
    # return (T0/lr)*(1-((P/P0)/(T/T0))**((lr*R)/(g*M-lr*R)))

def a(T):
    # return sqrt(gamma*R*T/M)      #???
    return sqrt(gamma*R*T)

def mach(a):
    return V_C_TAS / a

# def V_C_EAS(V_C_TAS, mach):
#     return V_C_TAS * mach           #???

def V_D_tas(mach, a):
    return (mach+0.05) * a

def V_A_tas(n,V_s1_tas):
    return V_s1_tas * sqrt(n)

def V_s1_tas(rho):
    return sqrt((2*MTOW)/(rho*C_lmaxclean*S))

def V_s1_eas(V_s1_tas, rho):
    return V_s1_tas*sqrt(rho/rho0)

def V_s0_tas(rho):
    return sqrt((2*MTOW)/(rho*C_lmax*S))

def V_s0_eas(V_s0_tas, rho):
    return V_s0_tas*sqrt(rho/rho0)

def V_F_tas(V_s1_tas):
    return 1.8*V_s1_tas

def V_F_eas(V_F_tas, rho):
    return V_F_tas * sqrt(rho / rho0)

def TAS(V_eas, rho):
    return V_eas * sqrt(rho0/rho)

def EAS(V_tas, rho):
    return V_tas * sqrt(rho/rho0)

def f(x):
    # return round(((x/50.22)**2.), 4)
    return round(((x/V_s0_eas)**2.), 4)

def h(x):
    return (x/59.905)**2


def l(x):
    return -(x/V_F_n1_eas)**2

def m(x):
    return (x/(V_D_EAS-V_C_EAS)) + (-1-(V_C_EAS/(V_D_EAS-V_C_EAS)))

def n(y):
    return 122.5763

# set variables
hm = 13106.4 #height considered
n_max = 3.598

P = TempPresRho(hm, g, R, T0, P0)[1]
T = TempPresRho(hm, g, R, T0, P0)[0]
rho = TempPresRho(hm, g, R, T0, P0)[2]
a = a(T)
print(f"a = {a}")
mach = mach(a)
print(f"mach = {mach}")
V_C_EAS = EAS(V_C_TAS, rho)
print(V_C_EAS)
V_D_EAS = EAS(V_D_tas(mach, a), rho)
print(V_D_EAS)
V_s1_tas = V_s1_tas(rho)
V_s1_eas = V_s1_eas(V_s1_tas, rho)
V_s0_tas = V_s0_tas(rho)
V_s0_eas = V_s0_eas(V_s0_tas, rho)
V_F_tas = V_F_tas(V_s1_tas)
V_F_eas = V_F_eas(V_F_tas, rho)
V_F_n1_eas = V_s0_eas * sqrt(1)
V_F_n2_eas = V_s0_eas * sqrt(2)
V_A_eas = EAS(V_A_tas(n_max, V_s1_tas), rho)
V_A_n2_eas = V_s1_eas * sqrt(2)

#Flaps down maximum
xg =[V_F_n2_eas, V_A_n2_eas]
yg = [2, 2]
plt.plot(xg, yg)

#Flaps down lift limited
xf = range(72)
yf = []
for n in xf:
    yf.append(f(n))
plt.plot(xf, yf)

#Flaps up lift limited
xh = range(int(V_A_eas)+1)
yh = []
for n in xh:
    yh.append(h(n))
plt.plot(xh, yh)

#Flaps up maximum
xi = [V_A_eas, V_D_EAS]
yi = [3.59, 3.59]
plt.plot (xi, yi)

#V_D limit
xz = [V_D_EAS, V_D_EAS]
yz = [0, 3.59]
plt.plot(xz, yz)

#Negative V_C to V_D
xm = [V_C_EAS, V_D_EAS]
ym = []
for n in xm:
    ym.append(m(n))
plt.plot(xm, ym)

#Negative maximum
xj = [V_F_n1_eas, V_C_EAS]
yj = [-1, -1]
plt.plot(xj, yj)

#Negative lift limited
xl = range(int(V_F_n1_eas)+1)
yl = []
for n in xl:
    yl.append(l(n))
plt.plot(xl, yl)

# function to show the plot
plt.show()