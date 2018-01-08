import time
import math

'''
#the sekvence is U, D, L, R, F, B (scanned)
#program gets U, R, F, D, L, B

read list of tuples (list will have 54 components (0-53))
'''
def classify(read_array):
    
    #assignes group to middle
    def learn():
        classified_array[4] = 'U'
        classified_array[13] = 'D'
        classified_array[22] = 'L'
        classified_array[31] = 'R'
        classified_array[40] = 'F'
        classified_array[49] = 'B'

    #count distance between two given colors
    def counted(read_value, learned_value):
        red = abs(int(read_value[0]) - int(learned_value[0]))
        green = abs(int(read_value[1]) - int(learned_value[1]))
        blue = abs(int(read_value[2]) - int(learned_value[2]))
        
        value = math.sqrt(red*red+blue*blue+green*green)
        return value
        
    #classify color to one of learned groups
    def classifyValue(j):
        read_value = read_array[j]
        nearest = 0
        nearest_value = 500
        for i in (4, 13, 22, 31, 40, 49):
            learned_value = read_array[i]
            value = counted(read_value, learned_value)
            if value < nearest_value:
                nearest_value = value
                nearest = classified_array[i]
        return nearest

    classified_array=[None]*54

    learn()
    
    U_number = D_number = L_number = R_number = F_number = B_number = 1

    #classify every color in given array, checks if every group has nine items at most
    for i in range(54):
        if (i != 4 and i != 13 and i != 22 and  i != 31 and i != 40 and i != 49):
            classified = classifyValue(i)
            if classified == 'U':
                U_number += 1
                if U_number > 9:
                    print("error: too much U")
                    return 2
                classified_array[i] = 'U'
            elif classified == 'D':
                D_number += 1
                if D_number > 9:
                    print("error: too much D")
                    return 2
                classified_array[i] = 'D'
            elif classified == 'L':
                L_number += 1
                if L_number > 9:
                    print("error: too much L")
                    return 2
                classified_array[i] = 'L'
            elif classified == 'R':
                R_number += 1
                if R_number > 9:
                    print("error: too much R")
                    return 2
                classified_array[i] = 'R'
            elif classified == 'F':
                F_number += 1
                if F_number > 9:
                    print("error: too much F")
                    return 2
                classified_array[i] = 'F'
            elif classified == 'B':
                B_number += 1
                if B_number > 9:
                    print("error: too much B")
                    return 2
                classified_array[i] = 'B'
            else:
                print("error: wrong classifikation")
                return 1
	
    #check if every group has nine items 
    if (U_number != D_number != L_number != R_number != F_number != B_number != 9):
        print("error: classification faild")
        return 3


    #creates string for two phase algorithm from created array in needed order
    '''
     U, D, L, R, F, B (have)
     U, R, F, D, L, B (need)
    '''
    send_str = ""

    ''' for U '''

    for i in range(9):
        send_str = send_str + classified_array[i]

    ''' for R '''
        
    for i in range(27, 36):
        send_str = send_str + classified_array[i]

    ''' for F '''

    for i in range(36, 45):
        send_str = send_str + classified_array[i]

    ''' for D '''

    for i in range(9, 18):
        send_str = send_str + classified_array[i]

    ''' for L '''

    for i in range(18, 27):
        send_str = send_str + classified_array[i]

    ''' for B '''

    for i in range(45, 54):
        send_str = send_str + classified_array[i]

    return send_str

