class Node:
    def __init__(self, board, parent=None):
        self.state = board
        self.parent = parent
        self.depth = self.parent.depth + 1 if self.parent else 0

    def expand(self):
        children = []
        x, y = self.state.get_white_positon()
        if(x > 0):
            # Generate node by moving white space to the left
            children.append(Node(self.state.move(x, y, -1, 0), parent=self)) 
        if(x < self.state.dimension - 1):
            # Generate node by moving white space to the right
            children.append(Node(self.state.move(x, y, 1, 0), parent=self)) 
        if(y > 0):
            # Generate node by moving white space down
            children.append(Node(self.state.move(x, y, 0, -1), parent=self)) 
        if(y < self.state.dimension - 1):
            # Generate node by moving white space down
            children.append(Node(self.state.move(x, y, 0, 1), parent=self)) 

        return children

    # def __ne__(self, other):
    #     self.state != other.state