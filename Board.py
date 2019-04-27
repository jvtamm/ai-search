from copy import deepcopy

class Board:
    def __init__(self, matrix, white_position=None, dimension=3):
        self.board = matrix
        self.dimension = dimension
        self.final_state = self.generate_final_state()
        self.white_position = white_position if white_position != None else self.get_white_positon()
        # self.white_position = [(index, row.index(0)) for index, row in enumerate(matrix) if 0 in row][0]

    def get_white_positon(self):
        if (not hasattr(self, 'white_position')):
            for row in range(self.dimension):
                for col in range(self.dimension):
                    if(self.board[row][col] == 0): self.white_position = (row, col)
        
        return self.white_position
    
    def check_final_state(self):
        return self.board == self.final_state

    def move(self, x, y, dx, dy):
        new_board = deepcopy(self.board)
        temp = new_board[x][y]
        new_board[x][y] = new_board[x + dx][y + dy]
        new_board[x + dx][y + dy] = temp

        return Board(new_board, (x + dx, y + dy), self.dimension)

    def generate_final_state(self):
        elements = [x for x in range(1, self.dimension**2)] + [0]
        final_state = []
        while(elements):
            final_state.append(elements[:self.dimension])
            elements = elements[self.dimension:]
        
        return final_state

    def __eq__(self, other):
        return self.board == other.board
    
    def __ne__(self, other):
        return self.board != other.board