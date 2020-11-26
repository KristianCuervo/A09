from GustTools import *
import numpy as np

#Constants
c = 2.834797715         #mean geometric chord [m]
S = 78.90625072         #wing surface area [m2]
C_L_alpha_M0 = 5.2      #base lift slope [1/rad]
C_L_max_clean = 1.514   #maximum lift coefficient (clean config) [-]
V_C = 250.8078156       #cruise velocity (TAS) [m/s]
Z_mo = 13106.4          #maximum operating altitude [m]
MTOW = 262631.8937      #maximum take off weight [N]
W_land_max = 144928.7383#maximum landing weight [N]
ZFW_max = 147482.2094   #maximum zero fuel weight (OEW + Pay_max) [N]

g = 9.80665             #gravitational acceleration [m/s2]
Rho_0 = 1.225           #sea level density [kg/m3]
p_0 = 101325            #sea level pressure [Pa]
T_0 = 288.15            #sea level temperature [K]
gamma = 1.4             #specific heat ratios of air [-]
R = 287.05              #air specific gas constant [J/Kg K]

#Print Results
def Print_Results(W,h,H,g,R,T_0,p_0,V_B,V_C,V_D,B,G,C,F,D,E):
    file = open("results.csv","a")
    text = f"{W:6.0f},{h:6.0f},{H},{TempPresRho(h,g,R,T_0,p_0)[2]:6.3f},{V_B:6.2f},{V_C:6.2f},{V_D:6.2f},{B:6.3f},{G:6.3f},{C:6.3f},{F:6.3f},{D:6.3f},{E:6.3f}"
    file.write("\n" + text)
    print(text)
    file.close()

#main
hlist = np.loadtxt("input.csv",delimiter=",",skiprows=1,usecols=[0])
Wlist = np.loadtxt("input.csv",delimiter=",",skiprows=1,usecols=[1])
Hlist = np.loadtxt("input.csv",delimiter=",",skiprows=1,usecols=[2])

print(f"W     ,h     ,H     ,Rho   ,V_B   ,B     ,G     ,V_C   ,C     ,F     ,V_D   ,D     ,E")
for i in range(len(hlist)):
    h = hlist[i]
    W = Wlist[i]
    H = Hlist[i]

    Points = CalcMaxGust(c,S,C_L_alpha_M0,C_L_max_clean,V_C,Z_mo,MTOW,W_land_max,ZFW_max,g,Rho_0,p_0,T_0,gamma,R,h,W,H)
    Velocities = [V_B(W,h,U_ref1(h),S,c,V_C,C_L_alpha_M0,C_L_max_clean,g,R,Rho_0,T_0,p_0),V_C,V_D(h,g,R,gamma,T_0,p_0)]
    Print_Results(W,h,H,g,R,T_0,p_0,Velocities[0],Velocities[1],Velocities[2],Points[0],Points[1],Points[2],Points[3],Points[4],Points[5])
