class Solution:
    def __init__(self, node, explored, frontier):
        self.explored = explored
        self.total_nodes = explored + frontier

        self.trace_solution(node)

    def print_solution(self):
        print('Solution Path:', '\n'.join(self.path))
        print('Expanded nodes: %s / %s' % (self.explored, self.total_nodes))
        print('Steps:', self.steps)


    def print_to_plot(self, exec_time):
        print(self.explored, self.total_nodes, self.steps, exec_time)

    def trace_solution(self, final_node):
        self.path = []
        current_node = final_node
        while(current_node):
            self.path.insert(0, str(current_node.state.board))
            current_node = current_node.parent

        self.steps = len(self.path)
