from txtreader import filereader ### Import this file from github (txtreader.py)
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import interpolate, integrate
from wingbox_properties import wb_centroid , weight

def interpolation(x_coor, array_x, array_y):
    f = sp.interpolate.interp1d(array_x, array_y, kind = 'cubic', fill_value = 'extrapolate') 
    return f(x_coor)

############ Constants
span        = filereader("MainWing_a10.00_v10.00ms.txt")[0]     #this file is available in the discord
chord       = filereader("MainWing_a10.00_v10.00ms.txt")[1]
CL_0_dist   = filereader("MainWing_a0.00_v10.00ms.txt")[3] 
CL_10_dist  = filereader("MainWing_a10.00_v10.00ms.txt")[3]
Cdi_0_dist  = filereader("MainWing_a0.00_v10.00ms.txt")[4] 
Cdi_10_dist = filereader("MainWing_a10.00_v10.00ms.txt")[4]
Cm_0        = filereader("MainWing_a0.00_v10.00ms.txt")[5]
Cm_10       = filereader("MainWing_a10.00_v10.00ms.txt")[5]    
Xcp_0_frac  = filereader("MainWing_a0.00_v10.00ms.txt")[7]
Xcp_10_frac = filereader("MainWing_a10.00_v10.00ms.txt")[7]

CL_0   = 0.2688          # total CL at aoa =  0 deg from XFLR5 file
CL_10  = 1.03017         # total CL at aoa = 10 deg from XFLR5 file
Cdi_0  = 0.002635        # induced drag at aoa = 0
Cdi_10 = 0.033823        # induced drag at aoa = 10

K1 = Cdi_0/(CL_0**2)     # drag constant Cdi = K*cl^2 with aoa = 0
K2 = Cdi_10/(CL_10**2)   # drag constant Cdi = K*cl^2 with aoa = 10
K  = (K1+K2)/2           # take the mean of the two drag constants because they differ


############ Inputs
rho     = 1.225                   #kg/m^3 (given from altitude)
W       = 26781*9.81              #weight of aircraft in chosen config [N]
V       = 90                      #free stream velocity [m/s]
q       = 0.5*rho*V**2            #dynamic pressure
S       = 78.91                   #surface area wing [m^2]
n       = 1.5                     #load factor found from wp4.3

############ OUTPUTS

######################################### LIFT AND AOA



CL_desired = CL_d = 2*n*W/(rho*V**2*S)
print('\ndesired CL', round(CL_d, 4))

#find angle of attack corresponding to desired CL:
aoa_d = (np.arcsin((CL_d - CL_0)/(CL_10-CL_0)*np.sin(10*np.pi/180)))
print('\ndesired angle of attack', round(aoa_d*180/np.pi, 3), 'degrees', 'or', round(aoa_d, 4) , 'radians')

##new desired Lift distribution
CL_d_dist = CL_0_dist +((CL_d - CL_0)/(CL_10-CL_0))*(CL_10_dist-CL_0_dist)
#print('desired' , CL_d_dist)

def L_accent(y):  #y is location that we're interested in, CL is array, c = chord array, q is constant = 1/2rhoV**2, span = span array
    CL_y = interpolation(y, span, CL_d_dist)
    c_y = interpolation(y, span, chord)
    L_accent = CL_y*q*c_y
    return L_accent

L_accent_array = np.array([])
span_array = np.array([])

for i in np.arange(0, 13.916, .001):
    span_array = np.append(span_array, i)
    L_accent_array = np.append(L_accent_array, L_accent(i))

#plot the lift distribution

#####plt.plot(span_array, L_accent_array, label = 'Lift per unit span [N/m]')


########################################## DRAG
Cdi_desired = Cdi_d = K*CL_d**2
#print('\ninduced drag coefficient desired cdi_d:', Cdi_d)

##  new induced drag distribution
Cdi_d_dist = Cdi_0_dist +((Cdi_d - Cdi_0)/(Cdi_10-Cdi_0))*(Cdi_10_dist-Cdi_0_dist)
#print('new induced drag distribution:', Cdi_d_dist)

def Di_accent(y):  #y is location that we're interested in, Cdi_d_dist is desired induced drag array, c = chord array, q is constant = 1/2rhoV**2, span = span array
    Cdi_y = interpolation(y, span, Cdi_d_dist)
    c_y = interpolation(y, span, chord)
    Di_accent = Cdi_y*q*c_y
    return Di_accent

######## NORMAL
def Normalforce(y):         #Normal force dependent on span-position
    Normal = L_accent(y)*np.cos(aoa_d)+Di_accent(y)*np.sin(aoa_d) + weight(y)
    return Normal

totalnormal = sp.integrate.quad(Normalforce, 0, 13.916)[0]
print('total Normal', totalnormal) #Total normal force which becomes negative internal shear at root

def Shearforce(y):
    Shear = -totalnormal + sp.integrate.quad(Normalforce, 0, y)[0]   #above calculated totalnormal is subtracted at the root
    return Shear

