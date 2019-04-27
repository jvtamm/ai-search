class Solution:
    def __init__(self, node, explored, frontier, steps):
        self.final_state = node
        self.explored = explored
        self.total_nodes = explored + frontier
        self.steps = steps

    def print_solution(self):
        print('Solution State:', self.final_state.state.board)
        print('Expanded nodes: %s / %s' % (self.explored, self.total_nodes))
        print('Steps:', self.steps)
