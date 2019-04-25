class Node:
    def __init__(self, board, cost_fn=None, parent=None):
        self.state = board
        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent else 0
        self.cost_fn = self.parent.cost_fn if self.parent else cost_fn
        
        self.set_cost()


    def set_cost(self):
        if(self.parent and self.cost_fn): self.cost_fn(self)
        else: self.cost = 0

    def update(self, new_parent, new_depth, new_cost):
        self.cost = new_cost
        self.parent = new_parent
        self.depth = new_depth

    def expand(self):
        children = []
        row, col = self.state.get_white_positon()
        if(col > 0):
            # Generate node by moving white space to the left
            children.append(Node(self.state.move(row, col, 0, -1), parent=self)) 
        if(col < self.state.dimension - 1):
            # Generate node by moving white space to the right
            children.append(Node(self.state.move(row, col, 0, 1), parent=self)) 
        if(row > 0):
            # Generate node by moving white space up
            children.append(Node(self.state.move(row, col, -1, 0), parent=self)) 
        if(row < self.state.dimension - 1):
            # Generate node by moving white space down
            children.append(Node(self.state.move(row, col, 1, 0), parent=self)) 

        return children

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return self.state != other.state