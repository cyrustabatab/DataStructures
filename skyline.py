import turtle
import pdb

def add_horizontal_line(y,x1,x2,coordinates):

#    pen.penup()
#        
#    pen.goto(x1,y)
#    pen.pendown()
#    pen.goto(x2,y)
#
#    pen.penup()
#
    
    coordinates.append(((x1,y),(x2,y)))

def add_vertical_line(x,y1,y2,coordinates):

    #pen.penup()

    #pen.goto(x,y1)
    #pen.pendown()
    #pen.goto(x,y2)

    #pen.penup()
    coordinates.append(((x,y1),(x,y2)))

class MaxHeap:

    def __init__(self):
        self.a = [None]
        self.map = {}

    @property
    def size(self):
        return len(self.a) - 1

    def max(self):
        try:
            return self.a[1]
        except:
            raise ValueError("Empty Heap")

    def add(self,point):
        self.a.append(point)
        self.map[point.id] = self.size
        self.swim()

    def remove_max(self):
        try:
            value = self.a[1]
        except:
            raise ValueError("Empty Heap")

        self._swap(1,self.size)
        
        del self.map[self.a[self.size].id]

        del self.a[self.size]

        self.sink()

        return value
    
    def increase_key(self,_id,new_height):

        index = self.map[_id]
        node = self.a[index]
        if new_height <= node.height:
            return

        node.height = new_height
        
        self.swim(index)


    def sink(self):
        i =1

        while i * 2 <= self.size:
            j = i * 2
            if j + 1 <= self.size and self.a[j + 1].height > self.a[j].height:
                j += 1

            if self.a[j].height > self.a[i].height:
                self._swap(i,j)
                i = j
            else:
                return

    def swim(self,index=None):
        i = self.size if index is None else index

        while i // 2 >= 1 and self.a[i].height > self.a[i//2].height:
            self._swap(i,i//2)
            i //= 2

    def _swap(self,i,j):
        self.a[i],self.a[j] = self.a[j],self.a[i]
        self.map[self.a[i].id] = i
        self.map[self.a[j].id] = j

    
    def delete(self,_id):
        self.increase_key(_id,float("inf"))
        self.remove_max()



    


class Point:


    def __init__(self,_id,x,height,isStart=True):
        self.id = _id
        self.x = x
        self.height  = height
        self.isStart = isStart


    def __lt__(self,point):
        if isinstance(point,Point):
            if self.x == point.x:
                if not self.isStart and point.isStart:
                    return False
                if not point.isStart and self.isStart:
                    return True
                return True
            else:
                return self.x < point.x

    
    def __repr__(self):
        return f"Node({self.id},{self.x},{self.height},{self.isStart})"

def draw_skyline(buildings):
    

    heap = MaxHeap()

    points = []
    for i,(start,end,height) in enumerate(buildings):
        points.append(Point(i,start,height))
        points.append(Point(i,end,height,isStart=False))
    

    points.sort()
    print(points)
    coordinates = []
    current_max = 0
    #current_max = points[0].height
    #heap.add(points[0])
    current_max_start = 0
#    pdb.set_trace()
    for i in range(len(points)):
        point = points[i]
        if point.isStart:
            heap.add(point)
            if point.height > current_max:
                add_horizontal_line(current_max,current_max_start,point.x,coordinates)
                add_vertical_line(point.x,current_max,point.height,coordinates)
                current_max = point.height
                current_max_start = point.x
        else:
            heap.delete(point.id)
            if current_max == point.height:
                add_horizontal_line(current_max,current_max_start,point.x,coordinates)
                old_max = current_max
                try:
                    current_max = heap.max().height
                except ValueError:
                    current_max =  0
                current_max_start = point.x
                add_vertical_line(point.x,current_max,old_max,coordinates)

    return coordinates
    
    
buildings = [(2,9,100),(3,7,150),(5,12,120),(15,20,100),(19,24,80)]



coordinates = draw_skyline(buildings)
print(coordinates)
pen = turtle.Turtle()

#pen.penup()
#pen.goto(0,0)
#pen.pendown()
#pen.goto(0,buildings[0][2])
#pen.penup()
for coordinate_1,coordinate_2 in coordinates:
    pen.penup()
    pen.goto(*coordinate_1)
    pen.pendown()
    pen.goto(*coordinate_2)
    pen.penup()

turtle.mainloop()

