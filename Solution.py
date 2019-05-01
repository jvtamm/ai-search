class Solution:
    def __init__(self, node, steps, frontier):
        self.explored = steps
        self.total_nodes = steps + frontier
        self.steps = steps

        self.trace_solution(node)

    def print_solution(self):
        print('Solution Path:', ' -> '.join(self.path))
        print('Expanded nodes: %s / %s' % (self.explored, self.total_nodes))
        print('Steps:', self.steps)

    def trace_solution(self, final_node):
        self.path = []
        current_node = final_node
        while(current_node):
            self.path.insert(0, str(current_node.state.board))
            current_node = current_node.parent
