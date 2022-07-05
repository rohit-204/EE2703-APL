#                                        EE2703 Applied Programming Lab
#     				                        Assignment 1:  Solution
#         			                         ROHIT KUMAR  EE20B110
#         				                      26th January 2022
#       INPUT   .netlist file
#       purpose       Identifies errors in SPICE program code, and displays the tokens in reverse order
 

from sys import argv, exit

#               checking for correct input

if len(argv) == 2 :	
	file_name = argv[1];
else:
	print("Number of arguments must be 2");
	exit(0);
try:
	f = open(file_name);
	total_line = f.readlines();
	f.close();
except:
	print("File not found");
	exit(0);

#             to determine start and end of function 	


startCircuit = '.circuit';
endCircuit = '.end';
start = -1;
end = -2;


#           the endline character is removed from each 'line'
#           tab spacesare converted to spaces

for current_line in total_line:

	location = total_line.index(current_line);
	current_line = current_line.replace('\n','');
	current_line = current_line.split('#')[0];
	current_line = current_line.replace('\t',' ');	
	current_line=current_line.strip();
	total_line[location] = current_line;

	if current_line[:len(startCircuit)] == startCircuit:
		start = location;
	elif current_line[:len(endCircuit)] == endCircuit:
		end = location;	

if start >= end:
	print("Circuit Block Invalid");
	exit(0);



str_token = [];

for current_line in total_line[start+1:end]:
	
	location = total_line.index(current_line);
	linelist = current_line.split(" ");
	linelist = [element for element in linelist if element != ""];

	if linelist == []:
		continue;
#   checked for whether it is a resistor, capacitor, inductor		
#	dependent and independent voltage and currect sources
 
 		
	if linelist[0][0] == 'R' or 'L' or 'C' or 'V' or 'I' :	
		if len(linelist) != 4:
			print("Incorrect Number of Parameters: Line ",location);
			exit(0);
		if linelist[1].isalnum() != True or linelist[2].isalnum() != True :
			print("Incorrect Node Designation - only alphanumeric variables: Line ",location);
			exit(0);
		
	elif linelist[0][0] ==  'E' or 'G':
		if len(linelist) != 6:
			print("Incorrect Number of Parameters: Line ",location);
			exit(0);
		if linelist[1].isalnum() != True or linelist[2].isalnum() != True or linelist[3].isalnum() != True or linelist[4].isalnum() != True:
			print("Incorrect Node Designation - only alphanumeric variables: Line ",location);
			exit(0);
	

	elif linelist[0][0] ==  'H' or 'F':
		if len(linelist) != 5:
			print("Incorrect Number of Parameters: Line ",location);
			exit(0);
		if linelist[1].isalnum() != True or linelist[2].isalnum() != True:
			print("Incorrect Node Designation - only alphanumeric variables: Line ",location);
			exit(0);
		if linelist[3][0] != 'V':
			print("Incorrect Voltage Label: Line ",location);
			exit(0);
	
	str_token.append(linelist);

#   printing tokens	
length = len(str_token);
for i in range(length-1,-1,-1):
	current_line = " ";
	for k in range(len(str_token[i])-1,-1,-1):
		print(str_token[i][k]," ",end="");
	print("\n");
	