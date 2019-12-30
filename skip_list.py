
class Node:

    def __init__(self,key=None,value=None):
        self.key = key
        self.value = value
        self.next = self.prev = self.up = self.down = None

    def __repr__(self):
        return f"Node({self.key},{self.value})"


class SkipList:


    def __init__(self):
        self.head = Node(key=float("-inf"))
        self.tail = Node(key=float("inf"))
        self.head.next = self.tail
        self.tail.prev = self.head
        self.height = 0
        self.size = 0
    

    def __len__(self):
        return self.size



    def getNode(self,key):

        current = self.head

        while True:

            while current.next.key <= key:
                current = current.next

            if current.down:
                current = current.down
            else:
                break

        return current
    
    def __contains__(self,key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self,key):
        node = self.getNode(key)

        if node.key == key:
            return node.value

        raise KeyError(f"Key {key} not found")
    
    def _make_new_level(self):

        n1 = Node(float("-inf"))
        n2 = Node(float("inf"))

        n1.next = n2
        n2.prev = n1

        n1.down = self.head
        n2.down = self.tail

        self.head.up = n1
        self.tail.up = n2

        self.head = n1
        self.tail = n2

        self.height += 1

    
    def __setitem__(self,key,value):

        node = self.getNode(key)

        if node.key == key:
            node.value = value
            return

        self.size += 1

        new_node = Node(key,value)
        new_node.next = node.next
        new_node.prev = node
        node.next.prev = new_node
        node.next = new_node

        previous = new_node
        current = node
        level = 0

        while random.randint(1,2) == 1:
            if level == self.height:
                self._make_new_level()

            
            while not current.up:
                current = current.prev

            current = current.up 
            level += 1

            new_node = Node(key,value)
            new_node.next = current.next
            new_node.prev = current
            current.next.prev = new_node
            current.next = new_node

            previous.up = new_node
            new_node.down = previous


    
    def __delitem__(self,key):

        node = self.getNode(key)

        if node.key != key:
            raise KeyError(f"Key {key} not found")

        
        self.size -= 1
        current = node

        while current:
            current.prev.next = current.next
            current.next.prev = current.prev
            current = current.up

        

    
    def __repr__(self):
        sl = ''

        current_head = self.head

        while current_head:
            current =current_head
            while current:
                sl += f"{(current.key,current.value)}" + ("->" if current.next else "\n")
                current = current.next

            current_head = current_head.down
        
        return sl



        
