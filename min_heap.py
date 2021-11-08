import sys


class MinHeap():

    def __cmp_func(a, b):
        return a < b

    # Initialize this MinHeap with a cmp function
    def __init__(self, cmp=__cmp_func, max_v=sys.maxsize):
        self.heap = []
        self.front = 0
        self.cmp = cmp
        self.max_v = max_v

    def node(self, i):
        return self.heap[i] if i < self.front else self.max_v

    # search for val by layer until the end of the heap
    def __contains__(self, val):
        return val in self.heap

    # returns the len of the heap
    def __len__(self):
        return self.front

    # returns the parent of the node at i
    def parent(self, i):
        return (i-1) // 2

    # returns the left node of the parent node at p
    def left_node(self, p):
        return 2*p + 1

    # returns the right node at the parent node at p
    def right_node(self, p):
        return 2*p + 2

    # returns the minimum value in the heap and removes it
    def pop(self):
        if self.front == 0:
            return None

        if self.front == 1:
            _temp = self.heap[0]
            self.front = 0
            self.heap = []
            return _temp
        
        min_val = self.node(0)
        self.heap[0] = self.node(self.front - 1)
        del self.heap[self.front - 1:]
        self.front -= 1
        self.min_heapify(0)
        return min_val


    # swap's pos1 with pos2 in the heap
    def swap(self, pos1, pos2):
        self.heap[pos1], self.heap[pos2] = self.heap[pos2], self.heap[pos1]

    # inserts the val into the index and resorts the heap into min order
    def insert(self, val):
        self.heap.append(val)
        self.front += 1

        i = self.front - 1
        while i != 0 and self.cmp(self.node(i), self.node(self.parent(i))):
            self.swap(i, self.parent(i))
            i = self.parent(i)

    # Recursively heapify's the min-heap from the node at i
    def min_heapify(self, i):
        l_i = self.left_node(i)
        r_i = self.right_node(i)

        l_node = self.node(l_i)
        r_node = self.node(r_i)
        p_node = self.node(i)

        smallest = i

        if self.cmp(l_node, p_node):
            smallest = l_i

        if self.cmp(r_node, self.node(smallest)):
            smallest = r_i

        if smallest != i:
            self.swap(i, smallest)
            self.min_heapify(smallest)
