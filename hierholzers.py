





class Node:

    def __init__(self,_id):
        self.id = _id
        self.neighbors = {}

    @property
    def id(self):
        return self._id
    

    @property
    def num_neighbors(self):
        return len(self.neighbors)

    def get_neighbors(self):
        return self.neighbors.keys()


    def add_neighbor(self,node,directed=False):
        count = 1
        if not directed and node is self:
            count = 2
        self.neighbors[node] = weight

        if node in self.neighbors:
            self.neighbors[node] += count
        else:
            self.neighbors = count
    
    def decrement_edge(self,node,directed=False):
        count = 1

        if not directed and node is self:
            count = 2

        self.neighbors[node] -= count

    def get_num_edges(self):
        return sum(self.neighbors.values())

    def get_edge_counts(self):
        return self.neighbors.values()

    def get_edge_count(self,node):
        return self.neighbors.get(node)


    def __repr__(self):
        return f"Node({self.id})"

class Graph:

    def __init__(self,directed=False):
        self.directed = directed
        self.node_list = {}
        self._edges= 0


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
            node = Node(_id)
            self.node_list[_id] = node
    
    def remove_edge(self,n1,n2):
        if n1 not in self.node_list or n2 not in self.node_list:
            return

        self.node_list[n1].decrement_edge(self.node_list[n2],self.directed)
        if not self.directed and n1 != n2:
            self.node_list[n2].decrement_edge(self.node_list[n1])

        self._edges -= 1

    def add_edge(self,n1,n2):
        if n1 not in self.node_list:
            self.add_vertex(n1)

        if n2 not in self.node_list:
            self.add_vertex(n2)


        self.node_list[n1].add_neighbor(self.node_list[n2],self.directed)
        if not self.directed and n1 != n2:
            self.node_list[n2].add_neighbor(self.node_list[n1])

        self._edges += 1
    
    def __iter__(self):
        return iter(self.node_list.values())

    def __getitem__(self,_id):
        return self.node_list.get(_id)

    def __repr__(self):
        g =''

        for node in self:
            g += f"{node.id}: "
            g += ','.join(str(neighbor.id) for neighbor in node.get_neighbors()) + '\n'

        return g
        

def dfs_visit(node,visited):

    visited.add(node.id)

    for neighbor in node.get_neighbors():
        if neighbor.id not in visited:
            dfs_visit(neighbor,visited)

def get_undirected_version(g):
    new_graph = Graph()

    for node in g:
        for neighbor in node.get_neighbors():
            new_graph.add_edge(node.id,neighbor.id)


def hierholzers(g,f):

    is_eulerian,start = f(g)

    if not is_eulerian:
        print("Graph has no Eulerian Cycle of Eulerian Path")
        return
    else:
        if start is None:
            print("Graph has Eulerian Cycle")
            start = random.choice(list(g.vertices))
        else:
            print("Graph has Eulerian Path")


    current_path = [start]
    circuit = []
    current_vertex = start


    while current_path:
        if g[current_vertex].num_neighbors:
            for neighbor in g[current_vertex].get_neighbors():
                next_vertex = neighbor.id
                break

            g.remove_edge(current_vertex,next_vertex)
            current_vertex = next_vertex
        else:
            circuit.append(current_vertex)
            current_vertex = current_path.pop()

    return circuit[::-1]




def is_directed_eulerian(g):

    undirected_graph = get_undirected_version(g)

    number_nonzero = sum(node.num_neighbors > 0 for node in undirected_graph)

    visited = set()

    for node in undirected_graph:
        if node.num_neighbors > 0:
            dfs_visit(node,visited)
            break
    

    if len(visited) != number_nonzero:
        return False,None
    

    in_degrees = defaultdict()

    for node in g:
        for neighbor in node.neighbors():
            in_degrees[neighbor.id] += node.get_edge_count(neighbor)

    start = None
    out_degree_greater_by_1 = 0
    in_degree_greater_by_1 = 0

    for node in g:
        out_degree = node.get_num_edges()
        in_degree = in_degrees.get(node.id,0)
        if abs(in_degree - out_degree) >= 2:
            return False,None

        if out_degree > in_degree:
            if out_degree_greater_by_1 == 1:
                return False,None
            out_degree_greater_by_1 = 1
            start = node.id
        else:
            if in_degree_greater_by_1:
                return False,None

            in_degree_greater_by_1 = 1
    
    return True,start

def is_undirected_eulerian(g):

    number_nonzero = sum(node.num_neighbors > 0 for node in self)

    visited = set()

    for node in g:
        if node.num_neighbors > 0:
            dfs_visit(node,visited)
            break

    if len(visited) != number_nonzero:
        return False,None
    

    start = None
    odd_count = 0

    for node in g:
        degree = node.get_num_edges()

        if degree % 2 == 1:
            if odd_count == 2:
                return False,None

            odd_count += 1
            if start is None:
                start = node.id

    return True,start



