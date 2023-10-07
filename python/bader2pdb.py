import sys
import argparse

#please verify the value, some corrections might be needed for some elements
valence_electron = {
    "H": 1,  "He": 2, "Li": 1, "Be": 2, "B": 3,  "C": 4,  "N": 5,  "O": 6,  "F": 7,  "Ne": 8,
    "Na": 1, "Mg": 2, "Al": 3, "Si": 4, "P": 5,  "S": 6,  "Cl": 7, "Ar": 8,
    "K": 1,  "Ca": 2, "Sc": 3, "Ti": 4, "V": 5,  "Cr": 6,  "Mn": 7, "Fe": 8, "Ni": 10, "Co": 9, "Cu": 11, "Zn": 12, "Ga": 13, "Ge": 14, "As": 15, "Se": 16, "Br": 17, "Kr": 18,
    "Rb": 1, "Sr": 2, "Y": 3, "Zr": 4, "Nb": 5, "Mo": 6, "Tc": 7, "Ru": 8, "Rh": 9, "Pd": 10, "Ag": 11, "Cd": 12, "In": 13, "Sn": 14, "Sb": 15, "Te": 16, "I": 17, "Xe": 18,
    "Cs": 1, "Ba": 2, "La": 3, "Hf": 4, "Ta": 5, "W": 6, "Re": 7, "Os": 8, "Ir": 9, "Pt": 10, "Au": 11, "Hg": 12, "Tl": 13, "Pb": 14, "Bi": 15, "Th": 3, "Pa": 4, "U": 3, "Np": 4, "Pu": 4, "Am": 5, "Cm": 6, "Bk": 7, "Cf": 6, "Es": 6, "Fm": 7, "Md": 8, "No": 8, "Lr": 8,
    "Ac": 3, "Ce": 3, "Pr": 3, "Nd": 3, "Pm": 3, "Sm": 3, "Eu": 3, "Gd": 3, "Tb": 3, "Dy": 3, "Ho": 3, "Er": 3, "Tm": 3, "Yb": 3, "Lu": 3,
    "Th": 4, "Pa": 5, "U": 6, "Np": 6, "Pu": 6, "Am": 6, "Cm": 6, "Bk": 6, "Cf": 6, "Es": 6, "Fm": 6, "Md": 6, "No": 6, "Lr": 6
}



# Function to read atom charges from ACF.dat file
def read_charges_from_acf(acf_file):
    charges = {}
    with open(acf_file, 'r') as acf:
        lines = acf.readlines()
    # Loop through lines and extract atom charges
    for line in lines:
        if line.startswith('    #') or line.startswith(' -') or line.startswith('    VAC') or line.startswith('    NUM'):
            continue  # Skip header lines
        if line.strip() == '':
            continue  # Skip empty lines
        atom_info = line.split()
        atom_index, charge = int(atom_info[0]), float(atom_info[4])
        #Store values in dictionnary
        charges[atom_index] = charge

    return charges


#Function to write data in a pdb file
def xyz_to_pdb(label):
    #Read data from xyz
    with open(f'{label}.xyz', 'r') as xyz:
        lines = xyz.readlines()
    #Read data from ACF
    atom_charges = read_charges_from_acf(f'{label}-ACF.dat') #Labels created with the automatic bader analysis change to your ACF.dat labels

    with open(f'{label}.pdb', 'w') as pdb:
        atom_count = 0
        for line in lines[2:]:  # Skip the first two lines containing the number of atoms and a comment
            atom_count += 1 #keep count of the atom number
            atom_info = line.split()
            atom_symbol, x, y, z = atom_info[0], float(atom_info[1]), float(atom_info[2]), float(atom_info[3]) #Get data from xyz

            #Calculation of charge transfer            
            charge = valence_electron[atom_symbol]-atom_charges[atom_count]
            
            #Write lines in pdb to be utilized in VMD
            if charge >= 0 :
                pdb_line = f"ATOM  {atom_count:>5} {atom_symbol:<4} MOL     1    {x:>8.3f}{y:>8.3f}{z:>8.3f}  {charge:>6.2f}\n"
            else :
                pdb_line = f"ATOM  {atom_count:>5} {atom_symbol:<4} MOL     1    {x:>8.3f}{y:>8.3f}{z:>8.3f}  {charge:>6.2f}\n"
            pdb.write(pdb_line)
        pdb.write("END\n")
    print("Conversion completed successfully.")


#Same script that takes into account calculation with spin polarization (very small changes)
#The way the charge transfer is calculated is Charge transfer = Valence electrons - (Charge Up + Charge Down)
def xyz_to_pdb_spin(label):
    with open(f'{label}.xyz', 'r') as xyz:
        lines = xyz.readlines()
    atom_charges_up = read_charges_from_acf(f'{label}-UP-ACF.dat') #Labels created with the automatic bader analysis change to your ACF.dat labels
    atom_charges_down = read_charges_from_acf(f'{label}-DN-ACF.dat') #Labels created with the automatic bader analysis change to your ACF.dat labels
    with open(f'{label}-CT.pdb', 'w') as pdb:
        atom_count = 0
        for line in lines[2:]:  # Skip the first two lines containing the number of atoms and a comment
            atom_count += 1
            atom_info = line.split()
            atom_symbol, x, y, z = atom_info[0], float(atom_info[1]), float(atom_info[2]), float(atom_info[3])

            #Calculation of charge transfer
            charge = valence_electron[atom_symbol]-atom_charges_up[atom_count]-atom_charges_down[atom_count]
            
            if charge >= 0 :
                pdb_line = f"HETATM{atom_count:5} {atom_symbol:4} MOL   1 {x:12.3f}{y:8.3f}{z:8.3f}  1.00 {charge:8.6f}         {atom_symbol}\n"
            else :
                pdb_line = f"HETATM{atom_count:5} {atom_symbol:4} MOL   1 {x:12.3f}{y:8.3f}{z:8.3f}  1.00 {charge:8.6f}        {atom_symbol}\n"
            pdb.write(pdb_line)

        pdb.write("END\n")
    print("Conversion completed successfully.")

if __name__ == "__main__":
    #Arguments
    parser = argparse.ArgumentParser(description="Convert XYZ files to PDB format.")
    parser.add_argument("label", help="Label for the input XYZ and ACF files")
    parser.add_argument("-s", "--spin", action="store_true", help="Enable spin polarized mode")

    args = parser.parse_args()

    if args.spin:
        xyz_to_pdb_spin(args.label)
    else:
        xyz_to_pdb(args.label)
    
