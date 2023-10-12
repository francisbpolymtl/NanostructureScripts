#This scripts is used along with the bash script write_denchar to read the 'NumberOfSpecies' and the 'ChemicalSpeciesLabel' block from the 
#siesta fdf file and to write it in denchar_input.fdf

import sys

def read_SpeciesLabel(label):
    with open(f"{label}.fdf", 'r') as f:
        for no, line in enumerate(f):
            if 'NumberOfSpecies' in line:
                print(line, end="")
            if '%block ChemicalSpeciesLabel' in line:
                print(line, end="")
                break
        for no, line in enumerate(f):
            if '%endblock ChemicalSpeciesLabel' not in line:
                print(line, end="")
            else:
                print('%endblock ChemicalSpeciesLabel')
                break

if __name__ == '__main__':
    label = sys.argv[1]
    read_SpeciesLabel(label)
    