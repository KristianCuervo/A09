def U(U_ds,s,H):
    #U_ds = design gust velocity [m/s]
    #s = distance into gust gradient s=[0,2H] [m]
    #H = gust gradient distance [m]
    from math import cos
    from math import pi
    U = (U_ds/2)*(1-cos(pi*s/H))
    return U

def U_ds(U_ref,F_g,H):
    #U_ref = reference gust velocity [m/s]
    #F_g = flight alleviation factor
    #H = gust gradient distance [m]
    U_ds = U_ref*F_g*(H/107)**(1/6)
    return U_ds

def H_max(c):
    #c = mean aerodynamic chord [m]
    H=max(107,12.5*c)
    return H

def U_ref1(h):
    #h = altitude [m]
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

def V_B(V_S1, U_ref, V_C, C_L_alpha, W, Rho, c):
    #V_S1 = clean config stall velocity (EAS) [m/s]
    #U_ref = reference gust velocity [m/s]
    #V_C = cruise velocity (EAS) [m/s]
    #C_L_alpha = lift slope [1/rad]
    #W = weight considered [N]

    from math import sqrt
    Rho_0 = 1.225
    g = 9.80665

    mu = (2*(W/S))/(Rho*c*C_L_alpha*g)
    K_G = (0.88*mu)/(5.3+mu)
    V_B = V_S1 * sqrt(1+((K_G*Rho_0*U_ref*V_C*C_L_alpha)/(2*(W/S))))
    return V_B

def TempPresRho(h):
    #h = altitude [m]

    from math import exp

    H = [0,11000,20000,32000,47000,51000,71000,86000]
    a = [-0.0065,0,0.001,0.0028,0,-0.0028,-0.002]
    g = 9.80665
    R = 287.05
    T=288.15
    p=101325

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
    #Z_mo = maximum operating altitude [m]
    #MTOW = maximum take off weight [N]
    #W_land_max = maximum landing weight [N]
    #ZFW_max = maximum zero fuel weight [N]

    from math import sqrt
    from math import tan
    from math import pi

    R_1 = W_land_max / MTOW
    R_2 = ZFW_max / MTOW
    F_gz = 1 - (Z_mo/76200)
    F_gm = sqrt(R_2 * tan(pi*R_1/4))
    F_g = 0.5 * (F_gz + F_gm)
    return F_g

def C_L_alpha_M(V,h):

    from math import sqrt
    gamma = 1.4
    R = 287.05
    C_L_alpha_M0 = 5.2

    T = TempPresRho(h)[0]
    a = sqrt(gamma*R*T)
    M = V/a
    C_L_alpha_M = C_L_alpha_M0 / sqrt(1-M**2)
    return C_L_alpha_M

def delta_n_s(t,U_ds,V,H,W,C_L_alpha,rho):
    #t = time into gust [s]
    #U_ds = design gust velocity [m/s]
    #V = velocity (TAS) [m/s]
    #H = gust gradient length [m]
    #W = weight considered [N]
    #C_L_alpha = lift slope [1/rad]
    #rho = air density [kg/m3]

    from math import cos
    from math import sin
    from math import exp
    from math import pi
    g = 9.80665
    S = 78.90625072

    omega = pi*V/H
    Lambda = (W*2)/(S*C_L_alpha*rho*V*g)
    delta_n_s = (U_ds/(2*g))*((omega*sin(omega*t))+((1/(1+(omega*Lambda)**-2))*((exp(-t/Lambda)/Lambda)-(cos(omega*t)/Lambda)-(omega*sin(omega*t)))))
    return delta_n_s