# This small scripts reads the label provided and returns the magnetic state if found in the label (FM, AFM, DIA)

import sys

def mag_state(label):
    state=label.split('-')
    if 'FM' in state:
        return print('FM')
    elif 'AFM' in state:
        return print('AFM')
    elif 'DIA' in state:
        return print('DIA')
    elif 'RELAX' in state:
        return print('DIA')
    else:
        return print('A problem has occured')

if __name__ == '__main__':   
    mag_state(sys.argv[1])