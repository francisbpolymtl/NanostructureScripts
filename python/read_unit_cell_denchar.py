# This script is used along with the bash script 'write_denchar' to read the lattice vectors from the SIESTA .XV output and
# to write it in denchar_input.fdf. This only works for systems with orthogonal unit cell.

import sys

def read_unit_cell(label, n_p):
    with open(f"{label}.XV") as f:
        lines=f.read().splitlines()
        print(f"Denchar.MaxX {round(float(lines[0].split()[0])*conv,4)} Ang \nDenchar.MaxY {round(float(lines[1].split()[1])*conv,4)} Ang \nDenchar.MaxZ {round(float(lines[2].split()[2])*conv,4)} Ang\n")
        print(f"Denchar.NumberPointsX {int(round(float(lines[0].split()[0])*conv,2)*n_p)} \nDenchar.NumberPointsY {int(round(float(lines[1].split()[1])*conv,2)*n_p)} \nDenchar.NumberPointsZ {int(round(float(lines[2].split()[2])*conv,2)*n_p)}")
    return
    
if __name__ == '__main__':
    conv = 0.52917721067121
    n_p=5
    if sys.argv[-1] != '0':
        n_p = float(sys.argv[-1])
    read_unit_cell(sys.argv[1], n_p)
        
