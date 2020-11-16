import numpy as np
data = np.loadtxt("results.csv",delimiter=",",skiprows=1)

loads = data[:,6:]

max_index = np.argmax(loads)
max_n = np.amax(loads)
max_row = max_index // 6
max_h = data[max_row,0]
max_W = data[max_row,1]
max_Rho = data[max_row,2]

min_n = np.amin(loads)
#min_index = np.argmin(loads)
min_row = max_index // 6
min_h = data[min_row,0]
min_W = data[min_row,1]
min_Rho = data[min_row,2]

print(f"   , n     , W       , h  , Rho")
print(f"max, {max_n:6}, {max_h}, {max_W}, {max_Rho}")
print(f"min, {min_n:6}, {min_h}, {min_W}, {min_Rho}")