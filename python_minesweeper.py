import random
from os import system, name 
 
def clear(): system('cls' if name == 'nt' else 'clear')
                            # windows system
    
def check_number_beside(x, y, mine_map, player_map):
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            try:
                if j == y and i == x:
                    continue
                elif j<0 or i<0:
                    continue
                if player_map[j][i]!= '⚑' and mine_map[j][i] != 0:
                    player_map[j][i] = mine_map[j][i]
            except:
                True
    return player_map
 
def beside_blank_reveal(mine_map, player_map):
    for y, j in enumerate(player_map):
        for x, i in enumerate(j):
            if i == ' ':
                player_map = check_number_beside(x, y, mine_map, player_map)
    return player_map

def fill_adjacent_blank(x, y, n, mine_map, player_map, visited):
    if x == n or y == n or x < 0 or y < 0 or mine_map[y][x] != 0 or visited[y][x] == True: # if out of bound, visited then return
        return
    if mine_map[y][x] == 0 and visited[y][x] == False: # zero that haven't been visited
        player_map[y][x] = ' '
        visited[y][x] = True
        
    fill_adjacent_blank(x-1, y, n, mine_map, player_map, visited) # recursion
    fill_adjacent_blank(x+1, y, n, mine_map, player_map, visited)
    fill_adjacent_blank(x, y-1, n, mine_map, player_map, visited)
    fill_adjacent_blank(x, y+1, n, mine_map, player_map, visited)
    
def beside_number_reveal(x, y, n, player_map, mine_map):
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            try:
                if player_map[j][i] == '⚑':
                    continue
                if mine_map[j][i] == 0:
                    visited = [[False for row in range(n)] for column in range(n)]
                    print("here")
                    fill_adjacent_blank(i, j, n, mine_map, player_map, visited)
                    player_map = beside_blank_reveal(mine_map, player_map)
                if j == y and i == x:
                    continue
                elif j<0 or i<0:
                    continue
                player_map[j][i] = mine_map[j][i]
            except:
                True
    return player_map

def mine_covered_with_flag(x, y, player_map, mine_map):
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            try:
                if j == y and i == x:
                    continue
                elif j<0 or i<0:
                    continue
                if mine_map[j][i] == 'X' and player_map[j][i] != '⚑':
                    return False
            except:
                True
    return True

def check_if_end(mine_map, player_map):
    for j, row in enumerate(player_map):
        for i, ele in enumerate(row):
            if mine_map[j][i] == 'X' and ele != '⚑': # some mines haven't been discovered
                return False
            if ele == '⚑' and mine_map[j][i] != 'X': # some flags were misplaced
                return False
    return True
    
def check_ele(cell): # draw color 
    if cell == 'X':
        print("\033[1;33;48m", end = "") # start yellow
    elif cell == '⚑':
        print("\033[1;31;48m", end = "") # start red

def print_out_interval(n):
    print("    \033[0;30;47m   \033[0m", end = "") # left side frame
    for i in range(3+(n-1)*8+4): # the middle spaces
        print(" ", end = "")
    print("\033[0;30;47m   \033[0m") # right side frame + new line

def display(map, n, k, player_map):
    #print("\033[H")
    print("\033[1;31;48m", end = "") # red
    print(str(k), "mines on the field!", end = "")
    print("\033[0m")
    #####just to print out the top##########
    print("    \033[0;30;47m      1", end = "") # 4 black spaces + 3 white spaces + 3 white spaces + '1' 
                                             # start color (white background, black font color)
    for i in range(2, n+1):
        print("       "+str(i), end = "") # 7 spaces + i each time
    print("      \033[0m") # (3 + 3) spaces + end color + new line
    ########################################    
    
    print_out_interval(n)
    for y_index, row in enumerate(map):
        print("    \033[0;30;47m"+str(y_index +1), end = "  \033[0m   ") # left side frame
        for x_index, cell in enumerate(row):
            if map[y_index][x_index] == 0: # turn mine map 0 to blank to print out
                cell = " "
            if player_map[y_index][x_index] == '⚑' and map[y_index][x_index] == 'X': # change mine_map output if the flag is on the right position
                cell = '⚑'
            check_ele(cell) # may start font folor for certain cases
            print(cell, end = "")
        # print("       ".join(str(cell) for cell in row)) # print out every element of array
            print("\033[0m", end = "") # end font color
            if x_index +1 != n: # print out 7 spaces except the last one
                print("       ", end = "")
            else:
                print("   \033[0;30;47m   \033[0m") # right side frame + new line
    
        print_out_interval(n)
        
    print("    \033[0;30;47m", end = "") # bottom
    for i in range(6+(n-1)*8+7):
        print(" ", end = "")
    print("\033[0m")
        
def create_player_map(n):
    arr = [['-' for row in range(n)] for column in range(n)]
    return arr
    
def count_the_mines(x, y, arr):
    for j in range(y-1, y+2): # -1 to 1
        for i in range(x-1, x+2):
            try:
                if j == y and i == x: # the 'X' position
                    continue # do nothing
                elif j<0 or i<0: # negative value (invalid)
                    continue
                arr[j][i] += 1
            except: # catch out of bound (exceed the boundary, invalid)
                True
    return arr

def no_mine_beside(x, y, arr):
    for j in range(y-1, y+2):
        for i in range(x-1, x+2):
            try:
                if j == y and i == x:
                    continue
                elif j<0 or i<0:
                    continue
                if arr[j][i] == 'X':
                    return False
            except:
                True
    return True

