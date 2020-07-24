from string import ascii_lowercase
from random import shuffle
from sys import setrecursionlimit

setrecursionlimit(10000)

from timeit import timeit

class TreeNode:
    NODE_ID = 0
    def __init__(self, name):
        self.name = name
        self.ID = TreeNode.NODE_ID
        self.left = None
        self.right = None
        self.front = 0
        self.back = 0
        self.key = (self.name, self.ID)
        TreeNode.NODE_ID += 1


    def lt(self, other):
        if self.name == other.name:
            return self.ID < other.ID
        return self.name < other.name 

    def gt(self, other):
        if self.name == other.name:
            return self.ID > other.ID 
        return self.name > other.name

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.name == other.name and self.ID == other.ID
        
    

class IBST:
    def __init__(self):
        self.allNodes = dict()
        self.root = None

    def __len__(self):
        return len(self.allNodes)

    def count(self):
        return len(self.allNodes)

    # returns the index of where it was inserted
    # returns -1 if it already exists
    def add(self, treenode):
        if not self.root:
            self.root = treenode
            self.allNodes[treenode.key] = treenode
            return 0
        if not self.Contains(treenode):
            self.allNodes[treenode.key] = treenode
            return self.addRecursive(self.root, treenode)
        else:
            return -1

    # add 1 to the number of nodes underneath the trees under the l/r branches
    def addRecursive(self, parent, treenode):
        
        if treenode.lt(parent):
            parent.back += 1
            if parent.left == None:
                parent.left = treenode
            else:
                self.addRecursive(parent.left, treenode)
        else:
            parent.front += 1
            if parent.right == None:
                parent.right = treenode
            else:
                self.addRecursive(parent.right, treenode)


    def Contains(self, node):
        return node.key in self.allNodes

    def index_not(self, node):
        if not self.Contains(node):
            return -1
        else:
            # start with a -> move from "start 0" to root
            if node != self.root:
                return self.recursiveIndex(self.root, self.root.back + 1, node) -1
            else:
                return self.root.back
            

    def recursiveIndex(self, parent, parentIndex, node):
        if node.lt(parent):
            return self.recursiveIndex(parent.left, parentIndex -1 - parent.back, node)
        elif node.gt(parent):
            return self.recursiveIndex(parent.right, parentIndex + 1 + parent.front, node)
        else:
            return parentIndex

    def __getitem__(self, index):
        index += 1
        rootIndex = self.root.back + 1
        if index == rootIndex:
            return self.root
        elif index < rootIndex:
            return self.leftItem(self.root.left, rootIndex, index)
        else:
            return self.rightItem(self.root.right, rootIndex, index)


    def leftItem(self, node, parentIndex, index):
        leftIndex = parentIndex - 1 - node.front
        if index == leftIndex:
            return node
        elif index < leftIndex:
            return self.leftItem(node.left, leftIndex, index)
        else:
            return self.rightItem(node.right, leftIndex, index)

    def rightItem(self, node, parentIndex, index):
        leftIndex = parentIndex + 1 + node.back
        if index == leftIndex:
            return node
        elif index < leftIndex:
            return self.leftItem(node.left, leftIndex, index)
        else:
            return self.rightItem(node.right, leftIndex, index)

    def print(self):
        IBST.printInorder(self.root)

    @staticmethod    
    def printInorder(node): 
        if node: 

            IBST.printInorder(node.left)
            
            print(node.name)

            IBST.printInorder(node.right)

        
tree = IBST()

print("before list")
unsorted = list(ascii_lowercase*1000)
print("before shuffle")
shuffle(unsorted)


def slow():
    test_list = list()
    for letter in unsorted:
        count = 0
        for item in test_list:
            if letter < item.name:
                count += 1
            else:
                break
        test_list.insert(count, TreeNode(letter))
    
    for i in range(len(test_list)):
        temp = test_list[i]

def fast():
    for letter in unsorted:
        tree.add(TreeNode(letter))

    for i in range(len(tree)):
        print(tree[i].name, tree[i].ID)


def it(col):
    for i in len(col):
        temp = col[i]



#print(unsorted)
'''
for letter in unsorted:
    tree.add(TreeNode(letter))

#tree.print()
print("before printing")
for i in range(tree.count()):
    print(tree[i].name)

print(tree.root.name)
'''

    
#print(timeit(slow, number = 1))
fast()
        
