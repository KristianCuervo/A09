import scipy as sp 
from scipy import interpolate
import txtreader as reader
import math
import numpy as np

def induced_drag_accent(y):
    q = float(input("What is the dynamic pressure?"))
    files = input("what is your file?")
    data = reader.filereader(files)
    y_array = data[0]
    chord_array = data[1]
    Ai_array = data[2]
    Cl_array = data[3]
    ICd_array = data[4]
    Di_array_2 = ICd_array*chord_array*q
    f_Di_2 = sp.interpolate.interp1d(y_array, Di_array_2, kind="cubic", fill_value="extrapolate")
    return(f_Di_2(y))

def moment_coeffecient_accent(y):
    q = float(input("What is the dynamic pressure?"))
    files = input("what is your file?")
    data = reader.filereader(files)
    y_array = data[0]
    chord_array = data[1]
    Cm_array = data[5]
    M_array = Cm_array*q*(chord_array**2)
    f_Cm = sp.interpolate.interp1d(y_array, M_array, kind="cubic", fill_value="extrapolate")
    return(f_Cm(y))








