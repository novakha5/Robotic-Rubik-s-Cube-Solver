def refactor(order):
	commands = ""
	tmpCom = ''
	tmpChange = ''
	for i in range(len(order)):
		tmp = order[i]
		if(tmp == 'R'):
			tmpCom = 'C'	
		elif(tmp == 'L'):
			tmpCom = 'D'	
		elif(tmp == 'F'):
			tmpCom = 'A'
		elif(tmp == 'B'):
			tmpCom = 'B'
		elif(tmp == 'U' or tmp == 'D'):
			tmpChange = "E c D e "
			if(tmp == 'U'):
				tmpCom = 'A'
			else:
				tmpCom = 'B'
		elif(tmp == '1'):
			print("still working")
		elif(tmp == '2'):
			tmpCom += '2'
		elif(tmp == '3'):
			tmpCom = tmpCom.lower()
		elif(tmp == ' '):
			if(len(tmpChange) != 0):
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
			tmpCom = ''
			tmpChange = ''
		else:
			print("unknown command")
	return commands
