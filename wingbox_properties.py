import sys
import numpy as np
import scipy as sp
from scipy import interpolate, integrate
 
wingspan = 27.83 ;

#Defining variables for wingbox size at root and tip
root_le_h = 581.88/1000; #Height of leading edge of wingbox at root
root_te_h = 553.5/1000; #Height of trailing edge of wingbox at root
root_l = 1784/1000; #Length of wingbox at root
    
tip_le_h = 157.31/1000; #Height of leading edge of wingbox at tip
tip_te_h = 148.66/1000; #Height of trailing edge of wingbox at tip
tip_l = 484/1000; #Length of wingbox at tip
    
root_area = 0.5 * (root_le_h+root_te_h) * root_l #area of wingbox at root
tip_area = 0.5 * (tip_le_h+tip_te_h) * tip_l #area of winbox at tip

dz_0 = 35.7/1000; #Shift of the TE spar at root of wingbox
dz_1 = 10.3/1000; #Shif go the TE spar at tip of wingbox

m1 = 3212.13 #kg
m2 = 11742 #kg

te_z_root_h = dz_0
te_z_tip_h = dz_1
    
root_x_centroid = ((root_le_h + 2*root_te_h)/(3*(root_te_h + root_le_h)))*root_l;
tip_x_centroid = ((tip_le_h + 2*tip_te_h)/(3*(tip_te_h + tip_le_h)))*tip_l;
    
root_z_tri1 = (2/3) * te_z_root_h; #centroid of triangle 1 root
root_area_tri1 = 0.5 * root_l * te_z_root_h; #area of triangle 1 root
root_z_rect = 0.5 * root_te_h + te_z_root_h; #centroid of rencangle root
root_area_rect = root_l * root_te_h; #area of rectangle root
root_z_tri2 = (1/3) * ((root_te_h + te_z_root_h)- root_le_h) + te_z_root_h + root_te_h; #centroid of triangle 2 root
root_area_tri2 = 0.5 * ((root_te_h + te_z_root_h)- root_le_h) * root_l #area ot triangle 2 root
    
tip_z_tri1 = (2/3) * te_z_tip_h; # centroid of triangle 1 tip
tip_area_tri1 = 0.5 * tip_l * te_z_tip_h; #area of triangle 1 root
tip_z_rect = 0.5 * tip_te_h + te_z_tip_h; #centroid of rencangle tip
tip_area_rect = tip_l * tip_te_h; #area of rectangle tip
tip_z_tri2 = (1/3) * ((tip_te_h + te_z_tip_h)- tip_le_h) + te_z_tip_h + tip_te_h; #centroid of triangle 2 tip
tip_area_tri2 = 0.5 * ((tip_te_h + te_z_tip_h)- tip_le_h) * tip_l #area ot triangle 2 tip

root_top_panel = (root_l ** 2 + ((root_te_h + te_z_root_h)- root_le_h) ** 2) ** 0.5
root_bottom_panel = (root_l ** 2 + te_z_root_h ** 2) ** 0.5
tip_top_panel = (tip_l ** 2 + ((tip_te_h + te_z_tip_h)- tip_le_h) ** 2) ** 0.5
tip_bottom_panel = (tip_l ** 2 + te_z_tip_h ** 2) ** 0.5

rho = 2782 #kg/m^3
A_str = 120/(10**6) #m^2

density_al = 2.7*1000 #kg/m^3

def wb_area(b): #Calculates enclosed are of wingbox at a span location b in mm
    
    if b > (wingspan/2):
        print("Wingspan to calculate wingarea was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate wingarea was less than 0");
        sys.exit();
    
    #linear regression for area along wingspan
    
    m = -(root_area - tip_area)/(wingspan/2)
    c = root_area
    
    area = m*b + c
    
    return area;

def wb_centroid(b): #Calculates centroid of wingbox at a span location b in mm wrt bottom left corner, returns a list with the following coords (x,z).
    
    if b > (wingspan/2):
        print("Wingspan to calculate wb centroid was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate wb centroid was less than 0");
        sys.exit();
    
    root_z_centroid = (root_z_tri1 * root_area_tri1 + root_z_rect * root_area_rect + root_z_tri2 * root_area_tri2)/(root_area_tri1 + root_area_rect + root_area_tri2) #z pos of centroid for root wb
    tip_z_centroid = (tip_z_tri1 * tip_area_tri1 + tip_z_rect * tip_area_rect + tip_z_tri2 * tip_area_tri2)/(tip_area_tri1 + tip_area_rect + tip_area_tri2)    #z pos of centroid for tip wb
    
    #finding x centroid at span pos
    
    m = -(root_x_centroid - tip_x_centroid)/(wingspan/2);
    c = root_x_centroid;
    x_centroid = m*b + c;
    
    #finding z centroid at span pos
    
    m = -(root_z_centroid - tip_z_centroid)/(wingspan/2);
    c = root_z_centroid;
    z_centroid = m*b + c;
    
    return (x_centroid, z_centroid);
 
