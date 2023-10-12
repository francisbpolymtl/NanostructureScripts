# This script is used by the bash script PDOS-Gen to read the species label from SIESTA .fdf input file

import sys

def get_labels(SystemLabel):
    with open(f"{SystemLabel}.fdf", 'r') as f:
        start=False
        List_label=""
        for line in f:
            if '%block ChemicalSpeciesLabel' in line:
                start=True
                continue
            if start == True:
                if "%endblock ChemicalSpeciesLabel" not in line:
                    List_label = List_label + f"{line.split()[-1]} "
                else:
                    print(List_label.rstrip())
                    return
            

if __name__ == "__main__":
    get_labels(sys.argv[1])