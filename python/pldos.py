# This code plots the PDOS for non-magnetic systems (when DOS_up = DOS_dn)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import glob
from read_Fermi import find_fermi


# Set the font and size for the axis labels
font = {'color': 'black',
        'weight': 'normal',
        'size': 14,
        }


# Define System Label, Magnetic configuration and Fermi level for the system
label=sys.argv[1]
Fermi = find_fermi(label)
print(f'Fermi level at {Fermi} eV')
Mag=""
if "DIA" in label.split('-'):
    Mag="Diamagnetic"
elif "AFM" in label.split('-'):
    Mag="Antiferromagnetic"
else:
    Mag=''


# Reads the data from the total DOS from ASCII file. Extracts Energies and DOS in arrays. Shift energy with respect to Fermi.
total_dos_dat = np.loadtxt(f'{label}.DOS')
total_energy = total_dos_dat[:, 0]
total_dos = total_dos_dat[:, 1]
shifted_total_energy = total_energy - Fermi


# For each desired PDOS, add this block of command to extract their data 
"""
c_pdos = np.loadtxt('PDOS-C.dat')
c_energy = c_pdos[:, 0]
c_dos = c_pdos[:, 1]
shifted_c_energy= c_energy - Fermi
"""

if '2DBN' in label or 'ABN' in label:
    b_pdos = np.loadtxt('PDOS-B.dat')
    n_pdos = np.loadtxt('PDOS-N.dat')
    h_pdos = np.loadtxt('PDOS-H.dat')
    b_energy = b_pdos[:, 0]
    b_dos = b_pdos[:, 1]
    n_energy = n_pdos[:, 0]
    n_dos = n_pdos[:, 1]
    h_energy = h_pdos[:, 0]
    h_dos = h_pdos[:, 1]
    shifted_b_energy= b_energy - Fermi
    shifted_n_energy= n_energy - Fermi
    shifted_h_energy= h_energy - Fermi
else:
    c_pdos = np.loadtxt('PDOS-C.dat')
    #b_pdos = np.loadtxt('PDOS-B.dat')
    #n_pdos = np.loadtxt('PDOS-N.dat')
    #h_pdos = np.loadtxt('PDOS-H.dat')
    c_energy = c_pdos[:, 0]
    c_dos = c_pdos[:, 1]
    #b_energy = b_pdos[:, 0]
    #b_dos = b_pdos[:, 1]
    #n_energy = n_pdos[:, 0]
    #n_dos = n_pdos[:, 1]
    #h_energy = h_pdos[:, 0]
    #h_dos = h_pdos[:, 1]
    shifted_c_energy= c_energy - Fermi
    #shifted_b_energy= b_energy - Fermi
    #shifted_n_energy= n_energy - Fermi
    #shifted_h_energy= h_energy - Fermi


# Geometry of the figure
fig, ax = plt.subplots(figsize=(10.2, 7.5))
plt.subplots_adjust(left=0.07, right=1 - 0.07, bottom=0.084, top=1 - 0.084)
ax.grid(False)


# Plot of the total DOS
ax.plot(shifted_total_energy, total_dos, color="black", linewidth=1, label="Total DOS")


# For each desired PDOS, add this block of command to plot their PDOS
"""
ax.plot(shifted_b_energy, b_dos, color="hotpink", linewidth=1, label="B PDOS")
"""
if '2DBN' in label or 'ABN' in label:
    ax.plot(shifted_b_energy, b_dos, color="hotpink", linewidth=1, label="B PDOS")
    ax.plot(shifted_n_energy, n_dos, color="dodgerblue", linewidth=1, label="N PDOS")
    ax.plot(shifted_h_energy, h_dos, color="slategray", linewidth=1, label="H PDOS")
else:
    ax.plot(shifted_c_energy, c_dos, color="darkorange", linewidth=1, label="C PDOS")
#   plt.plot(shifted_b_energy, b_dos, color="pink", linewidth=1, label="B PDOS")
#   plt.plot(shifted_n_energy, n_dos, color="blue", linewidth=1, label="N PDOS")
#   plt.plot(shifted_h_energy, h_dos, color="yellow", linewidth=1, label="H PDOS")


# Sets the labels on the figure
ax.set_xlabel(r'E-E$_f$ (eV)',fontdict=font)
ax.set_ylabel('DOS (a.u)',fontdict=font)
#plt.suptitle(f'{Mag} {label.split("-x")[0]} PDOS', fontsize=14)
#if Mag=='Diamagnetic':
#    plt.suptitle('(a)', fontsize=14)
#else:
#    plt.suptitle('(c)', fontsize=14)


# Plot the pristine DOS if the script is called with second argument being 1
if int(sys.argv[2])==1:
    pristine_file=glob.glob('../BN/*.DOS')[0]
    pristine_dos_dat=np.loadtxt(pristine_file)
    pristine_energy=pristine_dos_dat[:,0]
    pristine_dos=pristine_dos_dat[:,1]
    shifted_pristine_energy=pristine_energy-Fermi
    print(f'Found and plotted {pristine_file}')
    ax.plot(shifted_pristine_energy,pristine_dos*14, color='gray', linestyle='--', label='Pristine 7ABNNR', linewidth=1, alpha=0.8)


# Set the x-axis and y-axis limits
x_min = min(shifted_total_energy)  
x_max = max(shifted_total_energy)   
y_min = min(total_dos) 
plt.xlim(x_min, x_max)
plt.ylim(y_min)


# Set the tick parameters
x_tick_spacing = 2  
#y_tick_spacing = 0.1 
plt.xticks(np.arange(x_min, x_max, x_tick_spacing, int))
#plt.yticks(np.arange(y_min, y_max, y_tick_spacing))
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.yaxis.set_minor_locator(plt.MultipleLocator(5))
plt.tick_params(axis='both', labelsize=12, direction='in', width=1.5, right=True, top=True)
ax.tick_params(axis='both', which='minor', direction='in', top=True, right=True, width=1)


# Save the figure to a file
ax.legend()
#plt.show()
fig.savefig(f'{label}-DOS-Tex.png', dpi=400)
