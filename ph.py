from collections import deque
import hashlib



class BIT:


    def __init__(self,nums):
        self.a = [0] * (len(nums) + 1)

        for i,num in enumerate(nums):
            self.update(i + 1,num)

    def update(self,index,num):

        while index < len(self.a):
            self.a[index] += num
            index += index & -index


    def query(self,index):
        total = 0

        while index > 0:
            total += self.a[index]
            index -= index & -index

        return index

class BloomFilter:


    def __init__(self,a=1000,k=3):
        self.a = [False] * a
        self.hash_algorithms = [hashlib.sha384,hashlib.md5,hashlib.sha512,hashlib.sha256,hashlib.sha1]
        self.hash_functions = [self._get_hash_function(f) for f in self.hash_algorithms[:k]]


    def _get_hash_function(self,f):

        def hash_function(value):

            v = f(value.encode('utf-8')).hexdigest()
            return int(v,16) % len(self.a)

        return hash_function

    def add(self,value):

        for f in self.hash_functions:
            self.a[f(value)] = True


    def __contains__(self,value):

        return all(f(value) for f in self.hash_functions)



def sliding_window_max(a,k):
    queue = deque()

    result = []
    for i in range(k):
        num = a[i]
        while queue and num > a[queue[-1]]::
            queue.pop()


        queue.append(i)

    
    result.append(a[queue[0]])

    
    for i in range(k,len(a)):
        num = a[i]

        while queue and num > a[queue[-1]]:
            queue.pop()


        while queue and queue[0] < i - k:
            queue.popleft()


        queue.append(i)

        result.append(a[queue[0])

    return result








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


    power = x**(len(s2) - 1)

    

    for i in range(len(s2),len(s1)):
        letter_to_remove,letter_to_add = s1[i - len(s2)],s1[i] 
        current_hash = (current_hash - power * ord(letter_to_remove)) * x + ord(letter_to_remove)
        if current_hash == target_hash and s1[i - len(s2) + 1:i + 1] == s2:
            return i - len(s2) + 1

    return -1
    


class Node:

    def __init__(self,_id,key,predecessor):
        self.id = _id
        self.key = key
        self.predecessor = predecessor
        self.next = self.previous = None
        self.child = None
    

    def add_child(self,node):

        node.previous = self
        self.child.previous = node
        node.next = self.child
        self.child = node


    def __repr__(self):
        return f"Node({self.id},{self.key})"


class PairingHeap:


    def __init__(self):
        self.minimum = None
        self.map = {}
        self.size = 0
    

    @property
    def empty(self):
        return self.size == 0

    def __len__(self):
        return self.size
    

    def merge(self,heap):
        if isinstance(heap,PairingHeap):
            if heap.empty:
                return

            if self.empty:
                self.minimum = heap.minimum
                self.size = heap.size
                return

            if heap.minimum.key < self.minimum.key:
                heap.minimum.add_child(self.minimum)
                self.minimum = heap.minimum
            else:
                self.minimum.add_child(heap.minimum)

            self.size += heap.size
        else:
            raise ValueError("Can only merge Pairing Heaps")


    def add(self,_id,key=float("inf"),predecessor=None):
        node = Node(_id,key,predecessor)
        self.map[_id] = node


        if not self.minimum:
            self.minimum = node
        else:
            if node.key < self.minimum.key:
                node.add_child(self.minimum)
                self.minimum = node
            else:
                self.minimum.add_child(node)

        self.size += 1
    
    def _two_pass(self,node):
        
        stack = []
        current = node


        while current:
            current.previous = None
            if not current.next:
                stack.append(current)
                break


            temp = current.next.next
            current.next.previous = None
            current.next.next = None

            if current.key < current.next.key:
                current.add_child(current.next)
                current.next  =None
                stack.append(current)
            else:
                current.next.add_child(current)
                stack.append(current.next)




        if not stack:
            return
        
        current = stack.pop()

        while stack:
            previous = stack.pop()

            if current.key < previous.key:
                current.add_child(previous)
            else:
                previous.add_child(current)
                current = previous



        return current









    def remove_min(self):

        if self.minimum:

            new_root = self._two_pass(self.minimum.child)
            self.size -= 1
            if new_root.key < self.minimum.key:
                new_root.add_child(self.minimum)
                self.minimum = new_root
            else:
                self.minimum.add_child(new_root)

    

    def decrease_key(self,_id,key,predecessor):
        node = self.map[_id]

        if key >= node.key:
            return
        
        node.key = key
        node.predecessor = predecessor
        if node is self.root:
            return

        if node.previous: #trivial
            if node.previous.child is node:
                node.previous.child = node.next
            else:
                node.previous.next = node.next

        if node.next:
            node.next.previous = node.previous

        
        if node.key < self.minimum.key:
            node.add_child(self.minimum)
            self.minimum = node
        else:
            self.minimum.add_child(node)

    

    def delete(self,_id):
        node = self.map[_id]

        #detach node
        if node.previous: #trivial
            if node.previous.child is node:
                node.previous.child = node.next
            else:
                node.previous.next = node.next

        if node.next:
            node.next.previous = node.previous

        
        new_root = self._two_pass(node.child)
        self.size -= 1

        if new_root.key < self.minimum.key:
            new_root.add_child(self.minimum)
            self.minimum = new_root
        else:
            self.minimum.add_child(new_root)



        




