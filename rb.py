from enum import Enum


class Color(Enum):
    RED = 0
    BLACK = 1

class Node:

    def __init__(self,key=None,value=None,isNull=True,parent=None):
        self.key = key
        self.value = value
        self.isNull = isNull
        self.parent = parent
        self.left = Node(parent=self) if not self.isNull else None
        self.right = Node(parent=self) if not self.isNull else None
        self.color = Color.RED if not self.isNull else Color.BLACK


    @property
    def grandparent(self):
        if self.parent:
            return self.parent.parent
    
    @property
    def isLeftChild(self): 
        if self.parent:
            return self.parent.left is self
        else:
            return False
    @property
    def sibling(self):
        if self.parent:
            if self.isLeftChild:
                return self.parent.right
            else:
                return self.parent.left
            
    

    @property
    def uncle(self):
        if not self.grandparent:
            return

        return self.parent.sibling

    def __repr__(self):
        return f"Node({self.key},{self.value},{self.color})"




class RedBlack:


    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size 

    
    def __contains__(self,key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
        

    def __getitem__(self,key):
        current = self.root

        while not current.isNull:
            if current.key == key:
                return current.value

            if key < current.key:
                current = current.left
            else:
                current = current.right

        raise KeyError(f"Key {key} not in map")

    def __setitem__(self,key,value):
        node = Node(key,value,isNull=False)
        if not self.root:
            self.root = node
        else:
            current = self.root

            while True:
                if current.key == key:
                    current.value = value
                    return

                if key < current.key:
                    if not current.left.isNull:
                        current = current.left
                    else:
                        current.left = node
                        break
                else:
                    if not current.right.isNull:
                        current = current.right
                    else:
                        current.right = node
                        break


        self.size += 1
        self.fixTree(node)
    

    def in_order_traversal(self):
        current = self.root
        stack = []

        while not current.isNull or stack:
            if not current.isNull:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                print((current.key,current.value),end=' ')
                current = current.right

        print()

    def fixTree(self,node):

        if not node.parent:
            node.color =Color.BLACK
            return
        elif node.parent.color == Color.BLACK:
            return
        else:
            if node.uncle.color == Color.RED:
                node.parent.color = Color.BLACK
                node.uncle.color = Color.BLACK
                node.grandparent.color = Color.RED
                self.fixTree(node.grandparent)
            else:
                self.rotate(node)
    

    def rotateRight(self,node):
        new_root = node.left

        assert not new_root.isNull

        node.left = new_root.right

        if new_root.right:
            new_root.right.parent = node

        new_root.parent = node.parent

        if node.parent:
            if node.isLeftChild:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        else:
            self.root = new_root


        node.parent = new_root
        new_root.right = node


    

    def rotateLeft(self,node):
        new_root = node.right

        assert not new_root.isNull

        node.right = new_root.left
        if new_root.left: #trivial
            new_root.left.parent = node

        new_root.parent = node.parent

        if node.parent:
            if node.isLeftChild:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        else:
            self.root = new_root

        node.parent = new_root
        new_root.left = node
    
    def rotateLeftRight(self,node):
        self.rotateLeft(node.left)
        self.rotateRight(node)
    

    def rotateRightLeft(self,node):
        self.rotateRight(node.right)
        self.rotateLeft(node)

    def rotate(self,node):

        if node.parent.isLeftChild:
            if node.isLeftChild:
                node.parent.color = Color.BLACK
                node.grandparent.color = Color.RED
                self.rotateRight(node.grandparent)
            else:
                node.color = Color.BLACK
                node.grandparent.color = Color.RED
                self.rotateLeftRight(node.grandparent)
        else:
            if not node.isLeftChild:
                node.parent.color = Color.BLACK
                node.grandparent.color = Color.RED
                self.rotateLeft(node.grandparent)
            else:
                node.color = Color.BLACK
                node.grandparent.color = Color.RED
                self.rotateRightLeft(node.grandparent)
    

    def _replace(self,node,child):
        child.parent = node.parent

        if node.parent:
            if node.isLeftChild:
                node.parent.left = child
            else:
                node.parent.right =child



    def _delete_node_one_child(self,node):
        child = node.left if not node.left.isNull else node.right

        self._replace(node,child)


        if not child.parent:
            if child.isNull:
                self.root = None
                return
            else:
                self.root = child


        if node.color == Color.BLACK:
            if child.color == Color.RED:
                child.color = Color.BLACK
            else:
                self._delete_case_1(child)
    

    def _delete_case_1(self,node):
        if node.parent:
            self._delete_case_2(node)


    def _delete_case_2(self,node):
        sibling = node.sibling
        #want to have red parent and black sibling
        if sibling.color == Color.RED:
            node.parent.color = Color.RED
            sibling.color = Color.BLACK
            if node.isLeftChild:
                self.rotateLeft(node.parent)
            else:
                self.rotateRight(node.parent)
        

        self._delete_case_3(node)


    def _delete_case_3(self,node):
        sibling = node.sibling

        if node.parent.color == Color.BLACK and sibling.color == Color.BLACK and sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
            sibling.color = Color.RED
            self._delete_case_1(node.parent)
        else:
            self._delete_case_4(node)
    

    def _delete_case_4(self,node):
        sibling = node.sibling

        if node.parent.color == Color.RED and sibling.color == Color.BLACK and sibling.left.color == Color.BLACK and sibling.right.color == Color.BLACK:
            node.parent.color = Color.BLACK
            sibling.color = Color.RED
        else:
            self._delete_case_5(node)
    

    def _delete_case_5(self,node):
        sibling = node.sibling

        if sibling.color == Color.BLACK:
            if node.isLeftChild and sibling.left.color == Color.RED and sibling.right.color == Color.BLACK:
                sibling.left.color = Color.BLACK
                sibling.color = Color.RED
                self.rotateRight(sibling)
            elif not node.isLeftChild and sibling.right.color == Color.RED and sibling.left.color == Color.BLACK:
                sibling.right.color = Color.BLACK
                sibling.color = Color.RED
                self.rotateLeft(sibling)


        self._delete_case_6(node)
    

    def _delete_case_6(self,node):

        sibling = node.sibling

        sibling.color = node.parent.color
        node.parent.color = Color.BLACK

        if node.isLeftChild:
            sibling.right.color = Color.BLACK
            self.rotateLeft(node.parent)
        else:
            sibling.left.color = Color.BLACK
            self.rotateRight(node.parent)





    
    def __delitem__(self,key):
        self._delete(self.root,key)


    def _delete(self,node,key):

        current = node

        while not current.isNull:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                if current.left and current.right:
                    current.key,current.value = self._getMinValueFrom(current.right)
                    self._delete(current.right,current.key)
                else:
                    self._delete_node_one_child(current)
    
    def _getMinValueFrom(self,node):
        if node.left.isNull:
            return node.key,node.value

        return self._getMinValueFrom(node.left)
