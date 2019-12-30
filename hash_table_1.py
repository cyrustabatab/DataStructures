

def rabin_karp(s1,s2):
    assert len(s1) >= len(s2)

    x = 53
    current_hash = target_hash = 0
    same = True

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


    def __init__(self,key=None,value=None):
        self.key = key
        self.value = value
        self.next = None

    
    def __repr__(self):
        return f"Node({self.key},{self.value})"

class Map:

    def __init__(self,initial_capacity=10):
        self.capacity = initial_capacity
        self.a = [Node() for _ in range(self.capacity)]
        self.size = 0
    

    def resize(self):

        new_capacity = self.capacity * 2
        new_a = [Node() for _ in range(new_capacity)]


        for node in self.a: 
            if node.next:
                current = node.next

                while current:
                    temp = current.next
                    new_hash_value = Map.hash_function(current.key,new_capacity)
                    Map._insert(new_a,new_hash_value,current)
                    current = temp



        self.a = new_a
        self.capacity = new_capacity

    


    @staticmethod
    def _insert(a,hash_value,node):

        node.next = a[hash_value].next
        a[hash_value].next = node


    @property
    def load_factor(self):
        return self.size / self.capacity


    def __setitem__(self,key,value):
        
        if self.load_factor > 0.70:
            self.resize()

        hash_value = Map.hash_function(key,self.capacity)


        if not self.a[hash_value].next:
            self.a[hash_value].next = Node(key,value)
        else:
            current = self.a[hash_value].next
            while True:
                if current.key == key:
                    current.value = value
                    return
                

                if not current.next:
                    break

                current = current.next

            

            current.next = Node(key,value)

        self.size += 1
    
    def __getitem__(self,key):

        hash_value = Map.hash_function(key,self.capacity)

        if self.a[hash_value].next:
            current = self.a[hash_value].next

            while current:
                if current.key == key:
                    return current.value

                current = current.next


        raise KeyError(f"Key {key} not in map")
    
    def __contains__(self,key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    @staticmethod
    def hash_function(key,capacity):

        key = str(key)

        current_hash = 0
        x = 53
        for c in key[:10]:
            current_hash = current_hash * x + ord(c)

        return current_hash % capacity

    
    def __delitem__(self,key):

        hash_value = Map.hash_function(key,self.capacity)
        
        current = self.a[hash_value].next

        while current.next:
            if current.next.key == key:
                current.next = current.next.next
                self.size -= 1
                return
            current = current.next

        raise KeyError(f"Key {key} not found in map")
    
    def items(self):

        for node in self.a:
            if node.next:
                current = node.next
                while current:
                    yield (current.key,current.value)
                    current = current.next
    def values(self):

        for node in self.a:
            if node.next:
                current = node.next
                while current:
                    yield current.value
                    current = current.next

    def keys(self):

        
        return iter(self)



    
    def __iter__(self):

        for node in self.a:
            if node.next:
                current = node.next
                while current:
                    yield current.key
                    current = current.next
        



    
    def __repr__(self):
        m = ''
        
        for i,node in enumerate(self.a):
            m += f"{i}: "
            if node.next:
                current =node.next
                while current:
                    m += f"{current.key}" + ("->" if current.next else "")
                    current = current.next
            m += '\n'

        return m





