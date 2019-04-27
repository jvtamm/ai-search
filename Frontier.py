from Node import Node
from Board import Board

class Frontier:
    def __init__(self, creator, update_filter=None):
        self.data = creator()
        self.update_filter = update_filter

    def insert(self, node):
        self.data.put(node)

    def empty(self):
        return self.data.empty()

    def get(self):
        return self.data.get()

    def length(self):
        return len(self.data.queue)

    def check_node(self, node):
        for current_node in self.data.queue:
            if (current_node == node): return node

    def update(self, data):
        if(self.update_filter):
            data = self.update_filter(data)
            if not data: return

        self.data.put(data)
	
	
    