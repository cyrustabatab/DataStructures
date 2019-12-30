


def tsp_backtracking(g,start):

    path = []
    min_cost = [float("inf")]
    min_path = [None]
    current_cost = 0 
    current_path = [start]
    vertices = set(range(len(g)))
    vertices.remove(start)
    tsp_helper(g,start,current_cost,current_path,min_cost,min_path,vertices)
    
    print(min_cost[0])
    print(min_path[0])


def tsp_helper(g,start,current_cost,current_path,min_cost,min_path,vertices):
    last_vertex = current_path[-1]
    if not vertices:
        if current_cost + g[last_vertex][start] < min_cost[0]:
            min_cost[0] =  current_cost + g[last_vertex][start]
            min_path[0] = current_path[::] + [start]

        return


    for v in vertices:

        current_path.append(v)
        
        vertices.remove(v)
        tsp_helper(g,start,current_cost + g[last_vertex][v],current_path,min_cost,min_path,vertices)

        
        vertices.add(v)
        current_path.pop()





def find_hamiltonian_cycles(g):
    

    vertices = set(range(len(g)))

    path = []


    for v in range(len(g)):
        vertices.remove(v)
        path.append(v)
        find_hamiltonian_cycles_helper(g,v,path,vertices)
        vertices.add(v)
        path.pop()



def find_hamiltonian_cycles_helper(g,start,path,vertices):
    
    last_vertex = path[-1]
    if not vertices:
        if g[last_vertex][start] is not None:
            path.append(start)
            print(path)
            path.pop()

        return

    

    for v in vertices:
        if g[last_vertex][v] is not None:
            path.append(v)
            vertices.remove(v)
            find_hamiltonian_cycles_helper(g,start,path,vertices)
            vertices.add(v)
            path.pop()













def setup(m,memo,start,n):

    for i in range(n):
        if i == start:
            continue

        memo[i][1 << i | 1 << start][0] = m[start][i]
        memo[i][1 << i | 1 << start][1] = start


def solve(m,memo,start,n):

    for r in range(3,n + 1):
        for subset in subsets(r,n): 
            if notIn(start,subset):
                continue

            for next_node in range(n):
                if next_node == start or notIn(next_node,subset):
                    continue
                state = subset ^ (1 << next_node)
                minimum = float("inf")
                min_node = None
                for end in range(n):
                    if end == start or end == next_node or notIn(end,subset):
                        continue

                    minimum,min_node = min((minimum,min_node),(memo[end][state][0] + m[end][next_node],end),key=lambda x:x[0])


                memo[next_node][subset][0] = minimum
                memo[next_node][subset][1] = min_node





def notIn(start,subset):

    return (subset >> start) & 1 == 0



def subsets(r,n):

    numbers = []
    number = 0
    subsets_helper(r,n,0,number,numbers)
    return numbers


def subsets_helper(r,n,n_index,number,numbers):

    if r == 0:
        numbers.append(number)
        return

    for i in range(n_index,n):
        number |= (1 << i)

        subsets_helper(r -1,n,i + 1,number,numbers)

        number &= ~(1 << i)
        


def find_optimal_cost(m,memo,start,n):
    
    state = (1 <<n) - 1
    minimum = float('inf')

    for i in range(n):
        if i == start:
            continue

        minimum = min(minimum,memo[i][state][0] + m[i][start])

    return minimum

def find_optimal_path(m,memo,start,n):
    
    state = (1 << n) - 1
    minimum = float("inf")
    min_node = None

    for i in range(n):
        if i == start:
            continue

        if memo[i][state][0] + m[i][start] < minimum:
            minimum = memo[i][state][0] + m[i][start]
            min_node = i

    path =[]
    current = min_node

    while current is not None:
        path.append(current)
        temp = current
        current = memo[current][state][1]
        state ^= (1 << temp)


    return path[::-1] + [start]



def tsp(m,start):
    n = len(m)
    memo = [[[0 if i == j else float("inf"),None] for j in range(2**n)] for i in range(n)]

    setup(m,memo,start,n)
    solve(m,memo,start,n)
    optimal_cost = find_optimal_cost(m,memo,start,n)
    optimal_path = find_optimal_path(m,memo,start,n)

    print(optimal_cost)
    print(optimal_path)



if __name__ == "__main__":
    

    graph = [[0,10,15,20],
             [10,0,35,25],
             [15,35,0,30],
             [20,25,30,0]]
    

    find_hamiltonian_cycles(graph)
