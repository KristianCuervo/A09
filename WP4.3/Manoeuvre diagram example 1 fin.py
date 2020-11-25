# importing the required module
import matplotlib.pyplot as plt
import numpy as np
from math import *
from GustTools import *

# constants
S=78.906
c=2.834797715
C_lmaxclean=1.514
C_lmax=2.154
C_L_alpha_M0=5.2
n_min=-1
MTOW = 262631.8937
OEW = 122347.7654
W_land_max = 144928.7383
ZFW_max = 147482.2094
Z_mo = 13106.4
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



#Replaced these, they don't seem to be working properly
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

def get_n_max(W):
    return (max(2.5,(min(3.8,(2.1+(24000/((0.224809*W/g)+10000)))))))

def f(x):
    # return round(((x/50.22)**2.), 4)
    return round(((x/V_s0_eas)**2.), 4)

def h(x):
    return (x/V_s1_eas)**2


def l(x):
    return -(x/V_F_n1_eas)**2

# def m(x):                     #straight line, integrated into plt call
#     return (x/(V_D_EAS-V_C_EAS)) + (-1-(V_C_EAS/(V_D_EAS-V_C_EAS)))

# def n(y):                     #this doesn't seem to do anything
#     return 122.5763

def d_n(t):
    return delta_n_s(t,V_C_TAS,W,hm,U_ds,H,S,C_L_alpha,g,R,T0,P0)

# set variables
#height considered
hm = 0
#weight considered
W = OEW

n_max = get_n_max(W)
P = TempPresRho(hm, g, R, T0, P0)[1]
T = TempPresRho(hm, g, R, T0, P0)[0]
rho = TempPresRho(hm, g, R, T0, P0)[2]
a = a(T)
mach = mach(a)
V_C_EAS = EAS(V_C_TAS, rho)
V_D_EAS = EAS(V_D_tas(mach, a), rho)
V_B_EAS = EAS(V_B(W,hm,U_ref1(hm),S,c,V_C_TAS,C_L_alpha_M0,C_lmaxclean,g,R,rho0,T0,P0), rho)
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
gust_points = CalcMaxGust(c,S,C_L_alpha_M0,C_lmaxclean,V_C_TAS,Z_mo,MTOW,W_land_max,ZFW_max,g,rho0,P0,T0,gamma,R,hm,W)
H = H_max(c)
C_L_alpha = C_L_alpha_M(V_C_TAS,hm,C_L_alpha_M0,gamma,R,g,T0,P0)
t_max = (2*H)/V_C_TAS
U_ds = U_ds(U_ref1(hm), F_g(Z_mo, MTOW, W_land_max, ZFW_max), H)

#Plotting Load Diagram
plt.figure()
# naming the x axis
plt.xlabel('V')
# naming the y axis
plt.ylabel('n')

# giving a title to my graph
plt.title('Load Diagram; OEW & Sea-Level Altitude')

#Flaps down maximum
xg =[V_F_n2_eas, V_A_n2_eas]
yg = [2, 2]
plt.plot(xg, yg, 'm')

#Flaps down lift limited
xf = list(range(int(V_F_n2_eas)))
xf.append(V_F_n2_eas)
yf = []
for n in xf:
    yf.append(f(n))
plt.plot(xf, yf, 'm')

#Flaps up lift limited
xh = list(range(int(V_A_eas)))
xh.append(V_A_eas)
yh = []
for n in xh:
    yh.append(h(n))
plt.plot(xh, yh, 'b')

#Flaps up maximum
xi = [V_A_eas, V_D_EAS]
yi = [n_max, n_max]
plt.plot (xi, yi, 'b')

#V_D limit
xz = [V_D_EAS, V_D_EAS]
yz = [0, n_max]
plt.plot(xz, yz, 'b')

#Negative V_C to V_D
xm = [V_C_EAS, V_D_EAS]
ym = [-1, 0]
plt.plot(xm, ym, 'b')

#Negative maximum
xj = [V_F_n1_eas, V_C_EAS]
yj = [-1, -1]
plt.plot(xj, yj, 'b')

#Negative lift limited
xl = list(range(int(V_F_n1_eas)))
xl.append(V_F_n1_eas)
yl = []
for n in xl:
    yl.append(l(n))
plt.plot(xl, yl, 'b')

#top
x_gust_top = [0,V_B_EAS,V_C_EAS,V_D_EAS]
y_gust_top = [1,gust_points[0],gust_points[2],gust_points[4]]
plt.plot(x_gust_top, y_gust_top, 'r')

#bot
x_gust_bot = [0,V_B_EAS,V_C_EAS,V_D_EAS]
y_gust_bot = [1,gust_points[1],gust_points[3],gust_points[5]]
plt.plot(x_gust_bot, y_gust_bot, 'r')

#vertical
x_gust_ver = [V_D_EAS, V_D_EAS]
y_gust_ver = [gust_points[4], gust_points[5]]
plt.plot(x_gust_ver, y_gust_ver, 'r')

#V_S1
x_V_s1 = [V_s1_eas, V_s1_eas]
y_V_s1 = [0, 1]
plt.plot(x_V_s1,y_V_s1,'k--')
#V_A
x_V_A = [V_A_eas, V_A_eas]
y_V_A = [0, n_max]
plt.plot(x_V_A,y_V_A,'k--')
#V_C
x_V_C = [V_C_EAS, V_C_EAS]
y_V_C = [0, min(n_max,h(V_C_EAS))]
plt.plot(x_V_C,y_V_C,'k--')

#horizontal axis line
plt.axhline(color="black")

#Plotting Gust Variation
plt.figure()
t_gust_arr = np.linspace(0,t_max,100)
n_gust_arr = np.zeros(len(t_gust_arr))
for n in range(len(t_gust_arr)):
    n_gust_arr[n] = (1+d_n(t_gust_arr[n]))
t_gust = t_gust_arr.tolist()
n_gust = n_gust_arr.tolist()
plt.plot(t_gust, n_gust)

# function to show the plot
plt.show()