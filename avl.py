


def atoi(s):

    i = len(s) - 1

    power = 0
    number = 0
    while i >=  0:
        c = s[i]
        number += (ord(c) - 48) * 10**power
        power += 1
        i -= 1

    return number





def expression_evaluation(s):
    i = 0

    operand_stack = []
    operator_stack = []
    operators = {"*": 1,"/": 1,"+":0,"-":0}

    while i < len(s):
        c = s[i]
        if c == ' ':
            i += 1
            continue
        elif c.isdigit():
            number = []
            j = i

            while j < len(s) and s[j].isdigit():
                number.append(s[j])
                j += 1

            number = int(''.join(number))

            operand_stack.append(number)
            i = j
            continue
        elif c in operators:
            while operator_stack and operator_stack[-1] != '(' and operators[c] <= operators[operand_stack[-1]]:
                evaluate(operator_stack,operand_stack)

            operator_stack.append(c)
        elif c == '(':
            operator_stack.append(c)
        elif c == ')':
            while operator_stack and operator_stack[-1] != '(':
                evaluate(operator_stack,operand_stack)

            operator_stack.pop()
        else:
            raise InvalidSymbolException(c)

        i += 1

def evaluate(operator_stack,operand_stack):
    
    operations = {"*": lambda x,y: x *y,"/": lambda x,y: x/y,"+": lambda x,y: x +y,"-": lambda x,y: x- y}

    n2 = operand_stack.pop()
    n1 = operand_stack.pop()




def big_addition(x,y):
    assert x and y

    larger = len(max(x,y,key=len))


    result = [0]  * (larger + 1)


    i,j = len(x) - 1,len(y) - 1
    carry  = 0
    end = len(result) - 1


    while i >= 0 or j >= 0 or carry != 0:
        s = (x[i] if i >= 0 else 0) + (y[j] if j >= 0 else 0) + carry
        carry = s // 10
        result[end] = s % 10
        i -= 1
        j -= 1
        end -= 1

    return result

def big_multiply(x,y):

    assert x and y

    x,y = (x,y) if len(x) >= len(y) else (y,x)


    result = None

    for i in reversed(range(len(y))):
        amount = len(y) - 1 - i

        subproduct = [0] *(amount + len(x) + 1)

        j = len(x) -1
        carry  = 0
        end = len(subproduct) - 1- amount

        while j >= 0 or carry != 0: 
            product = y[i] * (x[i] if i >= 0 else 0) + carry
            carry = product // 10
            subproduct[end] = product % 10
            end -=  1
            j -= 1


        result = subproduct if result is None else big_addition(result,subproduct)



class Node:


    def __init__(self,key,value,parent=None):
        self.key = key
        self.value = value
        self.parent = parent
        self.left = self.right = None
        self.balanceFactor = 0

    def __repr__(self):
        return f"Node({self.key},{self.value})"


class AVL:

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size


    def __setitem__(self,key,value):
        
        if not self.root:
            self.root = Node(key,value)
        else:
            current = self.root

            while True:
                if current.key == key:
                    current.value = value
                    return

                if key < current.key:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(key,value,parent=current)
                        self.updateBalancesAfterAddition(current.left)
                        break
                else:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(key,value,parent=current)
                        self.updateBalancesAfterAddition(current.right)
                        break


        self.size += 1
    
    def __contains__(self,key):
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self,key):
        current = self.root

        while current:
            if current.key == key:
                return current.value


            if key < current.value:
                current = current.left
            else:
                current = current.right


        raise KeyError(f"Key {key} not found in tree")

    def updateBalancesAfterAddition(self,node):

        if not -1 <= node.balanceFactor <= 1:
            self.rebalance(node)
            return


        if node.parent:
            if node.parent.left is node:
                node.parent.balanceFactor += 1
            else:
                node.parent.balanceFactor -= 1


            if node.parent.balanceFactor != 0:
                self.updateBalancesAfterAddition(node.parent)
    
    def rotateRight(self,node):
        new_root = node.left

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


        new_root.right =node
        node.parent = new_root

        node.balanceFactor = node.balanceFactor-1 - max(new_root.balanceFactor,0)
        new_root.balanceFactor = new_root.balanceFactor -1 + min(node.balanceFactor,0)
    

    def in_order_traversal(self):
        current = self.root
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


    def rotateLeft(self,node):
        new_root = node.right

        node.right =  new_root.left

        if new_root.left:
            new_root.left.parent = node


        new_root.parent = node.parent

        if node.parent:
            if node.parent.left is node:
                node.parent.left = new_root
            else:
                node.parent.right = new_root
        else:
            self.root = new_root


        new_root.left = node
        node.parent = new_root

        node.balanceFactor = node.balanceFactor + 1 - min(new_root.balanceFactor,0)
        new_root.balanceFactor = new_root.balanceFactor + 1 + max(node.balanceFactor,0)


    
    def rebalance(self,node):

        if node.balanceFactor > 0:
            if node.left.balanceFactor < 0:
                self.rotateLeft(node.left)
            self.rotateRight(node)
        else:
            if node.right.balanceFactor > 0:
                self.rotateRight(node.right)
            self.rotateLeft(node)
    
    def updateBalancesAfterDeletion(self,node):

        if node.balanceFactor in (-1,1):
            return


        if not -1 <= node.balanceFactor <= 1:
            stopAfterRebalancing = False
            if node.balanceFactor > 0:
                if node.left.balanceFactor == 0:
                    stopAfterRebalancing = True
            else:
                if node.right.balanceFactor == 0:
                    stopAfterRebalancing = True


            self.rebalance(node)

            if stopAfterRebalancing:
                return


        if node.parent:

            if node.parent.left is node:
                node.parent.balanceFactor -= 1
            else:
                node.parent.balanceFactor += 1


            self.updateBalancesAfterDeletion(node.parent)

        

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
                if current.left and current.right:
                    current.key,current.value = self._getMinValueFrom(current.right)
                    self._delete(current.right,current.key)
                elif current.parent is None:
                    if current.left:
                        current.key,current.value,current.balanceFactor = current.left.key,current.left.value,current.left.balanceFactor
                        current.right = current.left.right

                        if current.right:
                            current.right.parent = current

                        current.left = current.left.left

                        if current.left:
                            current.left.parent = current
                    elif current.right:
                        current.key,current.value,current.balanceFactor = current.right.key,current.right.value,current.right.balanceFactor

                        current.left = current.right.left

                        if current.left:
                            current.left.parent = current

                        current.right = current.right.right

                        if current.right:
                            current.right.parent = current
                    else:
                        self.root= None
                elif current.parent.left is current:
                    current.parent.left = current.left if current.left else current.right

                    if current.left:
                        current.left.parent = current.parent
                    elif current.right:
                        current.right.parent = current.parent

                    current.parent.balanceFactor -= 1
                    self.updateBalancesAfterDeletion(current.parent)
                elif current.parent.right is current:
                    current.parent.right = current.left if current.left else current.right

                    if current.left:
                        current.left.parent = current.parent
                    elif current.right:
                        current.right.parent = current.parent
                    
                    current.parent.balanceFactor += 1

                    self.updateBalancesAfterDeletion(current.parent)

    
    def _getMinValueFrom(self,node):
        if not node.left:
            return node.key,node.value

        return self._getMinValueFrom(node.left)


if __name__ == "__main__":
    

    s = "1142"

    print(atoi(s))
