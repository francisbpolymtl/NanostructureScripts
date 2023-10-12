# This scripts can be called to extract Fermi level from the .OUT file from SIESTA

import sys

def find_fermi(label):
    with open(f'{label}.out', 'r') as file:
        for l_no, line in enumerate(file):
            if 'siesta:         Fermi =' in line:
                L_f = line
                break
    F_L = L_f.split()[-1]
    return float(F_L)

if __name__ == "__main__":
    find_fermi(sys.argv[1])