def create_mine_map(n, k, x_input, y_input):
    arr = [[0 for row in range(n)] for column in range(n)] # set all nxn elements to 0

    for i in range(k): # loop through k times, place k mines
        while True:
            x = random.randint(0,n-1)
            y = random.randint(0,n-1) # find the inner position to place a mine
            if x == x_input and y == y_input:
                continue
            if arr[y][x] == 'X':
                continue
            else:
                arr[y][x] = 'X'
                break
        
        count_the_mines(x, y, arr)
    if no_mine_beside(x_input, y_input, arr):
        return arr 
    else:
        return create_mine_map(n, k, x_input, y_input)
        
def Game(D):
    inGame = True # just to tell the programmer
    if D == 'E':
        n = 5 # canvas size 5x5
        k = 2 # place 2 mines
    elif D == 'N':
        n = 7 
        k = 7 
    elif D == 'H':
        n = 9 
        k = 15 
    first_input = True
    mine_map = create_player_map(n) # mine map haven't been initialized yet
    player_map = create_player_map(n) # initialization
    
    display(player_map, n, k, player_map)
    
    while inGame:
        while True: # check if input valid loop
            try: # enter x y
                print("\033[1;34;48m", end = "") # blue
                print("Enter x y coordinate: ", end = "")
                print("\033[0m")
                lis = input().split()
                if lis == ['inspect']: # secret key: if enter 'inspect' then display 
                    display(mine_map, n, k, player_map)
                    display(player_map, n, k, player_map)
                    continue
                x = int(lis[0])
                y = int(lis[1])
                x = x - 1 # program 0 1 2 3 4 = coordinate 1 2 3 4 5
                y = y - 1 
                        
                        
                try: # if input 'x' or 'X' behind, then place '⚑' if correct
                    flag_pos = str(lis[2])
                    if flag_pos == 'f' or flag_pos == 'F':
                        if first_input == True:
                            display(player_map, n, k, player_map)
                            print("First input cannot place flags!")
                            continue
                        if player_map[y][x] != '-' and player_map[y][x] != '⚑': # revealed
                            display(player_map, n, k, player_map)
                            print("You can't place a flag here!")
                            continue
                        elif player_map[y][x] == '⚑': # there's a flag on the player map
                            player_map[y][x] = '-'
                        elif player_map[y][x] == '-':
                            player_map[y][x] = '⚑'
                            
                        if check_if_end(mine_map, player_map):
                            display(mine_map, n, k, player_map) # end
                            print("\033[1;32;48m", end = "") # green
                            print("You Win!! You found all the mines!!!", end = "") 
                            print("\033[0m")
                            return
                        else:
                            display(player_map, n, k, player_map)
                            continue
                    else: # flag_pos invalid
                        display(player_map, n, k, player_map)
                        print("Wrong format, please try again")
                        continue
            
                except: # input nothing after x y is fine
                    True
                            
                if x>=n or x<0 or y>=n or y<0: # x y out of bound
                    display(player_map, n, k, player_map)
                    print("Wrong value, please try again")
                    continue
                break
                    
            except: # wrong x y
                display(player_map, n, k, player_map)
                print("Wrong format, please try again")
                continue
            
        if first_input == True:
            mine_map = create_mine_map(n, k, x, y)
            first_input = False
        if player_map[y][x] == '⚑':
            display(player_map, n, k, player_map)
            print("You cannot dig in this place! There's a flag!")
            continue
        elif player_map[y][x] != '-' and player_map[y][x] != '⚑' and mine_covered_with_flag(x, y, player_map, mine_map): # a number and no mine beside
            player_map = beside_number_reveal(x, y, n, player_map, mine_map)
                
        if mine_map[y][x] == 'X': # choose the position without telling it is a mine, end game, gg
            display(mine_map, n, k, player_map)
            print("\033[1;31;48m", end = "") # red
            print("GG", end = "")
            print("\033[0m")
            inGame = False
            return
        elif mine_map[y][x] == 0: # reveal
            visited = [[False for row in range(n)] for column in range(n)] # to judge if the position is visited or not
            fill_adjacent_blank(x, y, n, mine_map, player_map, visited) # print out all adjacent zero
            player_map = beside_blank_reveal(mine_map, player_map)
        else:
            player_map[y][x] = mine_map[y][x]
        display(player_map, n, k, player_map)
        #continue      
        
if __name__ == "__main__": # where the entire program start
    print('''
    MINESWEEPER -- simple version
    
    Your goal is to find out all the mines that were buried in the map and place flags on them.
    '\033[1;33;48mX\033[0m': mine '\033[1;31;48m⚑\033[0m': flag
    
    Input the coordinate of the place you want to dig. 
    Example: 2 1
    coordinate(2, 1)
    If you dig out a mine, you lose the game!
    
    Each time after you dig, you may see some numbers, which implies how many mines were buried beside each position, either above, below, left, right, or diagonally.
    Example: \033[1;33;48mX X X  X\033[0m - -
             \033[1;33;48mX\033[0m 8 \033[1;33;48mX\033[0m  - 3 -
             \033[1;33;48mX X X\033[0m  - \033[1;33;48mX X\033[0m
    You can type the coordinate of a number to clear the mark.
             
    You can place a flag where you think it's a mine, by typing 'f' or 'F' behind the input coordinate.
    You can pull up the flags by performing the same action.
    Example: 2 1 f
    Once all the mines have been properly marked, you win!
    
    Good luck!
    
    
    
    ''')
    
    print("\033[1;34;48m", end = "") # color blue start
    print('Enter the difficulty: (E = Easy, N = Normal, H = Hard)', end = "")
    print("\033[0m") # color blue end
    while True:
        D = input()
        if D == 'E' or D == 'N' or D == 'H':
            #clear()
            Game(D)
            print("Press ENTER to exit")
            exit = input() # catch any key
            break
        else:
            print('Wrong difficulty!')
            
            
            
