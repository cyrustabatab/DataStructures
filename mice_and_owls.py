import math


class Point:

    def __init__(self,x,y):
        self.x = x
        self.y = y
    

    def distance_to(self,point):
        if isinstance(point,Point):
            return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        
        raise ValueError("Can only get distance to points")

    def __repr__(self):
        return f"Point({self.x,self.y})"


class Mouse:


    def __init__(self,x,y,run_distance=3):
        self.location = Point(x,y)
        self.run_distance = run_distance

    def distance_to(self,hole):
        if isinstance(hole,Hole):
            return self.location.distance_to(hole.location)

class Hole:

    def __init__(self,x,y,capacity=0):
        self.location = Point(x,y)
        self.capacity = capacity
    

    def __repr__(self):
        return f"Hole({self.point},{self.capacity})"


class Edge:

    def __init__(self,capacity):
        self.capacity = capacity
        self.flow = 0

    @property
    def remaining_capacity(self):
        return self.capacity - self.flow
    
    def augment(self,amount):
        self.flow += amount


class FlowNode:

    def __init__(self,_id):
        self._id = _id
        self.neighbors = {}

    @property
    def id(self):
        return self._id


    def get_neighbors(self):
        return self.neighbors.keys()

    def add_neighbor(self,node,capacity=0):
        self.neighbors[node] = Edge(capacity)
    

    def augment(self,node,amount):
        self.neighbors[node].augment(amount)
        node.neighbors[self].augment(-amount)
    
    def get_remaining_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].remaining_capacity


    def get_capacity(self,node):
        if node in self.neighbors:
            return self.neighbors[node].capacity
    

    def get_flow(self,node):
        if node in self.neighbors:
            return self.neighbors[node].flow



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
    
    def __getitem__(self,_id):
        return self.node_list.get(_id)

    
    def __iter__(self):
        return iter(self.node_list.values())

    def __repr__(self):
        g = ''

        for node in self:
            g += f"{node.id}: "
            g += ','.join(str(neighbor.id) for neighbor in node.get_neighbors()) + '\n'

        return g

def mice_and_owls_solver(mice_coordinates,hole_coordinates):

    mices = {}
    holes = {}
    _id = 0
    for x,y in mice_coordinates:
        mices[_id] = Mouse(x,y)
        _id += 1
    

    for x,y,capacity in hole_coordinates:
        holes[_id] = Hole(x,y,capacity)
        _id += 1
    
    

    flow_graph = FlowGraph()
    for mouse_id,mouse in mices.items():
        for hole_id,hole in holes.items():
            if mouse.distance_to(hole) <= mouse.run_distance:
                flow_graph.add_edge(mouse_id,hole_id,1)



    source = "source"
    sink = "sink"

    for mouse in mices:
        flow_graph.add_edge(source,mouse,1)


    for hole_id,hole in holes.items():
        flow_graph.add_edge(hole_id,sink,hole.capacity)
    

    return max_flow(flow_graph,flow_graph[source],flow_graph[sink])

def dfs_visit(node,target,visited,bottleneck=float("inf")):
    if node is target:
        return bottleneck

    visited.add(node.id)
    
    current_bottleneck = bottleneck
    for neighbor in node.get_neighbors():
        if neighbor.id not in visited and node.get_remaining_capacity(neighbor) > 0:
            bottleneck = dfs_visit(neighbor,target,visited,min(current_bottleneck,node.get_remaining_capacity(neighbor)))

            if bottleneck > 0:
                node.augment(neighbor,bottleneck)
                return bottleneck

        
    return 0


def max_flow(g,source,sink):

    flow = 0
    while True:

        visited = set()

        bottleneck = dfs_visit(source,sink,visited)

        if bottleneck == 0:
            break

        flow += bottleneck
    
    return flow


if __name__ == "__main__":    
    

    mice = [(1,0),(0,1),(8,1),(12,0),(12,4),(15,5)]
    holes= [(1,1,1),(10,2,2),(14,5,1)]


    print(mice_and_owls_solver(mice,holes))

