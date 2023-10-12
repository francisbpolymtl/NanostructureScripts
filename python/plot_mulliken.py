# This script plot the spin density on a 2D structure provided by the output of the python script read_mulliken.py

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import sys
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# Function that read data from ann xyz file with the fourth column to be plotted as a colormap on the atom position
def read_atom_positions(filename):
    atoms = []
    x_coords = []
    y_coords = []
    colors = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip().split():
                if line.strip().split()[0].isalpha():
                    atom, x, y, z, color = line.strip().split()
                    atoms.append(atom)
                    x_coords.append(float(x))
                    y_coords.append(float(y))
                    colors.append(float(color))
    return atoms, x_coords, y_coords, colors

# Function that plot circles at each xy position with color corresponding to the fourth column of the xyz file. It also adds lines between atoms position. Change the threshold to change the allowed bond lenght.
def plot_atom_positions_with_lines_and_circles(atoms, x_coords, y_coords, colors, threshold=1.5):
    plt.figure()

    # Creates lines between positions
    segments = []
    for i in range(len(x_coords)):
        for j in range(i + 1, len(x_coords)):
            dist = ((x_coords[i] - x_coords[j])**2 + (y_coords[i] - y_coords[j])**2)**0.5
            if dist < threshold:
                segments.append([(x_coords[i], y_coords[i]), (x_coords[j], y_coords[j])])

    # Add line collection to the plot
    lc = LineCollection(segments, linewidths=1.5, colors='black', alpha=1.0)
    plt.gca().add_collection(lc)

    # Plot the circles above the atoms with specified colors
    v_min=min(colors)
    v_max=max(colors)
    abs_max=max([abs(v_min),abs(v_max)])
    print(colors)
    print(abs_max)
    plt.scatter(x_coords, y_coords, s=150, marker='o', c=colors, edgecolors=None, cmap='bwr', vmin=-abs_max, vmax=abs_max)

    # Add atom labels to some atom's position
    for i, atom in enumerate(atoms):
        if atom == 'C':
            plt.text(x_coords[i], y_coords[i]-0.2, atom, ha='center', va='top', fontsize=16)

    # Define geometry of the plot
    plt.axis('equal')

    cbar = plt.colorbar()
    cbar.set_label(label=r"$\mu_B$", size=15, weight='bold', rotation=0)  
    cbar.ax.yaxis.set_label_coords(-1.5, 0.5) 
    plt.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
    plt.box(False)
    plt.savefig(f'{label}-Mag.png', dpi=350)

if __name__ == '__main__':
    label=sys.argv[1]
    filename = f'{label}-Mag.xyz' 
    atoms, x_coords, y_coords, colors = read_atom_positions(filename)
    plot_atom_positions_with_lines_and_circles(atoms, x_coords, y_coords, colors, threshold=1.6)
    print(f'Plotted {label}-Mag.png succesfully')
