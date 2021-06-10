"""
Assignment 1
Date:    17th Feb 2021
Course:  Applied Programming Lab(EE2703)
Faculty: Prof. Harishankar Ramachandhran

Submission by: Santosh G(EE19B055)

To complie and execute: python3 EE2703_ASSIGN1-EE19B055.py <Input .netlist file>
"""
"""
Pseudo Code: 
Firstly, the number of input arguments are verified followed by the verification of the extension of input file as in Part 1,2
The actual circuit is found out using the positions of ".circuit" and ".end".
Sanity checks are performed to ensure single presence etc.
The lines are then printed appropriately after removing comments etc.
"""

from sys import argv, exit

#import sys
import cmath
import numpy as np
import pandas as pd

#Definitons
START = ".circuit"
END = ".end"
RESISTOR = "R"
CAPACITOR = "C"
INDUCTOR = "L"
Independant Voltage Source = "V"
Ind. Current Source = "I"
VCVS = "E"
VCCS = "G"
CCVS = "H"
CCCS = "F"
PI = np.pi

# Classes for each circuit component
class resistor:
    def __init__(self, name, n1, n2, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2

class inductor:
    def __init__(self, name, n1, n2, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2

class capacitor:
    def __init__(self, name, n1, n2, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2

class voltageSource:
    def __init__(self, name, n1, n2, val, phase=0):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)        
        self.node1 = n1
        self.node2 = n2
        self.phase = float(phase)

class currentSource:
    def __init__(self, name, n1, n2, val, phase=0):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2
        self.phase = float(phase)

class vcvs:
    def __init__(self, name, n1, n2, n3, n4, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2
        self.node3 = n3
        self.node4 = n4

class vccs:
    def __init__(self, name, n1, n2, n3, n4, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2
        self.node3 = n3
        self.node4 = n4

class ccvs:
    def __init__(self, name, n1, n2, vName, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2
        self.vSource = vName

class cccs:
    def __init__(self, name, n1, n2, vName, val):
        self.name = name
        if 'e' in str(val):
            self.value=float(val.split('e')[0])*(10**int(val.split('e')[1]))
        else:
            self.value=float(val)   
        self.node1 = n1
        self.node2 = n2
        self.vSource = vName

if len(argv) != 2:                       #Part-1 : Verification of Inputs
    print('Please Execute as following:\npython3 %s <inputfile>' % argv[0])
    exit()

sc = start_count = 0
ec = end_count = 0
lines = l = 0
freq = 0
w = 0

try:
    if argv[1].endswith('.netlist'):      #Part 2 : Verification of Input File
        with open(argv[1]) as f:          #Part 3 : Opening and reading of File
            lines = f.readlines()
            start = -1; end = -1
            for line in ([' '.join((line.split('#')[0].split())) for line in (lines)]):    #Part 4 : Finding the actual circuit part
                if CIRCUIT == line[0:8]:
                    start = l
                    sc = sc + 1 
                elif END == line[0:len(END)]:
                    end = l
                    ec = ec + 1
                elif (line[:3] == '.ac' | line[:3] == '.Ac' | line[:3] == '.AC'):
                    freq = float(line.split()[2])
                    w = 2*PI*circuitfreq                      
                l = l + 1
                
            for line in ([' '.join((lines[start].split('#')[0].split()))]):     #Part 5 : Making sure there is no extra text in the start of Circuit
                if(len(line) > 9):
                    print("Please check the '.circuit' line, unexpectd text found after .circuit ")
                    exit(0)
               
            if(sc != 1):                                         # Part 6 : Makin sure the ".commands" are present only once 
                print("Appearance of .circuit is expected only once")
            elif(ec != 1):
                print("Appearance of .end is expected only once")
                        
            elif start >= end:                # Part 7 : Verifying if .circuit preceeds .end
                print('Invalid circuit definition: .end preceeds .circuit')
                exit(0)

            else:                             # Part 8 : Removing Comments and reverse printing the lines that are part of the circuit. 
                for line in reversed([' '.join(reversed(line.split('#')[0].split())) for line in lines[start+1:end]]):

                 
    else: print("Incorrect file extension. Please Check.\n Expected: .netlist")

except IOError:
    print("File Doesn't exist")
    exit()

