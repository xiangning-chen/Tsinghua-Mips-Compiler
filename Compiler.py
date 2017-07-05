#compiler python3 version
#written by Chen xiangning

R_Type_Funct = {'add':'100000','addu':'100001','sub':'100010','subu':'100011','and':'100100','or':'100101',
'xor':'100110','nor':'100111','slt':'10101','sll':'000000','srl':'000010','sra':'000011'}

I_Type_OpCode = {'lui':'001111','addi':'001000','addiu':'001001','andi':'001100','slti':'001010',
'sltiu':'001011','beq':'000100','bne':'000101','blez':'000110','bgtz':'000111','bgez':'000001',
'bltz':'000001','sw':'101011','lw':'100011'}

J_Type_OpCode = {'j':'000010','jal':'000011','jr':'001000','jalr':'001001'}

Register = {'$zero':'00000','$at':'00001','$v0':'00010','$v1':'00011','$a0':'00100','$a1':'00101',
'$a2':'00110','$a3':'00111','$t0':'01000','$t1':'01001','$t2':'01010','$t3':'01011','$t4':'01100',
'$t5':'01101','$t6':'01110','$t7':'01111','$s0':'10000','$s1':'10001','$s2':'10010','$s3':'10011',
'$s4':'10100','$s5':'10101','$s6':'10110','$s7':'10111','$t8':'11000','$t9':'11001','$k0':'11010',
'$k1':'11011','$gp':'11100','$sp':'11101','$fp':'11110','$ra':'11111'}

def Binary2Hex(x):						#32 bit Binary str to 8 bit Hex str
	return format(int(x[:4],2),'x') + format(int(x[4:8],2),'x') + format(int(x[8:12],2),'x') + format(int(x[12:16],2),'x') + format(int(x[16:20],2),'x') + format(int(x[20:24],2),'x') + format(int(x[24:28],2),'x') + format(int(x[28:32],2),'x')			

def Dec2Binary(x,n):					#Dec str transer to Binary str, include nagitive
	tem,mark = abs(int(x)),'0'
	if int(x) < 0:
		tem,mark = pow(2,n) - tem,'1'
	tem = format(tem,'b')
	for i in range(n - len(tem)):
		tem = mark + tem
	return tem

Data = []								#read data from input.txt, data saved in list Data
Label = {}								#deal with beq and jump
with open('/Users/peter_cxn/input.txt','r') as Input:
	read = Input.readlines()
	i = 0
	for temp in read:
		l = temp.split()
		if l[0][-1] == ':':
			Label[l[0][:len(l[0]) - 1]] = i
		l.insert(0,i)
		Data.append(l)
		i += 1

Code = []
for line in Data:
	#get the position of name
	if line[1][-1] == ':':
		name,flag = line[2],2
	else:
		name,flag = line[1],1

	if name in R_Type_Funct:			#deal with R_Type
		Op,rd = '000000',line[flag + 1].strip(',')
		if name == 'sll' or name == 'srl' or name == 'sra':
			rs,rt,shamt = '$zero',line[flag + 2].strip(','),line[flag + 3]
		else:
			rs,rt,shamt = line[flag + 2].strip(','),line[flag + 3].strip(','),'00000'
		Code.append(Binary2Hex(Op + Register[rs] + Register[rt] + Register[rd] + Dec2Binary(shamt,5) + R_Type_Funct[name]))

	elif name in I_Type_OpCode:			#deal with I_Type
		if name == 'lw' or name == 'sw':
			rt,temp = line[flag + 1].strip(','),line[flag + 2]
			imm,rs = temp[:len(temp) - 5],temp[len(temp) - 4:-1]
		elif name == 'lui':
			rs,rt,imm = '$zero',line[flag + 1].strip(','),line[flag + 2]
		elif name =='beq' or name == 'bne':
			rs,rt,temp = line[flag + 1].strip(','),line[flag + 2].strip(','),line[flag + 3]
			imm = str(Label[temp] - line[0] - 1)
		elif name == 'bgez' or name == 'bgtz' or name == 'blez' or name == 'bltz':
			rs,rt,temp = line[flag + 1].strip(','),'$zero',line[flag + 2]
			imm = str(Label[temp] - line[0] - 1)
			if name == 'bgez':
				rt = '$at'
		else:
			rt,rs,imm = line[flag + 1].strip(','),line[flag + 2].strip(','),line[flag + 3]
		Code.append(Binary2Hex(I_Type_OpCode[name] + Register[rs] + Register[rt] + Dec2Binary(imm,16))) 
		
	else:								#deal with J_Type
		if name == 'j' or name == 'jal':
			target = str(Label[line[flag + 1]]) 
			Code.append(Binary2Hex(J_Type_OpCode[name] + Dec2Binary(target,26)))
		elif name == 'jr':
			rs = line[flag + 1]
			Code.append(Binary2Hex('000000' + Register[rs] + '000000000000000' + J_Type_OpCode[name]))
		else:
			rs,rd = line[flag + 1].strip(','),line[flag + 2]
			Code.append(Binary2Hex('000000' + Register[rs] + '00000' + Register[rd] + '00000' + J_Type_OpCode[name]))

i = 0
with open('/Users/peter_cxn/output.txt','wt') as Output:	#Data output, saved in output.txt
	for line in Code:
		print(str(i).ljust(3),':','0x',line,file = Output)
		i += 1



