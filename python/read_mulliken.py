# Python script called by bash script plot_mulliken that reads milliken population from SIESTA .out output file and that adds the charge difference between 
# Spin up and down as the fourth column of an .xyz file, that can further be plotted in matplotlib.

import sys

# Function to see if a line starts with a integer. If so, thats atom index.
def str_to_int(line):
    try:
        int(line.strip().split()[0])
        return True
    except ValueError:
        return False

# Function that reads mulliken populations for spin up and down and that put the values in python dictionaries. It also computes, for each atom, the difference between charge up and charge down.
def read_mulliken():
    dic_up = {}
    dic_down = {}
    dic_mag = {}
    Q_up=0
    Q_down=0
    with open('arquivoup', 'r') as f_up:
        line = f_up.readline()
        while line:
            if line.strip():
                if str_to_int(line):
                    dic_up[int(line.strip().split()[0])] = float(line.strip().split()[1])
            line = f_up.readline()
    with open('arquivodown', 'r') as f_down:
        line = f_down.readline()
        while line:
            if line.strip():
                if str_to_int(line):
                    dic_down[int(line.strip().split()[0])] = float(line.strip().split()[1])
            line = f_down.readline()
        for atom, charge in dic_up.items():
            dic_mag[atom]=charge-dic_down[atom]
            Q_up+=charge
            Q_down+=dic_down[atom]
        print(f"Charge up is {Q_up} e.")
        print(f"Charge down is {Q_down} e.")
        print(f"Magnetic moment is {Q_up-Q_down} Bohr magnetons")
        return dic_mag

# Function that adds the magnetisation computed with read_mulliken() as the fourth column of an .xyz file
def mulliken2xyz(label):
    with open(f'{label}.xyz', 'r') as xyz:
        lines = xyz.readlines()
    with open(f'{label}-Mag.xyz', 'w') as xyz:
        atom_count = 0
        dic_mag=read_mulliken()
        for line in lines[2:]: 
            atom_count += 1
            atom_info = line.split()
            atom_symbol, x, y, z = atom_info[0], float(atom_info[1]), float(atom_info[2]), float(atom_info[3])
            spin = dic_mag[atom_count]
            pdb_line = f"{atom_symbol:4} {x:12.4f}{y:8.4f}{z:8.4f} {spin:8.6f}\n"
            xyz.write(pdb_line)
    print(f'{label}-Mag.xyz was written succesfully!')

if __name__ == "__main__":
    label =sys.argv[1]
    mulliken2xyz(label)
    