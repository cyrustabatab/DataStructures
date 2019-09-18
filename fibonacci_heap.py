import bisect
from collections import defaultdict
import unittest
import math
import pdb





def rabin_karp(s1,s2):
    assert len(s1) >= len(s2)

    x = 53
    current_hash = target_hash = 0
    same = True

    for i in range(len(s2)):
        if same and s1[i] != s2[i]:
            same = False
        current_hash = (current_hash * x + ord(s1[i]))
        target_hash = (target_hash * x + ord(s2[i]))
    
    if same:
        return 0

    power = x**(len(s2) - 1)

    for i in range(len(s2),len(s1)):
        letter_to_remove,letter_to_add = s1[i - len(s2)],s1[i]
        current_hash = (current_hash - power * ord(letter_to_remove)) * x + ord(letter_to_add)
        if current_hash == target_hash and s1[i - len(s2) + 1:i + 1] == s2:
            return i - len(s2) + 1

    return -1

class Quack:

    def __init__(self):
        self.front = []
        self.back = []
        self.buffer = []
    
    def push(self,value):
        self.front.append(value)

    def pop(self):
        if not self.front and not self.back:
            raise ValueError("Empty Quack")


        if not self.front:

            for _ in range(len(self.back) // 2):
                self.buffer.append(self.back.pop())

            while self.back:
                self.front.append(self.back.pop())

            while self.buffer:
                self.back.append(self.buffer.pop())
        
        return self.front.pop()
            
    def pull(self):
        if not self.front and self.back:
            raise ValueError("Empty Quack")

        if not self.back:

            for _ in range(len(self.front)//2):
                self.buffer.append(self.front.pop())

            while self.front:
                self.back.append(self.front.pop())

            while self.buffer:
                self.front.append(self.buffer.pop())

        return self.back.pop()

class TimeMap:
    
    def __init__(self):
        self.times = []
        self.values = []

    def get(self,time):
        if not self.times:
            return

        index = bisect.bisect_left(self.times,time)
        
        if index < len(self.times) and self.times[index] == time:
            return self.values[index]
        elif index == 0:
            return
        else:
            return self.values[index -1]

    def set(self,time,value):
        index = bisect.bisect_left(self.times,time)

        if index < len(self.times) and self.times[index] == time:
            self.values[index] = value
        elif index == len(self.times):
            self.times.append(time)
            self.values.append(value)
        else:
            self.times.insert(i,time)
            self.values.insert(i,value)

class TimeDict:

    def __init__(self):
        self.map = defaultdict(TimeMap)

    def get(self,key,time):
        return self.map[key].get(time)

    def set(self,key,value,time):
        self.map[key].set(time,value)


class Node: #represents

    def __init__(self,key):
        self.key = key
        self.child = None
        self.prev = None
        self.next = None
        self.parent = None
        self.degree = 0
        self.num_children = 0
        self.marked = False
    
    def __repr__(self):
        return f"Node({self.key})"


class FibonacciHeap:

    def __init__(self):
        self.minimum = None #pointer to minimum root(node) in fibonacci heap
        self.size = 0

    def __len__(self):
        return self.size

    def insert(self,key): #O(1)

        node = Node(key)

        if not self.minimum:
            self.minimum = node
            node.next = node
            node.prev = node
        else:
            self.minimum.prev.next= node
            node.next = self.minimum
            node.prev = self.minimum.prev
            self.minimum.prev = node
            if node.key < self.minimum.key:
                self.minimum= node

        self.size += 1
    
    def remove_min(self): #)
        if not self.minimum: #empty heap
            print("Empty Heap")
            return
        
        minimum_node = self.minimum
        value = self.minimum.key
        current_child = minimum_node.child
        count = 0

        while current_child and (current_child is not minimum_node.child or count == 0):
            temp= current_child.next
            self.minimum.prev.next  = current_child
            current_child.next = self.minimum
            current_child.prev = self.minimum.prev
            self.minimum.prev = current_child
            current_child.parent = None
            current_child = temp
            count += 1
    
        #remove minimum node from root list
        self.minimum.prev.next = self.minimum.next
        self.minimum.next.prev = self.minimum.prev

        if self.minimum is self.minimum.next: #was only node and had no children
            self.minimum = None
        else:
            self.minimum = self.minimum.next
            self.consolidate()

        self.size -= 1
        return value

    def min(self):
        if self.minimum:
            return self.minimum.key
        raise ValueError("Empty Heap") 

    def union(self,heap): #O(1)
        if isinstance(heap,FibonacciHeap):
            temp = heap.minimum.next
            heap.minimum.next = self.minimum
            self.minimum.prev.next =temp
            temp.prev = self.minimum.prev
            self.minimum.prev = heap.minimum
            self.size += heap.size
            self.minimum = self.minimum if self.minimum.key <= heap.minimum.key else heap.minimum
        else: 
            print("Can only merge another fibonacci heap object")
    
    def consolidate(self):
        '''reduce number of trees in the Fibonacci heap'''
        #degree is number of children assume O(logn) children
        #array storing that stores pointers to roots with degree[node] = i where i is index of root
        a = [None] * (int(math.log(self.size,2)) + 1) #
        current = self.minimum
        first = True 
#        pdb.set_trace()
        while current and (current is not self.minimum or first == True):
            if first:
                first = False
            x = current
            degree_x = x.degree
            while a[degree_x] is not None:
                y = a[degree_x]
                if x.key > y.key:
                    x,y = y,x
                self.link(y,x)
                if y is self.minimum:
                    self.minimum = x 
                a[degree_x] = None
                degree_x += 1

            a[degree_x] = x
            current = x.next

        self.minimum = None
        
        for i in range(len(a)):
            if a[i]:
                node = a[i]
                node.next = node
                node.prev = node
                if not self.minimum:
                    self.minimum = node
                else:
                    node.prev = self.minimum.prev
                    node.next = self.minimum
                    self.minimum.prev.next = node
                    self.minimum.prev = node
                    if node.key < self.minimum.key:
                        self.minimum = node

    def link(self,y,x):

        y.prev.next = y.next
        y.next.prev = y.prev
        y.prev = y 
        y.next = y
        if not x.child:
            x.child = y
        else:
            y.prev = x.child.prev
            y.next = x.child
            x.child.prev.next = y
            x.child.prev = y
            x.child = y 

        x.degree += 1
        y.marked = False

    def __repr__(self):
        #prints out root nodes of Fibonacci Heap 
        heap = ''
        current = self.minimum
        count = 0
        while current is not self.minimum or count == 0:
            heap += f"{current.key}" + ("->" if current.next is not self.minimum else "")
            current = current.next
            count += 1

        return heap

    def decrease_key(self,node,key): #O(1)
        if key > node.key:
            raise ValueError("New key is greater than current key")

        node.key = key

        y = node.parent #parent of node

        if y is not None and x.key < y.key: #if has parent and x.key is less than parents key
            self.cut(x,y)
            self.cascading_cut(y)

    def cut(self,x,y):
        #remove x from child list of y, decrementing y.degree
        x.prev.next = x.next
        x.next.prev = x.prev

        self.minimum.prev.next = x
        x.prev = self.minimum.prev
        x.next = self.minimum
        self.minimum.prev = x
        y.degree -= 1
        x.parent = None
        x.marked = False

    def cascading_cut(self,y):
        z = y.parent

        if z is not None:
            if not y.marked:
                y.marked = True
            else:
                self.cut(y,z)
                self.cascading_cut(z)

class Test(unittest.TestCase):

    def test_empty_heap(self):
        heap = FibonacciHeap()
        with self.assertRaises(ValueError):
            heap.min()

    def test_inserts_and_mins_only(self):
        heap = FibonacciHeap()
        heap.insert(4)
        heap.insert(3)
        self.assertEqual(heap.min(),3)
        heap.insert(5)
        heap.insert(1)
        self.assertEqual(heap.min(),1)

    def test_inserts_and_remove_min(self):

        heap = FibonacciHeap()
        heap.insert(3)
        heap.insert(4)
        heap.insert(5)
        heap.insert(1)
        self.assertEqual(heap.remove_min(),1)
        self.assertEqual(heap.min(),3)

    
    def tests_inserts_and_remove_min_2(self):
        heap = FibonacciHeap()
        heap.insert(1)
        heap.insert(10)
        heap.insert(3)
        self.assertEqual(heap.remove_min(),1)
        self.assertEqual(heap.remove_min(),3)
        self.assertEqual(heap.remove_min(),10)

    
unittest.main(verbosity=2)


    #heap = FibonacciHeap()
    #heap.insert(3)
    #heap.insert(4)
    #heap.insert(5)
    #heap.insert(1)
    #heap.remove_min()




