from collections import deque
import math

def rabin_karp(s1,s2):
    assert len(s1) >= len(s2)
    
    current_hash = target_hash = 0
    same = True
    x = 53

    for i in range(len(s2)):
        if same and s1[i] != s2[i]:
            same = False

        current_hash = current_hash * x + ord(s1[i])
        target_hash = target_hash * x + ord(s2[i])

    if same:
        return 0 

    power =x**(len(s2) - 1)

    for i in range(len(s2),len(s1)):
        letter_to_remove,letter_to_add = s1[i - len(s2)],s1[i]
        current_hash = (current_hash - power * ord(letter_to_remove)) * x + ord(letter_to_add)
        if current_hash == target_hash and s1[i - len(s2) + 1:i + 1] == s2:
            return i - len(s2) + 1

    return -1


class Edge:

    def __init__(self,capacity=0):
        self.capacity = capacity
        self.flow = 0
    

    @property
    def remaining_capacity(self):
        return self.capacity - self.flow
    
    def augment(self,amount):
        self.flow += amount

    def __repr__(self):
        return f"Edge({self.capacity},{self.flow})"


class FlowNode:

    def __init__(self,_id):
        self._id = _id
        self.neighbors = {}
        self.bottleneck = float('inf')
        self.level = float('inf')


    @property
    def id(self):
        return self._id


    def get_neighbors(self):
        return self.neighbors.keys()


    def add_neighbor(self,node,capacity=0):
        self.neighbors[node] = Edge(capacity)

    
    def get_remaining_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].remaining_capacity

    def get_flow(self,node):
        if node in self.neighbors:
            return self.neighbors[node].flow


    def get_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].capacity
    
    def augment(self,node,amount):
        self.neighbors[node].augment(amount)
        node.neighbors[self].augment(-amount)
    def __repr__(self):
        return f"Node({self.id})"



class FlowGraph:

    def __init__(self):
        self.node_list = {}
        self._edges = 0

    @property
    def num_edges(self):
        return self._edges

    @property
    def num_vertices(self):
        return len(self.node_list)


    @property
    def vertices(self):
        return self.node_list.keys()



    def add_vertex(self,_id):
        if _id not in self.node_list:
            node = FlowNode(_id)
            self.node_list[_id] = node


    def add_edge(self,n1,n2,capacity=0):
        if n1 not in self.node_list:
            self.add_vertex(n1)

        if n2 not in self.node_list:
            self.add_vertex(n2)


        self.node_list[n1].add_neighbor(self.node_list[n2],capacity)

        self.node_list[n2].add_neighbor(self.node_list[n1])

        self._edges += 2

    def __getitem__(self,_id): 
        return self.node_list.get(_id)

    def __iter__(self):
        return iter(self.node_list.values())
    

    def reset_level_graph(self):
        for node in self:
            node.level = float('-inf')
    def __repr__(self):
        g = ''

        for node in self:
            g += f"{node.id}: "
            g += ','.join(str(neighbor.id) for neighbor in node.get_neighbors()) + '\n'

        return g


def create_level_graph(node,target):

    queue = deque()
    visited = set()
    visited.add(node.id)
    node.level = 0
    queue.append(node)

    while queue:
        current_node = queue.popleft()
        if current_node is target:
            break
        
        found = False
        for neighbor in current_node.get_neighbors():
            if neighbor.id not in visited and current_node.get_remaining_capacity(neighbor) > 0:
                visited.add(neighbor.id)
                neighbor.level = current_node.level + 1
                if neighbor is target:
                    found = True
                    break
                queue.append(neighbor)
        if found:
            break
    else:
        return False


    return True

def dfs_visit_2(node,target,visited,bottleneck=float('inf')):

    if node is target:
        return bottleneck

    visited.add(node.id)
    current_bottleneck = bottleneck

    for neighbor in node.get_neighbors():
        if neighbor.id not in visited and node.get_remaining_capacity(neighbor) > 0 and neighbor.level > node.level:
            bottleneck = dfs_visit_2(neighbor,target,visited,min(current_bottleneck,node.get_remaining_capacity(neighbor)))
            
            if bottleneck > 0:
                node.augment(neighbor,bottleneck)
                return bottleneck

            neighbor.level = float('-inf')


    return 0




def dinics(g,source,sink):

    flow = 0
    while True:

        if not create_level_graph(g[source],g[sink]):
            break

        while True:

            visited = set()

            bottleneck = dfs_visit_2(g[source],g[sink],visited)

            if bottleneck == 0:
                break

            flow += bottleneck

        g.reset_level_graph()


    return flow

def bfs_visit(node,target):
    
    visited = set()
    queue = deque()
    visited.add(node.id)
    node.predecessor = None
    node.level = 0
    queue.append(node)

    while queue:
        current_node = queue.popleft()

        if current_node is target:
            break
        
        for neighbor in current_node.get_neighbors():
            if neighbor.id not in visited and current_node.get_remaining_capacity(neighbor) > 0:
                visited.add(neighbor.id)
                neighbor.level = current_node.level + 1
                neighbor.predecessor = current_node
                neighbor.bottleneck = min(current_node.bottleneck,current_node.get_remaining_capacity(neighbor))
                queue.append(neighbor)

    else:
        return 0

    current = current_node
    bottleneck = current.bottleneck 

    while current.predecessor:
        current.predecessor.augment(current,bottleneck)
        current = current.predecessor

    return bottleneck



def edmonds_karp(g,source,sink):

    flow = 0

    while True:

        bottleneck = bfs_visit(g[source],g[sink])

        if bottleneck == 0:
            break

        flow += bottleneck

    return flow


def create_residual_graph(edges):
    g = FlowGraph()

    for source,end,capacity in edges:
        g.add_edge(source,end,capacity)

    return g


def dfs_visit(node,target,visited,bottleneck=float("inf")):
    
    if node is target:
        return bottleneck
    
    visited.add(node.id)
    current_bottleneck = bottleneck

    for neighbor in node.get_neighbors():
        if neighbor.id not in visited and node.get_remaining_capacity(neighbor) > 0:
            bottleneck = dfs_visit(neighbor,target,visited,min(current_bottleneck,node.get_remaining_capacity(neighbor)))

            if bottleneck > 0:
                node.augment(neighbor)
                return bottleneck


    return 0


def capacity_scaling(g,source,sink,max_capacity):
    delta = 2**(int(math.log(max_capacity,2)))
    

    while delta:

        visited = set()
        while True:
            pass


def ford_fulkerson(g,source,sink):

    flow = 0

    while True:

        visited = set()
        bottleneck = dfs_visit(g[source],g[sink],visited)

        if bottleneck == 0:
            break

        flow += bottleneck


if __name__ == "__main__":
    
    source = "source"
    sink = "sink"
    edges = [(source,0,7),(source,1,2),(source,2,1),(0,3,2),(0,4,4),(1,4,5),(1,5,6),
             (2,3,4),(2,7,8),(3,6,7),(3,7,1),(4,6,3),(4,8,3),(4,5,8),(5,8,3),(6,sink,1),(7,sink,3),
             (8,sink,4)]
    
    
    flow_graph = create_residual_graph(edges)

    print(edmonds_karp(flow_graph,source,sink))
