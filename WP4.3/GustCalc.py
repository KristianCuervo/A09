from GustTools import *

#Constants
c = 2.834797715         #mean geometric chord [m]
S = 78.90625072         #wing surface area [m2]
C_L_alpha_M0 = 5.2      #base lift slope [1/rad]
C_L_max_clean = 1.514   #maximum lift coefficient (clean config) [-]
V_C = 250.8078156       #cruise velocity (TAS) [m/s]
Z_mo =                  #maximum operating altitude [m]
MTOW = 262631.8937      #maximum take off weight [N]
W_land_max =            #maximum landing weight [N]
ZFW_max = 147482.2094   #maximum zero fuel weight (OEW + Pay_max) [N]

g = 9.80665             #gravitational acceleration [m/s2]
Rho_0 = 1.225           #sea level density [kg/m3]
p_0 = 101325            #sea level pressure [Pa]
T_0 = 288.15            #sea level temperature [K]
gamma = 1.4             #specific heat ratios of air [-]
R = 298.05              #air specific gas constant [J/Kg K]

#Per diagram inputs
h =                     #considered altitude [m]
W =                     #weight considered [N]

#MaxGust
O = [0,1]

#V_B
V = V_B(W,h,U_ref1(h),S,c,V_C,C_L_alpha_M0,C_L_max_clean,g,R,Rho_0,T_0,p_0)
C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
H = H_max(c)
t = H_max(c)/V
U_ref = U_ref(h)
F_g = F_g(Z_mo, MTOW, W_land_max, ZFW_max)
U_ds = U_ds(U_ref,F_g,H)
dn = delta_n_s(t,V,W,h,U_ds,H,S,C_L_alpha,g,R,T_0,p_0)

B = [V,1+dn]
G = [V,1-dn]

#V_C
V = V_C
C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
H = H_max(c)
t = H_max(c)/V
U_ref = U_ref(h)
F_g = F_g(Z_mo, MTOW, W_land_max, ZFW_max)
U_ds = U_ds(U_ref,F_g,H)
dn = delta_n_s(t,V,W,h,U_ds,H,S,C_L_alpha,g,R,T_0,p_0)

C = [V,1+dn]
F = [V,1-dn]

#V_D
V = V_D(h,g,R,gamma,T_0,p_0)
C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
H = H_max(c)
t = H_max(c)/V
U_ref = U_ref(h)
F_g = F_g(Z_mo, MTOW, W_land_max, ZFW_max)
U_ds = U_ds(U_ref,F_g,H)
dn = delta_n_s(t,V,W,h,U_ds,H,S,C_L_alpha,g,R,T_0,p_0)

D = [V,1+dn]
E = [V,1-dn]
