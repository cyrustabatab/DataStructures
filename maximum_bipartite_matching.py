from collections import defaultdict



class Node:


    def __init__(self,_id):
        self._id = _id
        self.neighbors = {}

    @property
    def id(self):
        return self._id

    def get_neighbors(self):
        return self.neighbors.keys()


    def add_neighbor(self,node,weight=0):
        self.neighbors[node] = weight


    def get_weight(self,node):
        return self.neighbors.get(node)


    def __repr__(self):
        return f"Node({self.id})"


class Graph:

    def __init__(self,directed=False):
        self.directed = directed
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
            node = Node(_id)
            self.node_list[_id] = node

    def add_edge(self,n1,n2,weight=0):
        if n1 not in self.node_list:
            self.add_vertex(n1)

        if n2 not in self.node_list:
            self.add_vertex(n2)
        
        self.node_list[n1].add_neighbor(self.node_list[n2],weight)
        if not self.directed:
            self.node_list[n2].add_neighbor(self.node_list[n1],weight)

        self._edges +=1 
    
    def __iter__(self):
        return iter(self.node_list.values())

    def __getitem__(self,_id):
        return self.node_list.get(_id)

    def __repr__(self):
        g = ''

        for node in self:
            g += f"{node.id}: "
            g += ','.join(str(neighbor.id) for neighbor in node.get_neighbors()) + '\n'

        return g


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


class FlowGraph(Graph):
    

    def __init__(self):
        super().__init__(directed=True)

    def add_vertex(self,_id):
        if _id not in self.node_list:
            node = FlowNode(_id)
            self.node_list[_id] = node
    



class FlowNode(Node):

    
    def add_neighbor(self,node,capacity=0):

        self.neighbors[node] = Edge(capacity)



    def get_remaining_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].remaining_capacity


    def get_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].capacity

    def get_flow(self,node):
        if node in self.neighbors:
            return self.neighbors[node].flow

    def augment(self,node,amount):
        self.neighbors[node].augment(amount)
        node.neighbors[self].augment(-amount)
    
    def __repr__(self):
        return f"FlowNode({self.id})"


def create_flow_graph(edges,people,books):

    flow_graph = FlowGraph()

    for source,end in edges:
        flow_graph.add_edge(source,end,1)
        flow_graph.add_edge(end,source)
    
    source = "Source"
    sink = "Sink"

    for person in people:
        flow_graph.add_edge(source,person,1)
        flow_graph.add_edge(person,source)

    for book in books:
        flow_graph.add_edge(book,sink,1)
        flow_graph.add_edge(sink,book)
    

    return flow_graph,flow_graph[source],flow_graph[sink]


def dfs_visit(g,node,target,visited,bottleneck=float("inf")):
    if node is target:
        return bottleneck

    visited.add(node.id)
    
    current_bottleneck = bottleneck
    for neighbor in node.get_neighbors():
        if neighbor.id not in visited and node.get_remaining_capacity(neighbor) > 0:
            bottleneck = dfs_visit(g,neighbor,target,visited,min(node.get_remaining_capacity(neighbor),current_bottleneck))

            if bottleneck > 0:
                node.augment(neighbor,bottleneck)
                return bottleneck

    return 0



def max_flow(g,source,sink):

    flow = 0

    while True:

        visited = set()
        bottleneck = dfs_visit(g,source,sink,visited)

        if bottleneck == 0:
            break

        flow += bottleneck

    return flow

def maximum_bipartite_matching(edges):

    people = {edge[0] for edge in edges}
    books = {edge[1] for edge in edges}
    
    flow_graph,source,sink = create_flow_graph(edges,people,books)
    
    
    flow = max_flow(flow_graph,source,sink)
    
    people_to_books = {}
    for person in people:
        for neighbor in flow_graph[person].get_neighbors():
            if flow_graph[person].get_flow(neighbor) > 0:
                people_to_books[person] = neighbor.id


    
    print(people_to_books)

edges = [("Harry","Chamber of Secrets"),("Harry","Prisoner of Azkaban"),("Ron","Chamber of Secrets"),("Ron","Prisoner of Azkaban"),("Ron","Goblet of Fire"),("Hermione","Sorcerer's Stone"),("Hermione","Chamber of Secrets"),("Hermione","Goblet of Fire"),("Hermione","Order of Phoenix"),("Fred","Prisoner of Azkaban"),("George","Prisoner of Azkaban"),("George","Goblet of Fire"),("George","Order of Phoenix")]


maximum_bipartite_matching(edges)



















