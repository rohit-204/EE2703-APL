#     Rohit Kumar
#     ee20b110

import numpy as np
from sys import argv, exit


CIRCUIT = ".circuit"
END = ".end"
AC = '.ac'

#    decleare   class for the element

class def_elem(): 

    def __init__(self,line):
        self.line = line
        self.tokens = self.line.split()
        self.name = type_of_element(self.tokens[0])
        self.from_node = self.tokens[1]
        self.to_node = self.tokens[2]


        if len(self.tokens) == 5:
            self.type = 'dc'
            self.value = float(self.tokens[4])



        elif len(self.tokens) == 6:
            self.type = 'ac'
            Vm = float(self.tokens[4])/2
            phase = float(self.tokens[5])
            real = Vm * np.cos(phase)
            imag = Vm * np.sin(phase)
            self.value = complex(real,imag)

        else:
            self.type = 'dc-only'
            self.value = float(self.tokens[3])

#  to take element name
def type_of_element(token):  
#does not support dependent sources yet
    code_to_element = {"R": "resistor", "L": "inductor", "C": "capacitor", "V": "ind voltage source", "I": "ind current source" }
    return code_to_element.get(token[0], None)

#     taking key values

def get_key(d,value): 
    for key in d.keys():
        if d[key] == value :
            return key

# to get frequency

def freq(lines): 
    w = 0
    for line in lines:
        if line[:3] == '.ac':
            w = float(line.split()[2])
    return w


def node_mapping(circuit): #Returns a dictionary of nodes from the circuit definition.
    d = {"GND" : 0} 
    nodes = [def_elem(line).from_node for line in circuit]
    nodes += [def_elem(line).to_node for line in circuit]
    nodes = list(set(nodes)) #all distinct nodes

    #  To print nodes
    cnt = 1
    for node in nodes:
        if node != 'GND' :
            d[node] = cnt
            cnt += 1
    return d

#  creates dictionary for each component
def build_dict(circuit,e): 
    d = {}
    ele_names = [def_elem(line).tokens[0] for line in circuit if def_elem(line).tokens[0][0].lower()== e]
    for i, name in enumerate(ele_names):
        d[name] = i
    return d

#store the lines and position of the given node

def find_node(circuit, node_key, node_map):  
    indx = []
    for i in range(len(circuit)):
        for j in range(len(circuit[i].split())):
            if circuit[i].split()[j] in node_map.keys():
                if node_map[circuit[i].split()[j]] == node_key:
                    indx.append((i, j))

    return indx

#   fill the M and b matrix for the given node

def upd_matrix(node_key): 
    indx = find_node(circuit, node_key, node_map)
    for ind in indx:
        #getting all the attributes of the element using the class definition
        element = def_elem(circuit[ind[0]])
        ele_name = circuit[ind[0]].split()[0]
        #resistors
        if ele_name[0] == 'R':
            if ind[1] == 1: #from_node
                neig_key = node_map[element.to_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, neig_key] -= 1/(element.value)
                    
            if ind[1] == 2 : #to_node
                neig_key = node_map[element.from_node]
                M[node_key, node_key] += 1/(element.value)
                M[node_key, neig_key] -= 1/(element.value)      
        #inductors
        if ele_name[0] == 'L' :
            try:
                if ind[1]== 1:
                    neig_key = node_map[element.to_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * w * element.value))
                    M[node_key, neig_key] += complex(0,1/(2 * np.pi * w * element.value))

                if ind[1] == 2 :
                    neig_key = node_map[element.from_node]
                    M[node_key, node_key] -= complex(0,1/(2 * np.pi * w * element.value))
                    M[node_key, neig_key] += complex(0,1/(2 * np.pi * w * element.value))


            except ZeroDivisionError: #in dc case as w = 0, handle it separately


                idx = ind_d[ele_name]
                if ind[1]== 1:
                    neig_key = node_map[element.to_node]
                    M[node_key, n + k + idx] += 1 
                    M[n + k + idx, node_key] -= 1
                    b[n + k + idx] = 0

                if ind[1]== 2:
                    M[node_key, n + k + idx] -= 1
                    M[n + k + idx, node_key] += 1
                    b[n + k + idx] = 0
        
        #independent voltage source
        if ele_name[0] == 'V' :
            index = volt_d[ele_name]

            if ind[1]== 1:
                neig_key = node_map[element.to_node]
                M[node_key,n+index] += 1
                M[n+index,node_key] -= 1
                b[n+index] = element.value

            if ind[1] == 2 :
                neig_key = node_map[element.from_node]
                M[node_key,n+index] -= 1
                M[n+index,node_key] +=1
                b[n+index] = element.value
        #independent current source
        if ele_name[0] == 'I' :
            if ind[1]== 1:
                b[node_key] -= element.value
            if ind[1] == 2 :
                b[node_key] += element.value

        #capacitors
        if ele_name[0] == 'C' :
            if ind[1]== 1: #from_node
                neig_key = node_map[element.to_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * w * (element.value))
                M[node_key, neig_key] -= complex(0, 2 * np.pi * w * (element.value))

            if ind[1] == 2 :#to_node
                neig_key = node_map[element.from_node]
                M[node_key, node_key] += complex(0, 2 * np.pi * w * (element.value))
                M[node_key, neig_key] -= complex(0, 2 * np.pi * w * (element.value))        
    
