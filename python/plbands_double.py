# This python script plots the band structure for magnetic systems, with states from spin up and spin down being compared

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import math
from read_Fermi import find_fermi


# Set the font and size for the axis labels
font = {'color': 'black',
        'weight': 'normal',
        'size': 14,
        }


# Define System Label
label=sys.argv[1]


# Read the data from the ASCII file. Extract energy values for spin up and down and k points in arrays.
band_dat = np.loadtxt(f'{label}-BANDS.dat')
k_up=[]
k_down=[]
E_up=[]
E_down=[]
for i in band_dat:
    if i[2]==1:
        k_up.append(i[0])
        E_up.append(i[1])
    else:
        k_down.append(i[0])
        E_down.append(i[1])

 
# Geometry of the figure
fig, (ax1,ax2) = plt.subplots(1,2, figsize=(7.87, 8.66))
plt.subplots_adjust(wspace=0, left=0.0825,right=1-0.0825, bottom=0.07, top=1 - 0.07)
plt.grid(False)
#fig.suptitle(f"Ferromagnetic {label.split('-x')[0]} band structure", fontsize=14)
#fig.suptitle("(b)", fontsize=14)


# Plot energy for spin up and down
ax1.plot(k_up, E_up, color="black", linestyle = 'None', marker = ".", markersize = 1.0)
ax2.plot(k_down, E_down, color="black", linestyle = 'None', marker = ".", markersize = 1.0)


# Sets the labels on the figure
if label.endswith("-F"):
    ax1.set_ylabel(r'E-E$_f$ (eV)', fontdict=font)
else:
    ax1.set_ylabel(r'E (eV)', fontdict=font)
fig.text(0.09+1/4*(1-0.09*2), 0.03, r'$\alpha$-spin', ha='center', va='center', fontsize=12)
fig.text(0.09+3/4*(1-0.09*2), 0.03, r'$\beta$-spin', ha='center', va='center', fontsize=12)


# Set the x-axis and y-axis limits
x_min = min(k_up)  
x_max = max(k_up)  
y_min = min(E_up)  
y_max= max(E_up)  
ax1.set_xlim(x_min,x_max)
ax2.set_xlim(x_min,x_max)
ax1.set_ylim(y_min,y_max)
ax2.set_ylim(y_min, y_max)


# Set the tick parameters
y_tick_spacing = 1
ax1.set_yticks(np.arange(y_min,  math.ceil(y_max), y_tick_spacing, int))
ax1.set_xticks(np.linspace(x_min, x_max, 2), [r'$\Gamma$', 'X'],ha='right')
ax1.tick_params(axis='y', direction='in', right=True, width=1.5)
ax1.tick_params(axis='x', labelsize=14, width=0)
ax2.set_yticks(np.arange(y_min,  math.ceil(y_max), y_tick_spacing, int), [])
ax2.set_xticks(np.linspace(x_min, x_max, 2), [r'$\Gamma$', 'X'], ha='left')
ax2.tick_params(axis='y', direction='in', width=1.5, right=True)
ax2.tick_params(axis='x', labelsize=14, width=0)


# Creates horizontal lines to show Fermi Level
if label.endswith('-F'):
    ax2.axhline(y=0, color='red', linestyle='--', linewidth=2)
    ax1.axhline(y=0, color='red', linestyle='--', linewidth=2)
else:
    ax2.axhline(y=find_fermi(label), color='red', linestyle='--', linewidth=2)
    ax1.axhline(y=find_fermi(label), color='red', linestyle='--', linewidth=2)


# Save the figure to a file
#plt.show()
fig.savefig(f'{label}-BS-Tex.png', dpi=400)