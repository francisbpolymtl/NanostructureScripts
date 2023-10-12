# This python script plots the band structure for non-magnetic systems (when DOS_up = DOS_dn)

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


# Define System Label and Magnetic configuration for the system
label=sys.argv[1]
Mag = None
if "DIA" in label.split('-'):
    Mag="Diamagnetic"
elif "AFM" in label.split('-'):
    Mag="Antiferromagnetic"
else:
    Mag=''


# Read the data from the ASCII file. Extract energy values and k points in arrays.
band_dat = np.loadtxt(f'{label}-BANDS.dat')
k = band_dat[:, 0]
E = band_dat[:, 1]


# Geometry of the figure
fig, ax = plt.subplots(figsize=(4.5, 8.66))
plt.subplots_adjust(left=0.1444, right=1 - 0.1444, bottom=0.07, top=1 - 0.07)
ax.grid(False)


# Plot energy
ax.plot(k, E, color="black", linestyle = 'None', marker = ".", markersize = 1.0)


# Sets the labels on the figure
if label.endswith("-F"):
    ax.set_ylabel(r'E-E$_f$ (eV)',fontdict=font)
else:
    ax.set_ylabel(r'E (eV)',fontdict=font)
#plt.suptitle(f'{Mag} {label.split("-x")[0]} band structure', fontsize=14)
#if Mag=='Diamagnetic':
#    plt.suptitle('(a)', fontsize=14)
#else:
#    plt.suptitle('(c)', fontsize=14)


# Set the x-axis and y-axis limits
x_min = min(k)  
x_max = max(k)  
y_min = min(E)  
y_max = max(E)  
plt.ylim(y_min,y_max)
plt.xlim(x_min,x_max)


# Set the tick parameters
y_tick_spacing = 1 
plt.yticks(np.arange(y_min,  y_max, y_tick_spacing, int))
plt.xticks(np.linspace(x_min, x_max, 2), [r'$\Gamma$', 'X'])
plt.tick_params(axis='x', labelsize=14, width=0)
plt.tick_params(axis='y', width=1.5, direction='in', right=True)


# Creates horizontal lines to show Fermi Level
if label.endswith('-F'):
    plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
else:
    plt.axhline(y=find_fermi(label), color='red', linestyle='--', linewidth=2)


# Save the figure to a file
#plt.show()
fig.savefig(f'{label}-BS-Tex.png', dpi=400) 