#accept the name of netlist file as commandline
#check if the user has actually provided the 		
#filename or not and give appropriate error
#message if needed.
if len(argv) != 2:
    print('\nUsage: %s <inputfile>' % argv[0]) 
    exit()
try:
    with open(argv[1]) as f:
        lines = f.readlines()
        #frequency of the source
        w = freq(lines)  
        start = -1
        end = -2
        for line in lines:              # extracting circuit definition start and end lines
            if CIRCUIT == line[:len(CIRCUIT)]:
                start = lines.index(line)
            elif END == line[:len(END)]:
                end = lines.index(line)
                break
        if start >= end:                # validating circuit block
            print('Invalid circuit definition')
            exit(0)

        
        circuit = []
        for line in [' '.join(line.split('#')[0].split()) for line in lines[start+1:end]]:
            circuit.append(line)                
        #1. preprocessing of the file done

        node_map = node_mapping(circuit)
        #2. table of distinct nodes present in the circuit
        #numbers assigned to the nodes correspond to the rows of the incidence matirx


        volt_d = build_dict(circuit, "v")
        ind_d = build_dict(circuit,'l')
        
        k = len([i for i in range(len(circuit)) if circuit[i].split()[0][0] == 'V'])
        n = len(node_map)
        dim = n + k   
        #dimension of M if source is AC.
        #if source is DC, we need to add inductors also
        # for dc signal, l acts as closed wire in steady state.
        if w == 0: 
            M = np.zeros((dim+len(ind_d),dim+len(ind_d)),dtype=np.complex)
            b = np.zeros(dim+len(ind_d),dtype=np.complex)
        else:
            M = np.zeros((dim,dim),dtype=np.complex)
            b = np.zeros(dim,dtype=np.complex)

        for i in range(len(node_map)): #update matrix for the ith node
            upd_matrix(i)
            
        #as Vgnd = 0
        M[0] = 0
        M[0,0] =1

        #  M and b arrays are constructed
        print('The node dictionary is :',node_map)
        print('M = :\n',M)
        print('b = :\n',b)


        #solve the matrix Mx = b
        try:
            x = np.linalg.solve(M,b)    
        except Exception:
            print('matrix is singular.')
            sys.exit()

        print('Voltage convention -> From node is at a lower potential')     
        
        for i in range(n):
            print("Voltage at node {} is {}".format(get_key(node_map,i),x[i]))

        for j in range(k):
            print('Current through source {} is {}'.format(get_key(volt_d,j),x[n+j]))

        if w == 0:
            for i in range(len(ind_d)):
                print("Current through inductor {} is {}".format(get_key(ind_d,i),x[n+k+i]))


except IOError:
    print('Invalid file')
    exit()