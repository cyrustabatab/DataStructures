

class Node:

    def __init__(self,key,value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"Node({self.key},{self.value})"


class DLL:

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head


class LRU:


    def __init__(self,capacity=3):
        self.capacity =capacity
        self.cache = {}
        self.current_size = 0
        self.ll = DLL()

    def __setitem__(self,key,value):
        if key not in self.cache:
            if self.current_size == self.capacity:
                self.remove_least_recent()
        else:
            self._replace(key,value)


        self.set_most_recent(self.cache[key])


    def __getitem__(self,key):
        if key in self.cache:
            value = self.cache[key].value
            self.set_most_recent(self.cache[key])
            return value


            

