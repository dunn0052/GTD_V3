from queue import Queue

class Node:
    def __init__(self, value: bool):
        self.v = value
        self.l = None
        self.r = None

class BinaryTree:

    #nth most common primes to condense groupings
    PRIMES = [2,3,5,7,11,13,17,19,23,29]

    # Modular inverse > ord("z") * max_len
    # so that modular inverses will be
    # greater than max key int "zzzzzzzzz" = 1342
    INVERSE_MOD_PRIME = 1361

    def __init__(self, max_len = 11):
        self.root = Node(None)
        self.height = len(self.PRIMES)
        self.max_len = max_len


    def addKey(self, key):
        if isinstance(key, str):
            if 0 < len(key) < self.max_len:
                key = self.HashFactorKey(self.ModularInverse(self.stringToInt(key)))
            else:
                print("Key too long. Max length is: " + str(self.max_len))
                return
        else:
            print("Key must be a string")
            return

        n = self.root
        for value in key:
            value = bool(int(value))
            if value:
                if not n.r:
                    n.r = Node(value)
                n = n.r
            else:
                if not n.l:
                    n.l = Node(value)
                n = n.l 

    @staticmethod    
    def printInorder(node): 
        if node: 
            # then print the data of node 
            print(node.v)
            # First recur on left child 
            BinaryTree.printInorder(node.l) 
            # now recur on right child 
            BinaryTree.printInorder(node.r)

    def size(self):
        return self.sumNode(self.root) - 1
    
    def sumNode(self, node):
        if node:
            return self.sumNode(node.l) + self.sumNode(node.r) + 1
        else:
            return 0

    def printTree(self):
        self.printInorder(self.root)

    @staticmethod
    def stringToInt(key):
        return sum(ord(letter) for letter in key)

    # check the prime factor bases as unique key
    def HashFactorKey(self, key):
        return [key%p == 0 for p in self.PRIMES]

    # used to mix up numbers to allow for similar keys to be mapped
    # to wildly diverse integers within the max key size
    def ModularInverse(self, num):
        return pow(num, self.INVERSE_MOD_PRIME -2, self.INVERSE_MOD_PRIME)

    def getUnique(self):
        return self.IntToString(self.BinaryToInt(self.findUnique()))

    def BFS(self):
        # the list of all visited nodes
        path = list()
        to_visit = Queue()
        to_visit.put(self.root)
        while not to_visit.empty():

            node = to_visit.pop()
            
            path.append(node)
            
            if node:
                to_visit.put(node.l)
                to_visit.put(node.r)
            else:
                path.pop(-1)
                break
        return path

    



    


r = BinaryTree()

for i in range(500):
    r.addKey("Station" + str(i))

print(r.size())

print(list(l.v for l in r.BFS()))

