import sys
import string


labelcnt = 0
outlines = []

def nxtlabel():
# return string
	global labelcnt
	l = "label" + str(labelcnt)
	labelcnt +=1
	return l


def clearline(l):
	while l[0] == " " or l[0] =="\t":
		l = l[1:]

	#if l[0] == "#":
	#	return ""

	while l[-1] == " " or l[-1] == "\t" or l[-1] =="\n":
		l = l[:-1]
		if l=="":
			break

	return l

def clearlines(lines):
	o = []
	for i in range(len(lines)):
		l = clearline(lines[i])
		if l != "":
			o.append(l)
	return o


def interpr(lines):
	
	i = -1

	while i < len(lines) -1:
		
		i += 1
		l = lines[i]

		print ("processing line: " + l)
		
		if l[0] == "#":
			outlines.append("--" + l[1:])
			continue
		
		if l[:2]=="if":

			iflab = nxtlabel()
			elselab = nxtlabel()
			filab = nxtlabel()

			outlines.append(
				interprCondition(l, iflab, elselab))
			
			elseline = None
			filine = None

			j = i
			stack = 0

			while True:
				j += 1
				l = lines[j]
				
				if l[:2] == "if":
					stack -= 1
					continue

				if stack != 0 and l[:2] == "fi":
					stack += 1
					continue
				
				if stack == 0 and l[:4] == "else":
					elseline = j
					continue

				if stack == 0 and l[:2] == "fi":
					if elseline == None:
						print ("SYNTAX ERROR: NO ELSE BLOCK FOUND")
						sys.exit()
					filine = j
					break

				
			# end while
			
			interpr(lines[i+1:elseline])

			outlines.append("\tJUMP " + filab)
			outlines.append(elselab + ":")

			interpr(lines[elseline +1 : filine])

			outlines.append(filab + ":")

			i = filine


			continue



				
		if l[:4]=="loop":
			labbegin = nxtlabel()
			outlines.append(labbegin+":")

			j = i+1
			stack = 0
			while (stack != 0 or
				(lines[j][:5] != "endif" and lines[j][:6] != "repeat")):
				if lines[j][:4] == "loop":
					stack -= 1
				if lines[j][:5] == "endif" or lines[j][:6] == "repeat":
					stack += 1
				j += 1
			
			interpr(lines[i+1:j])
			if lines[j][:5] == "endif":
				labexit = nxtlabel()
				outlines.append(
					interprCondition(lines[j], labexit, labbegin))
			elif lines[j][:6] == "repeat":
				outlines.append("\tJUMP " + labbegin)
			i = j
			continue

		if l[:4]=="incr":
			outlines.append("\tBUMPUP " + l[4:])
			continue

		if l[:4]=="decr":
			outlines.append("\tBUMPDN " + l[4:])
			continue

		if l[:4]=="pull":
			outlines.append("\tCOPYFROM " + l[4:])
			continue
		
		if l[:4]=="push":
			outlines.append("\tCOPYTO " + l[4:])
			continue

		if l[:4]=="read":
			
			outlines.append("\tINBOX")

			parts = l.split()
			if len(parts) == 3 and parts[1] == "->":
				outlines.append("\tCOPYTO " + parts[2])
			continue
		
		if l[:3]=="out":
			
			parts = l.split()
			if len(parts) == 3 and parts[1] == "<-":
				outlines.append("\tCOPYFROM " + parts[2])

			outlines.append("\tOUTBOX")
			continue

		if l[0] in string.digits:
			outlines.append(interprCalc(l))
			continue
		
		if l[0] == "*":
			x = l.find(" ")
			mult = int(l[1:x])
			repeater = [l[x+1:]]
			for x in range(mult):
				interpr(repeater)
			continue

		print("SYNTAX ERROR: UNNKOWN COMMAND")
		print(l)
		sys.exit()

def interprCalc(line, cache=None):
	parts = line.split()
	
	l = ""

	if parts[1] != "=":
		print("SYNTAX ERROR, '=' EXPECTED")
	
	l += "\tCOPYFROM " + parts[2] + "\n"

	if parts[3] == "+":
		l += "\tADD " + parts[4] + "\n"
		l += "\tCOPYTO " + parts[0]
	
	elif parts[3] == "-":
		l += "\tSUB " + parts[4] + "\n"
		l += "\tCOPYTO " + parts[0]

	elif parts[3] == "*":

		if len(parts) < 7 and parts[5] != "|":
			print "SYNTAX ERROR, NO CACHE GIVEN"

		cache = parts[6]
		countlab = nxtlabel()
		exitlab = nxtlabel()
		if cache==None:
			print("SYNTAX ERROR, NO CACHE CELL GIVEN")
		l += "\tCOPYTO " + parts[0] + "\n"
		l += "\tCOPYFROM " + parts[4] + "\n"
		l += "\tCOPYTO " + cache + "\n"
		l += countlab + ":\n"
		l += "\tBUMPDN " + cache + "\n"
		l += "\tJUMPZ " + exitlab + "\n"
		l += "\tCOPYFROM " + parts[2] + "\n"
		l += "\tADD " + parts [0] + "\n"
		l += "\tCOPYTO " + parts[0] + "\n"
		l += "\tJUMP " + countlab +"\n"
		l += exitlab + ":"
		
	return l

def interprCondition(cond, labTrue, labFalse):
	#return string
	
	l = ""
	parts = cond.split()[1:]
	if parts[1] == "=":

		l += "\tCOPYFROM " + parts[0] + "\n"
		l += "\tSUB " + parts[2] + "\n"
		l += "\tJUMPZ " + labTrue + "\n"
		l += "\tJUMP " + labFalse + "\n"
		l += labTrue + ":"
	
	elif parts[1] == "<":
		
		l += "\tCOPYFROM " + parts[0] + "\n"
		l += "\tSUB " + parts[2] + "\n"
		l += "\tJUMPN " + labTrue + "\n"
		l += "\tJUMP " + labFalse + "\n"
		l += labTrue + ":"
	
	elif parts[1] == ">":

		l += "\tCOPYFROM " + parts[2] + "\n"
		l += "\tSUB " + parts[0] + "\n"
		l += "\tJUMPN " + labTrue + "\n"
		l += "\tJUMP " + labFalse + "\n"
		l += labTrue + ":"

	return l


filename = sys.argv[1]

f = open(filename)
lines = f.readlines()
f.close()

lines = clearlines(lines)
interpr(lines)

f = open("out.hrmc", "w")
for l in outlines:
	f.write(l + "\n")
f.close()

