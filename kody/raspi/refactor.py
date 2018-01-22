def refactor(order):

        #controls if it is save to do next move or if it is needed to do some preperations (gives such preparations)
        def controlTurn(use_motor):

                global A_is_vertical
                global B_is_vertical
                global C_is_vertical
                global D_is_vertical
                global E_holds_cube
                global F_holds_cube
                tmp = ""
                if(use_motor == 'A' or use_motor == 'B'):
                        if(not F_holds_cube):
                                if(not C_is_vertical):
                                        tmp += "C "
                                        C_is_vertical = not C_is_vertical
                                if(not D_is_vertical):
                                        tmp += "D "
                                        D_is_vertical = not D_is_vertical
                                tmp += "f "
                                F_holds_cube = not F_holds_cube
                        else:
                                if(not C_is_vertical or not D_is_vertical):
                                        if(not E_holds_cube):
                                                tmp += "e "
                                                E_holds_cube = not E_holds_cube
                                        tmp += "F "
                                        F_holds_cube = not F_holds_cube
                                        if(not C_is_vertical):
                                                tmp += "C "
                                                C_is_vertical = not C_is_vertical
                                        if(not D_is_vertical):
                                                tmp += "D "
                                                D_is_vertical = not D_is_vertical
                                        tmp += "f "
                                        F_holds_cube = not F_holds_cube
                                if(not E_holds_cube):
                                        tmp += "e "
                                        E_holds_cube = not E_holds_cube
                elif(use_motor == 'C' or use_motor == 'D'):
                        if(not E_holds_cube):
                                if(not A_is_vertical):
                                        tmp += "A "
                                        A_is_vertical = not A_is_vertical
                                if(not B_is_vertical):
                                        tmp += "B "
                                        B_is_vertical = not B_is_vertical
                                tmp += "e "
                                E_holds_cube = not E_holds_cube
                        else:
                                if(not A_is_vertical or not B_is_vertical):
                                        if(not F_holds_cube):
                                                tmp += "f "
                                                F_holds_cube = not F_holds_cube
                                        tmp += "E "
                                        if(not A_is_vertical):
                                                tmp += "A "
                                                A_is_vertical = not A_is_vertical
                                        if(not B_is_vertical):
                                                tmp += "B "
                                                B_is_vertical = not B_is_vertical
                                        tmp += "e "
                                        E_holds_cube = not E_holds_cube
                        if(not F_holds_cube):
                                tmp += "f "
                                F_holds_cube = not F_holds_cube

                return tmp

        #check if it is save to rotate the cube
        def controlRotate():

                global A_is_vertical
                global B_is_vertical
                global C_is_vertical
                global D_is_vertical
                global E_holds_cube
                global F_holds_cube       
                tmp = ""

                if(not F_holds_cube):
                        if(not C_is_vertical):
                                tmp += "C "
                                C_is_vertical = not C_is_vertical
                        if(not D_is_vertical):
                                tmp += "D "
                                D_is_vertical = not D_is_vertical
                        tmp += "f "
                        F_holds_cube = not F_holds_cube
                if(E_holds_cube):
                        tmp += "E "
                        E_holds_cube = not E_holds_cube
                return tmp

        commands = ""
        tmpCom = ""
        tmpChange = ""

        global A_is_vertical
        global B_is_vertical
        global C_is_vertical
        global D_is_vertical
        global E_holds_cube
        global F_holds_cube
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
                        C_is_vertical = not C_is_vertical
                elif(tmp == 'L'):
                        tmpCom += controlTurn('D')
                        tmpCom += "D"
                        D_is_vertical = not D_is_vertical
                elif(tmp == 'F'):
                        tmpCom += controlTurn('A')
                        tmpCom += "A"
                        A_is_vertical = not A_is_vertical
                elif(tmp == 'B'):
                        tmpCom += controlTurn('B')
                        tmpCom += "B"
                        B_is_vertical = not B_is_vertical
                elif(tmp == 'U' or tmp == 'D'): 
                        tmpChange += controlRotate()
                        tmpChange += "cD e "
                        D_is_vertical = not D_is_vertical
                        C_is_vertical = not C_is_vertical
                        E_holds_cube = not E_holds_cube
                        if(tmp == 'U'):
                                tmpCom += controlTurn('A')
                                tmpCom += "A"
                                A_is_vertical = not A_is_vertical
                        else:
                                tmpCom += controlTurn('B')
                                tmpCom += "B"
                                B_is_vertical = not B_is_vertical
                elif(tmp == '2'):
                        tmpCom += "2"
                        if(tmpCom[len(tmpCom)-2] == "A"):
                                A_is_vertical = not A_is_vertical
                                if(tmpCom[len(tmpCom)-2] == "B"):
                                        B_is_vertical = not B_is_vertical

                        elif(tmpCom[len(tmpCom)-2] == "B"):
                                B_is_vertical = not B_is_vertical

                        elif(tmpCom[len(tmpCom)-2] == "C"):
                                C_is_vertical = not C_is_vertical
                                if(tmpCom[len(tmpCom)-2] == "D"):
                                        D_is_vertical = not D_is_vertical

                        elif(tmpCom[len(tmpCom)-2] == "D"):
                                D_is_vertical = not D_is_vertical

                elif(tmp == '3'):
			changing = tmpCom[len(tmpCom)-1]
			tmpCom = tmpCom[:-1]
			if(changing == "A"):
				tmpCom += "a"
			elif(changing == "B"):
				tmpCom += "b"
			elif(changing == "C"):
				tmpCom += "c"
			elif(changing == "D"):
				tmpCom += "d"
			if(changing == "E"):
				tmpCom += "e"
			if(changing == "F"):
				tmpCom += "f"
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
                                                tmpCom += ""
                                tmpCom = tmpChange + tmpCom
                        commands += tmpCom + tmp
                        #print("commands: {0}").format(tmpCom)
                        tmpCom = ""
                        tmpChange = ""
                elif(tmp == '('):
                        commands += "."
                        return commands
                else:
                        tmpCom += "" 
        return commands
    
A_is_vertical = True
B_is_vertical = True
C_is_vertical = True
D_is_vertical = True
E_holds_cube = True
F_holds_cube = True
