from math import sqrt
from wingbox_properties import *

t1 = 0.008                              #spar thickness (mm)
t2 = 0.0025                             #skin thickness (mm)

a_sea = 340.2922869                     #speed of sound (sea level)
a_cr = 295.0680184                      #speed of sound (cruise altitude)
rho_sea = 1.225012266                   #air density (sea level)
rho_cr = 0.2610636333                   #air density (cruise altitude)

dC_L_a_M0 = 6.336913214                 #reference lift slope
S = 78.91                               #wing surface area
c = 1.995932447                         #avg chord at ailerons
e = 0.1484304933                        #chord fraction distance of wb centroid to 1/4 chord

#C_L change due to aileron deflection (linear)
dC_L_e_sea_0 = 4.469070802
dC_L_e_sea_slope = 0.001428221586
dC_L_e_cr_0 = 4.526366582
dC_L_e_cr_slope = -0.0004034948745

#C_M change due to aileron deflection (linear)
dC_M_e_sea_0 = -0.5729577951
dC_M_e_sea_slope = 0.0008569329515
dC_M_e_cr_0 = -0.6302535746
dC_M_e_cr_slope = 0

G = 2.60E+10                            #shear stiffness (AL6061-T6)
J = J(10.55, t1, t2)                    #polar moment of inertia (external calculator)

def dC_L_a_sea(V):
    return dC_L_a_M0 / (sqrt(1-(V/a_sea)**2))

def dC_L_a_cr(V):
    return dC_L_a_M0 / (sqrt(1-(V/a_cr)**2))

def dC_L_e_sea(V):
    return dC_L_e_sea_0 + V*dC_L_e_sea_slope

def dC_L_e_cr(V):
    return dC_L_e_cr_0 + V*dC_L_e_cr_slope

def dC_M_e_sea(V):
    return dC_M_e_sea_0 + V*dC_M_e_sea_slope

def dC_M_e_cr(V):
    return dC_M_e_cr_0 + V*dC_M_e_cr_slope

def ail_eff_sea(V):
    top = (0.5*rho_sea*(V**2)*S*c*dC_M_e_sea(V)*dC_L_a_sea(V))+(G*J*dC_L_e_sea(V))
    bot = ((G*J)-(0.5*rho_sea*(V**2)*S*c*e*dC_L_a_sea(V)))
    return top/bot

def ail_eff_cr(V):
    top = (0.5*rho_cr*(V**2)*S*c*dC_M_e_cr(V)*dC_L_a_cr(V))+(G*J*dC_L_e_cr(V))
    bot = ((G*J)-(0.5*rho_cr*(V**2)*S*c*e*dC_L_a_cr(V)))
    return top/bot

def V_r_sea(V):
    top = -1*G*J*dC_L_e_sea(V)
    bot = 0.5*rho_sea*S*c*dC_M_e_sea(V)*dC_L_a_sea(V)
    return sqrt(top/bot)

def V_r_cr(V):
    top = -1*G*J*dC_L_e_cr(V)
    bot = 0.5*rho_cr*S*c*dC_M_e_cr(V)*dC_L_a_cr(V)
    return sqrt(top/bot)

def main_sea(V_i):
    V = V_i + 1
    ae = ail_eff_sea(V)
    try:
        if ae > 0:
            main_sea(V)
        else:
            main2_sea(V)
    except:
        print(f"V_r_sea beyond Mach 1")

def main2_sea(V_i):
    V = V_i - 0.001
    ae = ail_eff_sea(V)
    if ae < 0:
        main2_sea(V)
    else:
        print(f"V_r_sea = {V:.3f}")

def main_cr(V_i):
    V = V_i + 1
    ae = ail_eff_cr(V)
    try:
        if ae > 0:
            main_cr(V)
        else:
            main2_cr(V)
    except:
        print(f"V_r_cr beyond Mach 1")

def main2_cr(V_i):
    V = V_i - 0.001
    ae = ail_eff_cr(V)
    if ae < 0:
        main2_cr(V)
    else:
        print(f"V_r_cr = {V:.3f}")

main_sea(0)
main_cr(0)