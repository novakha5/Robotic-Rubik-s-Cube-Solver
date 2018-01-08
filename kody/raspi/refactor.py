def refactor(order):

	#controls if it is save to do next move or if it is needed to do some preperations (gives such preparations)
	def controlTurn(use_motor):
		tmp = ""
		if(use_motor == 'A' or use_motor == 'B'):
			if(!F_holds_cube):
				if(!C_is_vertical):
					tmp += "C "
					C_is_vertical = !C_is_vertical
 				if(!D_is_vertical):
					tmp += "D "
					D_is_vertical = !D_is_vertical
				tmp += "f "
				F_holds_cube = !F_holds_cube
			else:
				if(!C_is_vertical or D_is_vertical):
					if(!E_holds_cube):
						tmp += "e "
						E_holds_cube = !E_holds_cube
					tmp += "F "
					F_holds_cube = !F_holds_cube
					if(!C_is_vertical):
						tmp += "C "
						C_is_vertical = !C_is_vertical
					if(!D_is_vertical):
						tmp += "D "
						D_is_vertical = !D_is_vertical
					tmp += "f "
					F_holds_cube = !F_holds_cube
			if(!E_holds_cube):
				tmp += "e "
				E_holds_cube = !E_holds_cube
						
		elif(use_motor == 'C' or use_motor == 'D'):
			if(!E_holds_cube):
				if(!A_is_vertical):
					tmp += "A "
					A_is_vertical = !A_is_vertical
 				if(!B_is_vertical):
					tmp += "B "
					B_is_vertical = !B_is_vertical
				tmp += "e "
				E_holds_cube = !E_holds_cube
			else:
				if(!A_is_vertical or B_is_vertical):
					if(!F_holds_cube):
						tmp += "f "
						F_holds_cube = !F_holds_cube
					tmp += "E "
					if(!A_is_vertical):
						tmp += "A "
						A_is_vertical = !A_is_vertical
					if(!B_is_vertical):
						tmp += "B "
						B_is_vertical = !B_is_vertical
					tmp += "e "
					E_holds_cube = !E_holds_cube
			if(!F_holds_cube):
				tmp += "f "
				F_holds_cube = !F_holds_cube
		
		return tmp

	#check if it is save to rotate the cube
	def controlRotate():
		tmp = ""
		if(!F_holds_cube):
			if(!C_is_vertical):
				tmp += "C "
				C_is_vertical = !C_is_vertical
			if(!D_is_vertical):
				tmp += "D "
				D_is_vertical = !D_is_vertical
			tmp += "f "
			F_holds_cube = !F_holds_cube
		if(E_holds_cube):
			tmp += "E "
			E_holds_cube = !E_holds_cube
		return tmp

	commands = ""
	tmpCom = ""
	tmpChange = ""
	A_is_vertical = True	
	B_is_vertical = True
	C_is_vertical = True
	D_is_vertical = True
	E_holds_cube = True
	F_holds_cube = True
	
	#takes given string and creates one for use in stm
	for i in range(len(order)):
		tmp = order[i]
		if(tmp == 'R'):
			tmpCom += controlTurn('C')
			tmpCom += "C"	
			C_is_vertical = !C_is_vertical
		elif(tmp == 'L'):
			tmpCom += controlTurn('D')
			tmpCom += "D"	
			D_is_vertical = !D_is_vertical
		elif(tmp == 'F'):
			tmpCom += controlTurn('A')
			tmpCom += "A"
			A_is_vertical = !A_is_vertical
		elif(tmp == 'B'):
			tmpCom += controlTurn('B')
			tmpCom += "B"
			B_is_vertical = !B_is_vertical
		elif(tmp == 'U' or tmp == 'D'):
			tmpChange += controlRotate()
			tmpChange += "E cD e "
			D_is_vertical = !D_is_vertical
			C_is_vertical = !C_is_vertical
			if(tmp == 'U'):
				tmpCom += controlTurn('A')
				tmpCom += "A"
				A_is_vertical = !A_is_vertical
			else:
				tmpCom += controlTurn('B')
				tmpCom += "B"
				B_is_vertical = !B_is_vertical
		elif(tmp == '2'):
			tmpCom += "2"
			if(tmpCom[len(tmpCom)-1] == "A"):
				A_is_vertical = !A_is_vertical		
				if(tmpCom[len(tmpCom)-2] == "B"):
 					B_is_vertical = !B_is_vertical

			elif(tmpCom[len(tmpCom)-1] == "B"):
				B_is_vertical = !B_is_vertical

			elif(tmpCom[len(tmpCom)-1] == "C"):
				C_is_vertical = !C_is_vertical
				if(tmpCom[len(tmpCom)-2] == "D"):
					D_is_vertical = !D_is_vertical

			elif(tmpCom[len(tmpCom)-1] == "D"):
				D_is_vertical = !D_is_vertical

		elif(tmp == '3'):
			tmpCom[len(tmpCom) - 1] = tmpCom[len(tmpCom) - 1].lower()
		elif(tmp == ' '):
			if(tmpChange != ""):
				#for rotated cube makes change of layers
				for j in range(i, len(order)):
					if(order[j] == 'F'):
						orderList = list(order)
						orderList[j] = 'D'
						order = "".join(orderList)			
					elif(order[j] == 'B'):		
						orderList = list(order)
						orderList[j] = 'U'
						order = "".join(orderList)			
					elif(order[j] == 'U'):		
						orderList = list(order)
						orderList[j] = 'F'
						order = "".join(orderList)			
					elif(order[j] == 'D'):
						orderList = list(order)
						orderList[j] = 'B'
						order = "".join(orderList)			
					else:
						print("transforming")			
				tmpCom = tmpChange + tmpCom
			commands += tmpCom + tmp
			tmpCom = ""
			tmpChange = ""
		else:
			tmpCom += "" 
	return commands
