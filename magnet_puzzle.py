

def combinations(a,n):

    aux_buffer = [None] * n

    combinations_helper(a,aux_buffer,0,0)

def combinations_helper(a,aux_buffer,a_index,buffer_index):
    if buffer_index == len(aux_buffer):
        print(aux_buffer)
        return

    for i in range(a_index,len(a)):
        number = a[i]
        aux_buffer[buffer_index] = number
        combinations_helper(a,aux_buffer,i + 1,buffer_index)

def permutations(a,n):
    aux_buffer = [None] * n
    in_buffer = set()

    permutations_helper(a,aux_buffer,in_buffer,0)

def permutations_helper(a,aux_buffer,in_buffer,buffer_index):
    if buffer_index == len(aux_buffer):
        print(aux_buffer)
        return


    for i in range(len(a)):
        if i not in in_buffer:
            aux_buffer[buffer_index] = a[i]
            in_buffer.add(i)
            permutations_helper(a,aux_buffer,in_buffer,buffer_index + 1)
            in_buffer.remove(i)
            aux_buffer[buffer_index] = None


def display_board(board):

    for row in range(len(board)):
        for col in range(len(board[0])):
            print(board[row][col],end=' ')

        print()

    print()

def is_valid(solution,rules,top,bottom,left,right,row_placed,col_placed,value):

    rows,cols = len(rules) - 1,len(rules[0]) - 1
    

    
    
    
    if value != 'x':
        if row_placed > 0 and value == solution[row_placed -1][col_placed]:
            return False


        if col_placed > 0 and value == solution[row_placed][col_placed -1]:
            return False
    

    if (value == '+' and (top[col_placed] == 0 or left[row_placed] == 0)) or (value == '-' and (bottom[col_placed] == 0 or right[row_placed] == 0)):
        return False

    
    if col_placed == cols:
        if (value == '+' and (left[row_placed] > 1 or right[row_placed] > 0)) or (value == '-' and (right[row_placed] > 1 or left[row_placed] > 0)) or (value == 'x' and (left[row_placed] > 0 or right[row_placed] > 0)): 
            return False

    

    if row_placed == rows:
        if (value == "+" and (top[col_placed] > 1 or bottom[col_placed] > 0)) or (value == '-' and (bottom[col_placed] > 1 or top[col_placed] > 0)) or (value == 'x' and (top[col_placed] > 0 or bottom[col_placed] > 0)):
            return False


    return True





     





def magnet_puzzle(rules,top,bottom,left,right):
    
    
    solution = []
    indices = [] 
    for i in range(len(rules)):
        new_row = []
        for j in range(len(rules[0])):
            new_row.append(None)
            indices.append((i,j))

        solution.append(new_row)
    
    magnet_puzzle_helper(solution,rules,top,bottom,left,right,indices,0)

def magnet_puzzle_helper(solution,rules,top,bottom,left,right,indices,index):
    

    if index == len(indices):
        display_board(solution)
        return True

    rows,cols = len(rules),len(rules[0])

    row,col = indices[index]

    
    values = ("x","-","+")

    if rules[row][col] == 'B':
        values = ("+",) if solution[row -1][col] == '-' else ('-',) if solution[row -1][col] == '+' else ('x',)
    elif rules[row][col] == 'R':
        values = ("+",) if solution[row][col - 1] == '-' else ('-',) if solution[row][col -1] == '+' else ('x',)
    

    for value in values:

        if is_valid(solution,rules,top,bottom,left,right,row,col,value):

            solution[row][col] = value
            if value == '+':
                top[col] -= 1
                left[row] -= 1
            elif value =='-':
                bottom[col] -= 1
                right[row] -= 1


            if magnet_puzzle_helper(solution,rules,top,bottom,left,right,indices,index + 1):
                return True


            if value == '+':
                top[col] += 1
                left[row] += 1
            elif value == '-':
                bottom[col] += 1
                right[row] += 1

            solution[row][col] = None


    
    return False

if __name__ == "__main__":
    

    top = [1,-1,-1,2,1,-1]
    bottom = [2,-1,-1,2,-1,3]
    left = [2,3,-1,-1,-1]
    right = [-1,-1,-1,1,-1]

    rules = [['L','R','L','R','T','T'],
             ['L','R','L','R','B','B'],
             ['T','T','T','T','L','R'],
             ['B','B','B','B','T','T'],
             ['L','R','L','R','B','B']]
    

    top_2 = [2,-1,-1]
    bottom_2 = [-1,-1,2]
    left_2= [-1,-1,2,-1]
    right_2 = [0,-1,-1,-1]
    
    rules_2 = [['T','T','T'],
               ['B','B','B'],
               ['T','L','R'],
               ['B','L','R']]
    display_board(rules_2)
    magnet_puzzle(rules_2,top_2,bottom_2,left_2,right_2)
