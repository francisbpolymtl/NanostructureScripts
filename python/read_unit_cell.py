# Python script called by the bash script simAFM to extract the lattice vector of the system from the .XV file found in the directory

import sys

def read_unit_cell(label):
    with open(f"{label}.XV") as f:
        lines=f.read().splitlines()
        for i in range(3):
            print(f"{round(float(lines[i].split()[0])*conv,4)}   {round(float(lines[i].split()[1])*conv,4)}   {round(float(lines[i].split()[2])*conv,4)}")
        print("Y")
        print(f"{int(round(float(lines[0].split()[0])*conv,2)*10)}   {int(round(float(lines[1].split()[1])*conv,2)*10)}   {int(round(float(lines[2].split()[2])*conv,2)*10)}")
    return

if __name__ == "__main__":
    conv = 0.52917721067121
    read_unit_cell(sys.argv[1])