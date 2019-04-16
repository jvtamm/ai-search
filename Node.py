class Node:
    def __init__(self, board, parent=None):
        self.state = board
        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent else 0
        self.cost = 0

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