def bottompanel_dz(b):
    
    m = - (te_z_root_h - te_z_tip_h)/(wingspan/2)
    c = te_z_root_h
    dz = m*b + c
    
    return dz
   
def wb_front_spar_h(b): #Calculates the height of the front spar of the wb at a span pos in mm.
    
    if b > (wingspan/2):
        print("Wingspan to calculate front spar height was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate front spar height was less than 0");
        sys.exit();
        
    m = -(root_le_h - tip_le_h)/(wingspan/2);
    c = root_le_h;
    
    front_spar_h = m*b + c;
    
    return front_spar_h;

def wb_rear_spar_h(b): # Calculates the height of the rear spar of the wb at a span pos in mm
    
    if b > (wingspan/2):
        print("Wingspan to calculate rear spar height was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate rear spar height was less than 0");
        sys.exit();
        
    m = -(root_te_h - tip_te_h)/(wingspan/2);
    c = root_te_h;
    
    rear_spar_h = m*b + c;
    
    return rear_spar_h;

def wb_top_panel(b): #Calculates the width of the top panel of the wb at a span pos in mm
    
    if b > (wingspan/2):
        print("Wingspan to calculate top panel of wb was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate top panel of wb was less than 0");
        sys.exit();
        
    m = -(root_top_panel - tip_top_panel)/(wingspan/2);
    c = root_top_panel;
    top_panel = m * b + c;
    
    return top_panel;
        
def wb_bottom_panel(b): #Calculates the width of the bottom panel of the wb at a span pos in mm.
    
    if b > (wingspan/2):
        print("Wingspan to calculate top panel of wb was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate top panel of wb was less than 0");
        sys.exit();
          
    m = -(root_bottom_panel - tip_bottom_panel)/(wingspan/2);
    c = root_bottom_panel;
    bottom_panel = m * b + c;
    
    return bottom_panel;      

def J(b, t1, t2): #calculate J using formula for thin walled structures
    if b > (wingspan/2):
        print("Wingspan to calculate wingarea was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate wingarea was less than 0");
        sys.exit();
    
    A = wb_area(b)
    C = (wb_front_spar_h(b) + wb_rear_spar_h(b))/t1 + (wb_bottom_panel(b) + wb_top_panel(b))/t2 #demoninator of J
    
    J_t = 4*A**2/C
    return J_t

def I_xx(b, t1, t2): #calculate moment of inertia assume thin walled and spar as point area
    if b > (wingspan/2):
        print("Wingspan to calculate wingarea was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate wingarea was less than 0");
        sys.exit();
   
    #find moment of inertia using thin walled assumptions

    I_x_fs = t1*wb_front_spar_h(b)**3 / 12 #I around own axes
    I_x_rs = t1*wb_rear_spar_h(b)**3 / 12
    dz_fs = wb_centroid(b)[1] - wb_front_spar_h(b)/2 #steiner terms 
    dz_rs = -wb_centroid(b)[1] + ((dz_0-dz_1)/wingspan)*b + dz_0 + wb_rear_spar_h(b)/2

    I_xx_fs = I_x_fs + wb_front_spar_h(b)*t1 * dz_fs**2
    I_xx_rs = I_x_rs + wb_rear_spar_h(b)*t1 * dz_rs**2

    #for top  panel only the steiner terms are calculated as the moment around their x axis is considered negligible

    dz_bp = wb_centroid(b)[1] - ((dz_0-dz_1)/wingspan)*b /2
    dz_tp = -wb_centroid(b)[1] + wb_front_spar_h(b) + (((dz_0-dz_1)/wingspan)*b + dz_0 + wb_rear_spar_h(b) - wb_front_spar_h(b))
    I_x_bp = t2 *wb_bottom_panel(b)*(wb_bottom_panel(b)**2 * (((((dz_0-dz_1)/wingspan)*b + dz_0)/wb_bottom_panel(b))**2))

    I_xx_bp = wb_bottom_panel(b) * t2 * dz_bp**2 + I_x_bp
    I_xx_tp = wb_top_panel(b) * t2 * dz_tp**2

    I = I_xx_bp + I_xx_tp + I_xx_fs + I_xx_rs

    return I


