from copy import deepcopy
import pdb

def rabin_karp(s1,s2):

    assert len(s1) >= len(s2)

    x = 53
    current_hash = target_hash =0
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
        current_hash = (current_hash - power * ord(letter_to_remove)) * x + ord(letter_to_add)
        if current_hash == target_hash and s1[i - len(s2) + 1:i + 1] == s2:
            return i - len(s2) + 1

    return -1


class Node:


    def __init__(self,key,value,parent=None):
        self.key = key
        self.value = value
        self.left = self.right = None
        self.parent = parent
    
    @property
    def isLeftChild(self):
        if self.parent:
            return self.parent.left is self

    @property
    def isRightChild(self):
        if self.parent:
            return self.parent.right is self

    def __repr__(self):
        return f"Node({self.key},{self.value})"





class SplayTree:


    def __init__(self,root=None):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size


    def __setitem__(self,key,value):
        if not self.root:
            self.root = Node(key,value)
        else:
            current = self.root

            while current:
                if current.key == key:
                    current.value = value
                    self.splay(current)
                    return

                if key < current.key:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(key,value,current)
                        self.splay(current.left)
                        break
                else:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(key,value,current)
                        self.splay(current.right)
                        break

        self.size += 1
    
        
    def rotateLeft(self,node):
        new_root = node.right
        assert new_root
        node.right = new_root.left
        if new_root.left:
            new_root.left.parent = node

        new_root.parent = node.parent

        if node.parent:
            if node.parent.left is node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        else:
            self.root =new_root

        
        node.parent = new_root
        new_root.left = node
    

    def rotateRight(self,node):
        new_root = node.left
        assert new_root
        node.left = new_root.right
        if new_root.right:
            new_root.right.parent = node

        new_root.parent = node.parent

        if node.parent:
            if node.parent.left is node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        else:
            self.root = new_root

        node.parent = new_root
        new_root.right = node
    
    
    def __contains__(self,key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True
    
    def __getitem__(self,key):
        current = self.root
        value = None
        while True:

            if current.key == key:
                value = current.value
                break

            if key < current.key:
                if not current.left:
                    break
                current = current.left
            else:
                if not current.right:
                    break
                current = current.right
        
        self.splay(current)

        if value is not None:
            return value

        raise KeyError(f"Key {key} not found in tree")


    def zig(self,node):
        if node.isLeftChild:
            self.rotateRight(node.parent)
        else:
            self.rotateLeft(node.parent)
    

    def zig_zig(self,node,leftRotate:bool):

        if leftRotate:
            self.rotateLeft(node.parent.parent)
            self.rotateLeft(node.parent)
        else:
            self.rotateRight(node.parent.parent)
            self.rotateRight(node.parent)
    
    def zig_zag(self,node,leftRight:bool):

        if leftRight:
            self.rotateLeft(node.parent)
            self.rotateRight(node.parent)
        else:
            self.rotateRight(node.parent)
            self.rotateLeft(node.parent)
    
    def splay(self,node):

        while node.parent:
            if node.parent is self.root: #parent is root
                self.zig(node)
            elif node.isLeftChild and node.parent.isLeftChild:
                self.zig_zig(node,False)
            elif node.isRightChild and node.parent.isRightChild:
                self.zig_zig(node,True)
            elif node.isLeftChild and node.parent.isRightChild:
                self.zig_zag(node,False)
            elif node.isRightChild and node.parent.isLeftChild:
                self.zig_zag(node,True)

    

    
    def __delitem__(self,key):
        self._delete(self.root,key)

    def _delete(self,node,key):
        current = node

        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self.size -= 1
                if current.left and current.right:
                    current.key,current.value =self._getMinValueFrom(current.right)
                    self._delete(current.right,current.key)
                elif not current.parent:
                    if current.left:
                        current.key,current.value= current.left.key,current.left.value
                        current.right = current.left.right
                        if current.right:
                            current.right.parent = current
                        current.left = current.left.left
                        if current.left:
                            current.left.parent = current
                    elif current.right:
                        current.key,current.value= current.right.key,current.right.value
                        current.left = current.right.left
                        if current.left:
                            current.left.parent = current

                        current.right = current.right.right
                        if current.right:
                            current.right.parent = current
                    else:
                        self.root = None
                elif current.parent.left is current:
                    current.parent.left = current.left if current.left else current.right
                    if current.left:
                        current.left.parent = current.parent
                    elif current.right:
                        current.right.parent = current.parent

                    self.splay(current.parent)
                elif current.parent.right is current:
                    current.parent.right = current.left if current.left else current.right
                    if current.left:
                        current.left.parent = current.parent
                    elif current.right:
                        current.right.parent = current.parent

                    self.splay(current.parent)
                    
    
    @staticmethod
    def in_order_traversal(root):
        current = root
        stack = []

        while current or stack:
            if current:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                print((current.key,current.value),end=' ')
                current = current.right
        
        print()


    def split(self,x):

        closest_greater_than_or_equal = None
        current = self.root

        while current:
            if current.key == x:
                closest_greater_than_or_equal = current
                break

            if x < current.key:
                closest_greater_than_or_equal = current
                current = current.left
            else:
                current = current.right

        self.splay(closest_greater_than_or_equal)


        left_tree = deepcopy(self.root.left) #less than x
        left_tree.parent = None#
        right_tree = deepcopy(self.root) #greater than or equal
        right_tree.left = None
        
        pdb.set_trace()
    
        SplayTree.in_order_traversal(left_tree)
        SplayTree.in_order_traversal(right_tree)


    

    def _getMinValueFrom(self,node):
        if not node.left:
            return node.key,node.value

        return self._getMinValueFrom(node.left)



if __name__ == "__main__":    
    

    st = SplayTree()

    st[4] = 2
    st[5] = 3
    st[6]= 2
    st[7] = 3

    st.split(5)
