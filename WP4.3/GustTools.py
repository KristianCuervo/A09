def U(s,U_ds,H):
    from math import cos
    from math import pi
    U = (U_ds/2)*(1-cos(pi*s/H))
    return U

def U_ds(U_ref,F_g,H):
    U_ds = U_ref*F_g*(H/107)**(1/6)
    return U_ds

def H_max(c):
    H=max(107,12.5*c)
    return H

def U_ref1(h):
    h0 = 0
    n0 = 17.07
    h1 = 4572
    n1 = 13.41
    h2 = 18288
    n2 = 6.36

    U_ref1=n2
    if h<=h2:
        U_ref1 = n1 + ((n2-n1)/(h2-h1))*h
    if h<=4572:
        U_ref1 = n0 + ((n1-n0)/(h1-h0))*h
    return U_ref1

def U_ref2(h):
    U_ref2 = U_ref1(h) * 0.5
    return U_ref2

def V_S1(W,h,C_L_max_clean,S,g,R,T_0,p_0):
    from math import sqrt
    V_S1 = sqrt(W/(0.5*TempPresRho(h,g,R,T_0,p_0)[2]*S*C_L_max_clean))
    return V_S1

def V_B(W,h,U_ref,S,c,V_C,C_L_alpha,C_L_max_clean,g,R,Rho_0,T_0,p_0):
    from math import sqrt
    mu = (2*(W/S))/(TempPresRho(h,g,R,T_0,p_0)[2]*c*C_L_alpha*g)
    K_G = (0.88*mu)/(5.3+mu)
    V_B = V_S1(W,h,C_L_max_clean,S,g,R,T_0,p_0) * sqrt(1+((K_G*Rho_0*U_ref*V_C*C_L_alpha)/(2*(W/S))))
    return V_B

def V_D(h,g,R,gamma,T_0,p_0):
    from math import sqrt

    T = TempPresRho(h, g, R, T_0, p_0)[0]
    a = sqrt(gamma * R * T)
    V_D = a * (0.85+0.05)
    return V_D

def TempPresRho(h,g,R,T_0,p_0):
    from math import exp
    H = [0,11000,20000,32000,47000,51000,71000,86000]
    a = [-0.0065,0,0.001,0.0028,0,-0.0028,-0.002]
    T=T_0
    p=p_0

    lvl = 0
    def detlvl(h,lvl):
        if h > H[lvl+1]:
            lvl += 1
            lvl = detlvl(h,lvl)
        return lvl
    lvl = detlvl(h, lvl)

    for i in range(lvl+1):
        h_1 = min(h, H[i+1])
        T_1 = T + a[i]*(h_1-H[i])
        if a[i]==0:
            p_1 = p * exp(-(g/(R*T_1))*(h_1 - H[i]))
        else:
            p_1 = p * (T_1/T)**(-g/(a[i]*R))
        T=T_1
        p=p_1

    Rho = p/(R*T)
    return [T,p,Rho]

def F_g(Z_mo, MTOW, W_land_max, ZFW_max):
    from math import sqrt
    from math import tan
    from math import pi

    R_1 = W_land_max / MTOW
    R_2 = ZFW_max / MTOW
    F_gz = 1 - (Z_mo/76200)
    F_gm = sqrt(R_2 * tan(pi*R_1/4))
    F_g = 0.5 * (F_gz + F_gm)
    return F_g

def C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0):
    from math import sqrt

    T = TempPresRho(h,g,R,T_0,p_0)[0]
    a = sqrt(gamma*R*T)
    M = V/a
    C_L_alpha_M = C_L_alpha_M0 / sqrt(1-M**2)
    return C_L_alpha_M

def delta_n_s(t,V,W,h,U_ds,H,S,C_L_alpha,g,R,T_0,p_0):
    from math import cos
    from math import sin
    from math import exp
    from math import pi

    omega = pi*V/H
    Lambda = (W*2)/(S*C_L_alpha*TempPresRho(h,g,R,T_0,p_0)[2]*V*g)
    delta_n_s = (U_ds/(2*g))*((omega*sin(omega*t))+((1/(1+((omega*Lambda)**-2)))*(((exp(-t/Lambda))/Lambda)-((cos(omega*t))/Lambda)-(omega*sin(omega*t)))))
    return delta_n_s

def delta_n_s_max(h, V, U_ds, H, W, S, C_L_alpha, g, R, T_0, p_0):
    n_list = []
    t = 0
    t_max = 2*H / V
    while t <= t_max:
        n_list.append(delta_n_s(t,V,W,h,U_ds,H,S,C_L_alpha,g,R,T_0,p_0))
        t += 0.001
    n_max = max(n_list)
    return n_max


def CalcMaxGust(c,S,C_L_alpha_M0,C_L_max_clean,V_C,Z_mo,MTOW,W_land_max,ZFW_max,g,Rho_0,p_0,T_0,gamma,R,h,W,H):

    #V_B
    Uref = U_ref1(h)
    V = V_B(W,h,U_ref1(h),S,c,V_C,C_L_alpha_M0,C_L_max_clean,g,R,Rho_0,T_0,p_0)
    C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
    Fg = F_g(Z_mo,MTOW,W_land_max,ZFW_max)
    Uds = U_ds(Uref,Fg,H)
    dn = delta_n_s_max(h, V, Uds, H, W, S, C_L_alpha, g, R, T_0, p_0)

    B = 1+dn
    G = 1-dn

    #V_C
    Uref = U_ref1(h)
    V = V_C
    C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
    t = H_max(c)/V
    Fg = F_g(Z_mo, MTOW, W_land_max, ZFW_max)
    Uds = U_ds(Uref,Fg,H)
    dn = delta_n_s_max(h, V, Uds, H, W, S, C_L_alpha, g, R, T_0, p_0)

    C = 1+dn
    F = 1-dn

    #V_D
    Uref = U_ref2(h)
    V = V_D(h,g,R,gamma,T_0,p_0)
    C_L_alpha = C_L_alpha_M(V,h,C_L_alpha_M0,gamma,R,g,T_0,p_0)
    t = H_max(c)/V
    Fg = F_g(Z_mo, MTOW, W_land_max, ZFW_max)
    Uds = U_ds(Uref,Fg,H)
    dn = delta_n_s_max(h, V, Uds, H, W, S, C_L_alpha, g, R, T_0, p_0)

    D = 1+dn
    E = 1-dn

    return(B,G,C,F,D,E)