spanlist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
span_inertias = []

for i in spanlist:      # clean wing box
    span_inertias.append(I_xx(i, 0.01, 0.01))


section = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 13.915]
section_top_str = [3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 0, 0, 0, 0]
section_bot_str = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0]
S1 = sp.interpolate.interp1d(section,section_top_str,kind="previous",fill_value="extrapolate")
S2 = sp.interpolate.interp1d(section, section_bot_str, kind="previous", fill_value="extrapolate")

string_inertias = []
#for i in spanlist:
    #string_inertias.append(I_xx_str(i, S1(i), S2(i), 1.2/10000))

def nstringer(b):
    if b > (wingspan/2):
        print("Wingspan to calculate wingarea was too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate wingarea was less than 0");
        sys.exit();

    n_top = float(S1(b))
    n_bottom =  float(S2(b))
    return n_top, n_bottom

def I_xx_str(b, area_str): #calculate I of stringers around x axis through centroid of wb
    if b > (wingspan/2):
        print("Wingspan to calculate stringer Moment of interta too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate stringer Moment of interta less than 0");
        sys.exit();     
    nstr_top, nstr_bot = nstringer(b)
    
    dist_bot = wb_centroid(b)[1] - (bottompanel_dz(b)/2)
    dist_top = wb_front_spar_h(b) - wb_centroid(b)[1] + ((bottompanel_dz(b) + wb_rear_spar_h(b) - wb_front_spar_h(b))/2)
     
    str_dist_bot = dist_bot - (area_str ** 0.5)/2
    str_dist_top = dist_top - (area_str ** 0.5)/2
     
    I_xx_str = nstr_bot * area_str * str_dist_bot ** 2 + nstr_top * area_str * str_dist_top ** 2

    return I_xx_str    

def S(b):
    S = 2*((0.5*root_l-0.5*tip_l)/(wingspan/2) * b + 0.5*tip_l*wingspan/2)
    return 2*S

def weight(b):
    if b > (wingspan/2):
        print("Wingspan to calculate weight too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate  weight less than 0");
        sys.exit();  
    C = (m1/2) / S(wingspan/2)
    m = S(b)* C
    
    w = 9.80665*m
    return w

def weight_f(b):
    if b > (wingspan/2):
        print("Wingspan to calculate fuel weight too high");
        sys.exit();
    if b < 0:
        print("Wingspan to calculate stringer weightless than 0");
        sys.exit();  
    C = ((m2)/2) / S(wingspan/2*0.75)
    if b <(wingspan/2*0.75) : 
        
        m = S(b)* C
    
        w = 9.80665*m
    else:
        w = S(wingspan/2*0.75)*C *9.80665

    return w

def wb_weight(t_spar, t_panel): #Calculates weight of entrie wingbox
    #inputs: t_spar: tickness in m of spars (front and rear)
            #t_panel: tickness in m of panels (top and bottom)
    
    a_front_spar = (wb_front_spar_h(0) + wb_front_spar_h(wingspan/2))*(wingspan/2)
    vol_front_spar = a_front_spar * t_spar
    
    a_rear_spar = (wb_rear_spar_h(0) + wb_rear_spar_h(wingspan/2))*(wingspan/2)
    vol_rear_spar = a_rear_spar * t_spar
    
    a_top_panel = (wb_top_panel(0) + wb_top_panel(wingspan/2))*(wingspan/2)
    vol_top_panel = a_top_panel * t_panel
    
    a_bottom_panel = (wb_bottom_panel(0) + wb_bottom_panel(wingspan/2))*(wingspan/2)
    vol_bottom_panel = a_bottom_panel * t_panel
    
    vol_stringers = 0
    
    for i in range(len(section)-1):        
        vol_stringers += 2 * (section_top_str[i] * A_str + section_bot_str[i] * A_str) * (section[i+1]-section[i])
    
    w = (vol_front_spar + vol_rear_spar + vol_top_panel + vol_bottom_panel + vol_stringers) * density_al
    
    return w
   
def Area_top(y):
    return wb_top_panel(y)*t + A_str*nstringer(y)[0]
 
# print(f"wing box weight = {wb_weight(0.005,0.005)}")
# print(f"J = {J(10.55, 0.006, 0.002)}")