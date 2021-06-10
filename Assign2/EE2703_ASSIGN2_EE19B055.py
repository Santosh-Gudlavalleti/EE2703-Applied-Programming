"""
Assignment 1
Date:    3rd March 2021
Course:  Applied Programming Lab(EE2703)
Faculty: Prof. Harishankar Ramachandhran

Submission by: Santosh G(EE19B055)

To complie and execute: python3 EE2703_ASSIGN2_EE19B055.py <Input .netlist file>

PS: Few sources on online were referred, to get an understanding to solve the problem(including dependant sourecs)
"""

from sys import argv, exit
import cmath
import numpy as np
import pandas as pd

#Definitons of Various Component
CIRCUIT = ".circuit"
END = ".end"
RESISTOR = "R"
CAPACITOR = "C"
INDUCTOR = "L"
Independant_Voltage_Source = IVS = "V"
Ind_Current_Source = ICS =  "I"
VCVS = "E"
VCCS = "G"
CCVS = "H"
CCCS = "F"
PI = np.pi

#Creating various classes to deduce information based on the type of component
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
nodes = []
comp = { RESISTOR: [], CAPACITOR: [], INDUCTOR: [], IVS: [], ICS: [], VCVS: [], VCCS: [], CCVS: [], CCCS: [] }

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
                elif (line[:3] == '.ac'):
                    freq = float(line.split()[2])
                    w = 2*PI*freq                      
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

            
            else:
                data = lines[start+1:end]          # Analysis of circuit                     
                for line in ([line.split('#')[0].split('\n')[0] for line in data]):
                    det = line.split() 
                    if det[1] not in nodes:         #Finding total nodes to determine the size of matrices
                        nodes.append(det[1])
                    if det[2] not in nodes:
                        nodes.append(det[2])
                    
                    if det[0][0] == RESISTOR:       #Deducing data after finding the component type
                        comp[RESISTOR].append(resistor(det[0], det[1], det[2], det[3]))
                     
                    elif det[0][0] == CAPACITOR:
                        comp[CAPACITOR].append(resistor(det[0], det[1], det[2], det[3]))
                    
                    elif det[0][0] == INDUCTOR:
                        comp[INDUCTOR].append(resistor(det[0], det[1], det[2], det[3]))
                        
                    elif det[0][0] == IVS:
                        if len(det) == 5: # DC Source
                            comp[IVS].append(voltageSource(det[0], det[1], det[2], float(det[4])))
                    
                        elif len(det) == 6: # AC Source
                            if freq == 0:
                                sys.exit("Frequency of AC Source not specified!!")
                            comp[IVS].append(voltageSource(det[0], det[1], det[2], float(det[4])/2, det[5]))
                    
                    elif det[0][0] == ICS:
                        if len(det) == 5: # DC Source
                            comp[ICS].append(currentSource(det[0], det[1], det[2], float(det[4])))
                        elif len(det) == 6: # AC Source
                            if freq == 0:
                                sys.exit("Frequency of AC Source not specified!!")
                            comp[ICS].append(currentSource(det[0], det[1], det[2], float(det[4])/2, det[5]))
                        
                    elif det[0][0] == VCVS:
                        comp[VCVS].append(vcvs(det[0], det[1], det[2], det[3], det[4], det[5]))
                        
                    elif det[0][0] == VCCS:
                        comp[VCCS].append(vcvs(det[0], det[1], det[2], det[3], det[4], det[5]))
                   
                    elif det[0][0] == CCVS:
                        comp[CCVS].append(ccvs(det[0], det[1], det[2], det[3], det[4]))
                   
                    elif det[0][0] == CCCS:
                        comp[CCCS].append(cccs(det[0], det[1], det[2], det[3], det[4]))
                   
                    else:            #Error in Input of Components
                        sys.exit("Unexpected Components, Please Check\n")
                
                if('GND' in nodes):    
                    nodes.remove('GND')
                    nodes = ['GND'] + nodes
                else: 
                    print("Ground Node hasn't been mentioned, Please Check")
                    exit()
                
                nodecount = len(nodes)            #Total Number of Nodes
                nodeindex = {nodes[i]:i for i in range(nodecount)}  #Indexing each node, to ensure easier calculations without restricting the user to follow specific naming
                VScount = len(comp[IVS])+len(comp[VCVS])+len(comp[CCVS])
                
                A = np.zeros((nodecount + VScount, nodecount + VScount), complex)   #Defining Matrices
                B = np.zeros((nodecount + VScount), complex)
                A[0][0] = 1
                for r in comp[RESISTOR]:                #Making corresponding entries to matrices 
                    if r.node1 != 'GND':
                        A[nodeindex[r.node1]][nodeindex[r.node1]] += 1/r.value
                        A[nodeindex[r.node1]][nodeindex[r.node2]] -= 1/r.value
                    if r.node2 != 'GND':
                        A[nodeindex[r.node2]][nodeindex[r.node1]] -= 1/r.value
                        A[nodeindex[r.node2]][nodeindex[r.node2]] += 1/r.value
                    # Capacitor Equations
                for c in comp[CAPACITOR]:
                    if c.node1 != 'GND':
                        A[nodeindex[c.node1]][nodeindex[c.node1]] += complex(0, w*c.value)
                        A[nodeindex[c.node1]][nodeindex[c.node2]] -= complex(0, w*c.value)
                    if c.node2 != 'GND':
                        A[nodeindex[c.node2]][nodeindex[c.node1]] -= complex(0, w*c.value)
                        A[nodeindex[c.node2]][nodeindex[c.node2]] += complex(0, w*c.value)
                    # Inductor Equations
                for l in comp[INDUCTOR]:
                    if l.node1 != 'GND':
                        A[nodeindex[l.node1]][nodeindex[l.node1]] += complex(0, -1.0/(w*l.value))
                        A[nodeindex[l.node1]][nodeindex[l.node2]] -= complex(0, -1.0/(w*l.value))
                    if l.node2 != 'GND':
                        A[nodeindex[l.node2]][nodeindex[l.node1]] -= complex(0, -1.0/(w*l.value))
                        A[nodeindex[l.node2]][nodeindex[l.node2]] += complex(0, -1.0/(w*l.value))
                            
                    # Voltage Source Equations
                for i in range(len(comp[IVS])):
                        # Equation accounting for current through the source
                    if comp[IVS][i].node1 != 'GND':
                        A[nodeindex[comp[IVS][i].node1]][nodecount+i] = 1.0
                    if comp[IVS][i].node2 != 'GND':
                        A[nodeindex[comp[IVS][i].node2]][nodecount+i] = -1.0
                    # Auxiliary Equations
                    A[nodecount+i][nodeindex[comp[IVS][i].node1]] = -1.0
                    A[nodecount+i][nodeindex[comp[IVS][i].node2]] = +1.0
                    B[nodecount+i] = cmath.rect(comp[IVS][i].value, comp[IVS][i].phase*PI/180)
        
        
                    # Current Source Equations
                for i in comp[ICS]:
                    if i.node1 != 'GND':
                        B[nodeindex[i.node1]] = -1*i.value
                    if i.node2 != 'GND':
                        B[nodeindex[i.node2]] = i.value
                    
                    # VCVS Equations
                for i in range(len(comp[VCVS])):
                        # Equation accounting for current through the source
                    if comp[VCVS][i].node1 != 'GND':
                        A[nodeindex[comp[VCVS][i].node1]][nodecount+len(comp[IVS])+i] = 1.0
                    if comp[VCVS][i].node2 != 'GND':
                        A[nodeindex[comp[VCVS][i].node2]][nodecount+len(comp[IVS])+i] = -1.0
                    A[nodecount+len(comp[IVS])+i][nodeindex[comp[VCVS][i].node1]] = 1.0
                    A[nodecount+len(comp[IVS])+i][nodeindex[comp[VCVS][i].node2]] = -1.0
                    A[nodecount+len(comp[IVS])+i][nodeindex[comp[VCVS][i].node3]] = -1.0*comp[VCVS][i].value
                    A[nodecount+len(comp[IVS])+i][nodeindex[comp[VCVS][i].node4]] = 1.0*comp[VCVS][i].value
                    # CCVS Equations
                
                for i in range(len(comp[CCVS])):
                # Equation accounting for current through the source
                    if comp[VCVS][i].node1 != 'GND':
                        A[nodeindex[comp[CCVS][i].node1]][nodecount+len(comp[IVS])+len(comp[VCVS])+i] = 1.0
                    if comp[VCVS][i].node2 != 'GND':
                        A[nodeindex[comp[VCVS][i].node2]][nodecount+len(comp[IVS])+len(comp[VCVS])+i] = -1.0
                    A[nodecount+len(comp[IVS])+len(comp[VCVS])+i][nodeindex[comp[CCVS][i].node1]] = 1.0
                    A[nodecount+len(comp[IVS])+len(comp[VCVS])+i][nodeindex[comp[CCVS][i].node2]] = -1.0
                    A[nodecount+len(comp[IVS])+len(comp[VCVS])+i][nodecount+len(comp[IVS])+len(comp[VCVS])+i] = -1.0*comp[CCVS][i].value
                    
                    
                # VCCS Equations
                for vccs in comp[VCCS]:
                    if vccs.node1 != 'GND':
                        A[nodeindex[vccs.node1]][nodeindex[vccs.node4]]+=vccs.value
                        A[nodeindex[vccs.node1]][nodeindex[vccs.node3]]-=vccs.value
                    if vccs.node2 != 'GND':
                        A[nodeindex[vccs.node2]][nodeindex[vccs.node4]]-=vccs.value
                        A[nodeindex[vccs.node3]][nodeindex[vccs.node3]]+=vccs.value
                    # CCCS Equations
                for cccs in comp[CCCS]:
                    def getIndexIVS(vName):
                        for i in range(len(comp[IVS])):
                             if comp[IVS][i].name == vName:
                                 return i
                    if cccs.node1 != 'GND':
                        A[nodeindex[cccs.node1]][nodecount+getIndexIVS(cccs.vSource)]-=cccs.value
                    if cccs.node2 != 'GND':
                        A[nodeindex[cccs.node2]][nodecount+getIndexIVS(cccs.vSource)]+=cccs.value

                
                if(np.linalg.det(A) != 0):        #Making sure Matrix is Invertible 
                    
                    x = np.linalg.solve(A, B)     #Solving the two matrices to find the necessary solution
                    
                    for i in range(nodecount):                      #Printing the final Answers
                        print("Voltage at node %s is %s"%(nodes[i], x[i]))
                    
                    for i in range(len(comp[IVS])):
                        print("current through source %s is %s" %( comp[IVS][i].name , x[nodecount+i]))
                   
                    for i in range(len(comp[VCVS])):
                        print("current through soure %s is %s" %( comp[VCVS][i].name , x[nodecount+len(IVS)+i-1]))
                   
                    for i in range(len(comp[CCVS])):
                        print("current through source %s is %s" %( comp[CCVS][i].name , x[nodecount+len(IVS)+len(VCVS)+i]))                               
                    print("Tha above values are Amplitudes")
                    
                for line in ([' '.join((line.split('#')[0].split())) for line in (lines[0:start] + lines[end+1:l])]):
                    if line != "":           # Part 9 : Shows a warning, if extra text is present outside the circuit.
                        print("\nWarning: Extra Words, comments excluded, present outside the Circuit Definition.")
                        break    
            
    else: print("Incorrect file extension. Please Check.\n Expected: .netlist")
except IOError:
    print("File Doesn't exist")
    exit()

