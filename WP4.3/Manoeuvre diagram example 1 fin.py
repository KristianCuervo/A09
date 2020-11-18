# importing the required module
from math import *
import matplotlib.pyplot as plt

# naming the x axis
plt.xlabel('V')
# naming the y axis
plt.ylabel('n)

# giving a title to my graph
plt.title('Manuovering; MTOW & Alt')


S=78.906
C_lmaxclean=1.514
C_lmax=2.154
n_max=3.598
n_min=-1
MTOW = 262631.89
rho0 = 1.2252
T0 = 273.15 + 15
P0 = 101325
lr = -0.0065
R = 8.314
g = 9.80665
M = 0.0289644
gamma = 1.4
V_C_TAS = 250.80782

def T(hm):
    if hm<11000:
        return T0 + lr*hm
    else:
        return -56

def P(hm):
    if hm < 11000:
        return P0*(T0/(T0+lr*hm))**((g*M)/((R*lr)))
    else:
        return P0*e**((-g*M*hm)/(R*T0))

def rho(P, T):
    return (T0/lr)*(1-((P/P0)/(T/T0))**((lr*R)/(g*M-lr*R)))

def a(T):
    return sqrt(gamma*R*T/M)

def mach(a):
    return V_C_TAS / a

def V_C_EAS(V_C_TAS, mach):
    return V_C_TAS * mach

def V_s1_tas(rho):
    return sqrt((2*MTOW))/(rho*C_lmaxclean*S)

def V_s1_eas(V_s1_tas, rho):
    return V_s1_tas*sqrt(rho/rho0)

def V_s0_tas(rho):
    return sqrt((2*MTOW))/(rho*C_lmax*S)

def V_s0_eas(V_s0_tas, rho):
    return V_s0_tas*sqrt(rho/rho0)

def V_F_tas(V_s1_tas):
    return 1.8*V_s1_tas

def V_F_eas(V_F_tas, rho):
    return V_F_tas * sqrt(rho / rho0)

def f(x):
    # return round(((x/50.22)**2.), 4)
    return round(((x/V_s0_eas)**2.), 4)

def h(x):
    return (x/59.905)**2


def l(x):
    return -(x/59.905)**2

def m(x):
    return (x/(122.5763-115.7665)) + (-1-(115.7665/(122.5763-115.7665)))

def n(y):
    return 122.5763


xg =[71.022, 84.718]
yg = [2, 2]
plt.plot(xg, yg)

xf = range(72)
yf = []
for n in xf:
    yf.append(f(n))
plt.plot(xf, yf)

xh = range(114)
yh = []
for n in xh:
    yh.append(h(n))
plt.plot(xh, yh)

xi = [113.504, 122.573]
yi = [3.59, 3.59]
plt.plot (xi, yi)

xz = [122.573, 122.573]
yz = [0, 3.59]
plt.plot(xz, yz)

xm = [115.7665, 122.5763]
ym = []
for n in xm:
    ym.append(m(n))
plt.plot(xm, ym)

xj = [59.905, 115.7665]
yj = [-1, -1]
plt.plot(xj, yj)

xl = range(60)
yl = []
for n in xl:
    yl.append(l(n))
plt.plot(xl, yl)

# function to show the plot
plt.show()