import sys


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
def xyz_to_pdb_spin(label):
    #Read data from xyz    
    with open(f'{label}.xyz', 'r') as xyz:
        lines = xyz.readlines()
    #Read data from ACF
    atom_charges_up = read_charges_from_acf(f'{label}-UP-ACF.dat')
    atom_charges_down = read_charges_from_acf(f'{label}-DN-ACF.dat')
    
    with open(f'{label}-SD.pdb', 'w') as pdb:
        atom_count = 0
        for line in lines[2:]:  # Skip the first two lines containing the number of atoms and a comment
            atom_count += 1
            atom_info = line.split()
            atom_symbol, x, y, z = atom_info[0], float(atom_info[1]), float(atom_info[2]), float(atom_info[3])

            #Calculation of spin density
            charge = atom_charges_up[atom_count]-atom_charges_down[atom_count]

            #Write lines in pdb to be utilized in VMD
            if charge >= 0 :
                pdb_line = f"HETATM{atom_count:5} {atom_symbol:4} MOL   1 {x:12.3f}{y:8.3f}{z:8.3f}  1.00 {charge:8.6f}         {atom_symbol}\n"
            else :
                pdb_line = f"HETATM{atom_count:5} {atom_symbol:4} MOL   1 {x:12.3f}{y:8.3f}{z:8.3f}  1.00 {charge:8.6f}        {atom_symbol}\n"
            pdb.write(pdb_line)

        pdb.write("END\n")
    print("Conversion completed successfully.")

if __name__ == "__main__":
    label =sys.argv[1]
    xyz_to_pdb_spin(label)
    