span1_array = np.array([])      #create empty arrays to store data
normal_array = np.array([])
for i in np.arange(0, 13.916, .1):
    span1_array = np.append(span1_array, i)
    normal = Normalforce(i)       
    normal_array = np.append(normal_array, normal)
plt.plot(span1_array, normal_array, label = 'NormalForce along span [N]')   

########## SHEAR        same procedure as above
span_array  = np.array([])
shear_array = np.array([])
for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)       
    shear_array = np.append(shear_array, Shearforce(i))

plt.plot(span_array, shear_array, label = 'ShearForce along span [N]')

######## Moment

def Momentforce(y):
    Moment = sp.integrate.quad(Shearforce, 0, y)[0]
    return Moment

totalmoment = -Momentforce(13.196)          #gives negative value while the bending moment at the root must be positive -> minus sign
print('total moment at root', totalmoment)
Moment_array = np.array([])
span_array = np.array([])

""" for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)
    moment = totalmoment + Momentforce(i)       #momentforce(i) gives negative values here so
    Moment_array = np.append(Moment_array, moment)
plt.plot(span_array, Moment_array, label = 'Moment along span [N/m]')
plt.legend()        #makes the labels visible
plt.show()          #show all the 3 plots in one diagram """

######################## REPEAT CALCULATIONS BUT WITH FUEL


######## NORMAL
def Normalforce1(y):         #Normal force dependent on span-position
    Normal = L_accent(y)*np.cos(aoa_d) - Di_accent(y)*np.sin(aoa_d) - weight(y) - weight_f(y)
    return Normal

totalnormal1 = sp.integrate.quad(Normalforce1, 0, 13.916)[0]
print('total Normal', totalnormal1) #Total normal force which becomes negative internal shear at root

def Shearforce1(y):
    Shear = -totalnormal1 + sp.integrate.quad(Normalforce1, 0, y)[0]   #above calculated totalnormal is subtracted at the root
    return Shear

span_array = np.array([])      #create empty arrays to store data
normal1_array = np.array([])
for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)
    normal = Normalforce1(i)       
    normal_array1 = np.append(normal1_array, normal)
plt.plot(span_array, normal1_array, label = 'NormalForce along span [N]')   

########## SHEAR        same procedure as above
span_array  = np.array([])
shear1_array = np.array([])
for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)       
    shear1_array = np.append(shear1_array, Shearforce1(i))

plt.plot(span_array, shear1_array, label = 'ShearForce along span [N]')

######## Moment

def Momentforce1(y):
    Moment = sp.integrate.quad(Shearforce1, 0, y)[0]
    return Moment

totalmoment1 = -Momentforce1(13.196)          #gives negative value while the bending moment at the root must be positive -> minus sign
print('total moment at root', totalmoment)
Moment1_array = np.array([])
span_array = np.array([])

for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)
    moment = totalmoment1 + Momentforce1(i)       #momentforce(i) gives negative values here so
    Moment1_array = np.append(Moment1_array, moment)
plt.plot(span_array, Moment1_array, label = 'Moment along span [N/m]')
plt.legend()        #makes the labels visible
plt.show()          #show all the 3 plots in one diagram


############## TORQUE DIAGRAM

def TorqueFunc(y):   #Return torque at a specific position of span 
    
    #desired AoA
    c_y = interpolation(y, span, chord)
    cp_x_10 = interpolation(y, span, Xcp_10_frac )
    cp_x_0 = interpolation(y, span, Xcp_0_frac )

    #also add moment calculation because life is meaningless
    CM_0 = interpolation(y, span , Cm_0)
    CM_10 = interpolation(y, span, Cm_10)
    Cm_alpha = (CM_10-CM_0)/np.radians(10)
    Cm = Cm_alpha*aoa_d + CM_0
    Mom = Cm*q*c_y**2

    #Calculate position of c.p. at span pos (y)
    cp_x_alpha = (cp_x_10-cp_x_0)/np.radians(10)
    cp_x = aoa_d * cp_x_alpha + cp_x_0
    
    #Import positon of centroid of wing
    wingbox_centroid_pos_x, wingbox_centroid_pos_z  = wb_centroid(y)
    wingbox_airfoil_centroid_x = (wingbox_centroid_pos_x/c_y)+0.2 #percentage of chord
    d1 = cp_x - (wingbox_airfoil_centroid_x * c_y)#distance between cp x position and centroid x position    
        
    torque = Normalforce(y) * d1  + Mom#Normal force * distance 
    


    return torque

torque_array = []
max_torque = -TorqueFunc(13.915)

for i in np.arange(0, 13.916, .1):
    span_array = np.append(span_array, i)
    torque = TorqueFunc(i) + max_torque #momentforce(i) gives negative values here some
    
    
    torque_array = np.append(torque_array, torque)


plt.plot(span_array, torque_array, label = 'Torque along span (around y-axis) [N/m]')
plt.legend()        #makes the labels visible
plt.show()          #show all the 3 plots in one diagram 
