from copy import copy



class BIT:


    def __init__(self,nums):
        self.a = [0] * (len(nums) + 1)

        for i,num in enumerate(nums):
            self.update(i + 1,num)


    def update(self,index,num):

        while index < len(self.a):
            self.a[index] += num
            index +=  index & -index


    def query(self,index):
        
        total = 0
        while index > 0:
            total += self.a[index]
            index -= index & -index


        return total

    def range_query(self,a,b):
        return self.query(b) - self.query(a - 1)




class State:


    def __init__(self,board,distance=0,action=None,predecessor=None):
        self.board = board
        self.distance = distance
        self.action = action
        self.predecessor = predecessor


    @property
    def heuristic(self):
        return self.board.heuristic
    
    @property
    def tiles(self):
        return self.board.tiles

    def __lt__(self,state):
        if isinstance(state,State):
            return self.heuristic  + self.distance <= state.heuristic + state.distance



class Board:


    def __init__(self,tiles,size):
        self.tiles = tiles
        self.empty = self.tiles.index(0)
        self.size = size

        self._calculate_heuristic()

    
    def manhattan_distance(self,a,b):
        

        a_row,a_col = a//self.size,a%self.size
        b_row,b_col = b//self.size,b%self.size

        return abs(a_row - b_row) + abs(a_col - b_col)

    def _calculate_heuristic(self):

        total = 0
        for i in range(1,self.size**2):
            total += self.manhattan_distance(i,self.tiles.index(i))

        self.heuristic = total
    

    def _swap(self,empty,diff):

        tiles = copy(self.tiles)

        tiles[empty],tiles[empty + diff] = tiles[empty + diff],tiles[empty]

        return tiles

    def get_successors(self):
        successors = []

        empty = self.empty


        if empty // self.size > 0:
            successors.append((Board(self._swap(empty,-self.size),self.size),'D'))

        if empty // self.size < self.size:
            successors.append((Board(self._swap(empty,self.size),self.size),'U'))
        
        if empty % self.size > 0:
            successors.append((Board(self._swap(empty,-1),self.size),'R'))


        if empty % self.size < self.size: 
            successors.append((Board(self._swap(empty,1),self.size),'L'))

        
        return successors
    

    def display(self):

        for i in range(0,self.size**2,self.size):
            print(''.join(map(str,board[i:i+ self.size])))

        print()

class NPuzzle:


    def __init__(self,tiles,n=8):
        assert math.sqrt(n +1).is_integer(),"NPuzzle size needs to be one less than perfect square"
        assert len(tiles) == len(tiles[0]) == math.sqrt(n + 1),"Board size does not match N"
        
        self.n = math.sqrt(n + 1)

        self.tiles = []

        for row in tiles:
            self.tiles.extend(row)
        
        self.solve()
        self.goal_tiles = list(range(1,n + 1)) + [0]

    def search(self,start_state):

        states = []
        visited =set()
        visited.add(tuple(start_state.tiles))

        heapq.heappush(states,start_state)

        while states:
            current_state = heapq.heappop(states)
            current_board,current_distance,current_tiles = current_state.board,current_state.distance,current_state.tiles

            if current_tiles == self.goal_tiles:
                return current_state
            
            
            for successor,action in current_board.get_successors():
                successor_tiles= tuple(successor.tiles)
                if successor_tiles not in visited:
                    visited.add(successor_tiles)
                    heapq.heappush(states,State(successor,current_distance + 1,action,current_state))






    def solve(self):
        start_board = Board(self.tiles,self.n)

        start_state = State(start_board)

        self.search(start_state)
