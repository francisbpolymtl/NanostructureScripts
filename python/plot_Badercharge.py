import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import sys
import argparse

# Get the label from command-line argument
label = sys.argv[1]

# Read atom positions from a PDB file
def read_atom_positions_pdb(filename):
    atoms = []
    x_coords = []
    y_coords = []
    colors = []
    
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('HETATM') or line.startswith('ATOM'):  # Check for HETATM or ATOM records
                atom_label = line[12:16].strip()  # Extract atom label from the line
                x = float(line[30:38])  # Extract x-coordinate from the line
                y = float(line[38:46])  # Extract y-coordinate from the line
                color = float(line[60:66])  # Extract color information from the line

                # Append data to respective lists
                atoms.append(atom_label)
                x_coords.append(x)
                y_coords.append(y)
                colors.append(color)
    
    return atoms, x_coords, y_coords, colors

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

# Function to plot atom positions with lines and circles
def plot_atomsCircles(atoms, x_coords, y_coords, colors, threshold=1.5):
    plt.figure()  # Set up a new plot

    # Create line segments between closely positioned atoms, excluding certain atoms
    segments = []
    excluded_atoms = {'Co', 'Cu', 'Ni'} #Add atoms that you don't want to make bonds in the dictionnary
    for i in range(len(x_coords)):
        for j in range(i + 1, len(x_coords)):
            atom_i = atoms[i]
            atom_j = atoms[j]
            if atom_i not in excluded_atoms and atom_j not in excluded_atoms:
                dist = ((x_coords[i] - x_coords[j])**2 + (y_coords[i] - y_coords[j])**2)**0.5
                if dist < threshold:
                    segments.append([(x_coords[i], y_coords[i]), (x_coords[j], y_coords[j])])

    # Add line collection to the plot
    lc = LineCollection(segments, linewidths=2, colors='black', alpha=1.0)
    plt.gca().add_collection(lc)

    # Plot circles above atoms with specified colors
    v_min = min(colors)
    v_max = max(colors)
    abs_max = max([abs(v_min), abs(v_max)])
    plt.scatter(x_coords, y_coords, s=150, marker='o', c=colors, edgecolors=None, cmap='bwr', vmin=-abs_max, vmax=abs_max)

    labelAtoms = {'Co', 'Cu', 'Ni'} #Add atoms you want to be labeled in the dictionnary

    for i, atom in enumerate(atoms):
        if atom not in labelAtoms:
            continue
        else:
            plt.text(x_coords[i], y_coords[i] + 0.2, atom, ha='center', va='bottom', fontsize=16)

    # Set plot properties
    plt.axis('equal')
    plt.grid(False)
    cbar = plt.colorbar()
    cbar.set_label(label=r"$e^-$", size=15, weight='bold', rotation=0)
    cbar.ax.yaxis.set_label_coords(-1.5, 0.5)
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    plt.box(False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Visualize atom positions and properties.")
    parser.add_argument("label", help="Label for the input file")
    parser.add_argument("-m", "--muliken", action="store_true", help="Use Muliken population data (default: BADER)")
    parser.add_argument("-s", "--spin", action="store_true", help="Enable spin density mode (default : Charge transfer)")

    args = parser.parse_args()
    label = args.label

    if args.muliken:
        filename = f'{label}.xyz'
        atoms, x_coords, y_coords, colors = read_atom_positions(filename)
        plot_atomsCircles(atoms, x_coords, y_coords, colors, threshold=1.5)
        plt.savefig(f'{label}-SD.png', dpi=350)

    else:
        if args.spin:
            filename = f'{label}-SD.pdb'  # Replace this with your actual filename
            atoms, x_coords, y_coords, colors = read_atom_positions_pdb(filename)
            plot_atomsCircles(atoms, x_coords, y_coords, colors, threshold=1.5)
            plt.savefig(f'{label}-SD.png', dpi=350)
            print(f'Plotted {label}-SD.png')    
        else:     
            filename = f'{label}-CT.pdb'  # Replace this with your actual filename
            atoms, x_coords, y_coords, colors = read_atom_positions_pdb(filename)
            plot_atomsCircles(atoms, x_coords, y_coords, colors, threshold=1.5)
            plt.savefig(f'{label}-CT.png', dpi=350)
            print(f'Plotted {label}-CT.png')
        
    
    
