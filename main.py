import sys, math, argparse
from queue import Queue, LifoQueue, PriorityQueue

from Node import Node
from Board import Board
from Frontier import Frontier
from Solution import Solution

def search(initial_state, frontier, dimension, cost_fn=None):
	initial_node = Node(Board(initial_state, dimension=dimension), cost_fn=cost_fn)
	frontier.insert(initial_node)
	# steps = 0

	explored = []

	while(not frontier.empty()):
		node = frontier.get()
		explored.append(node)
		# steps += 1

		if(node.state.check_final_state()):
			solution = Solution(node, len(explored), frontier.length())
			return solution

		for child in node.expand():
			# Checks if node in frontier and get reference if it is
			alternative_node = frontier.check_node(child)

			# If not explored and not in frontier just add it
			if(child not in explored and not alternative_node):
				frontier.update(child)

			# If node already in frontier but with higher cost just replace it
			if(alternative_node and alternative_node.cost > child.cost):
				alternative_node.update(child.parent, child.depth, child.cost)

		# print([node.state.board for node in frontier.queue])
		# print([vars(node) for node in frontier.queue])
		# print()
	
	return False

def bfs(initial_state, dimension=3):
	"""  Searches for solution applying breadth first search algorithm. """
	
	return search(initial_state, Frontier(Queue), dimension)

def ids(initial_state, dimension=3):
	"""  Searches for solution applying iterative deepening search algorithm. """

	for max_depth in range(sys.maxsize):
		solution = search(initial_state, Frontier(LifoQueue, update_filter=lambda x: x if x.depth <= max_depth else False), dimension)
		if(solution):
			return solution

def uniform_cost(initial_state, dimension=3):
	"""  Searches for solution applying uniform cost search algorithm. """

	def add_cost(node):
		node.cost = node.depth

	return search(initial_state, Frontier(PriorityQueue), dimension, cost_fn=add_cost)

def manhattan_distance(puzzle):
	""" Heuristic Function to calculate the cost to take every number to correct place using manhattan distance"""

	count = 0
	dimension = puzzle.dimension
	for i in range(dimension):
		for j in range(dimension):
			correct_row = math.floor((puzzle.board[i][j] - 1) / dimension) if puzzle.board[i][j] != 0 else dimension - 1
			correct_column = (puzzle.board[i][j] % dimension) - 1 if puzzle.board[i][j] % dimension != 0 else dimension - 1

			count += abs(i - correct_row) + abs(j - correct_column)

	return count

def misplaced_nodes(puzzle):
	""" Heuristic Function to calculate number of nodes that are in the wrong position """

	count = 0
	for i in range(puzzle.dimension):
		for j in range(puzzle.dimension):
			if (puzzle.board[i][j] != puzzle.final_state[i][j] and puzzle.board[i][j] != 0): count += 1

	return count

def greedy(initial_state, heuristic, dimension=3):
	"""  Searches for solution applying greedy search algorithm with misplaced nodes heuristic. """

	def add_cost(node):
		node.cost = heuristic(node.state)

	return search(initial_state, Frontier(PriorityQueue), dimension, cost_fn=add_cost)

def a_star(initial_state, heuristic, dimension=3):
	"""  Searches for solution applying a star search algorithm with manhattan distance heuristic. """

	def add_cost(node):
		node.cost = node.depth + heuristic(node.state)

	return search(initial_state, Frontier(PriorityQueue), dimension, cost_fn=add_cost)

def hill_climbing(initial_state, heuristic, limit=1000, dimension=3):
	def add_cost(node):
		node.cost = node.depth + heuristic(node.state)

	current_node = Node(Board(initial_state, dimension=dimension), cost_fn=add_cost)
	side_moves = 0
	steps = 0

	while True:
		steps += 1
		if(side_moves > limit):
			return Solution(current_node, steps, 0)
	
		best_neighbour = None
		for child in current_node.expand():
			if(not best_neighbour): best_neighbour = child
			elif (child.cost < best_neighbour.cost):
				best_neighbour = child

		if(best_neighbour.cost > current_node.cost):
			return Solution(current_node, steps, 0)
		
		if(best_neighbour.cost == current_node.cost):
			side_moves += 1
		else:
			side_moves = 0
		
		current_node = best_neighbour

def input_parser():
	"""Parses execution arguments"""

	parser = argparse.ArgumentParser()
	parser.add_argument("file", metavar="STATE", type=str, help ='File with initial state')
	parser.add_argument("algo", metavar="ALGORITHM", type=int, help ='Search algorithm')
	parser.add_argument("heuristic", metavar="HEURISTIC", nargs="?", type=int, help ='Heuristic')

	args = parser.parse_args()

	if (args.algo > 3 and not args.heuristic):
		parser.error("For greedy, a_star or hill climbing heuristic is required")

	return args

if __name__ == "__main__":
	arguments = input_parser()
	heuristics_options = [manhattan_distance, misplaced_nodes]
	algo_options = [bfs, ids, uniform_cost, greedy, a_star, hill_climbing]

	initial_state = []
	with open(arguments.file) as fp:
		for line in fp:
			initial_state.append(list(map(int, line.strip().split())))

	dimension = len(initial_state)
	algorithm = algo_options[arguments.algo - 1]
	solution = None

	if(arguments.heuristic):
		heuristic = heuristics_options[arguments.heuristic - 1]
		solution = algorithm(initial_state, heuristic, dimension=dimension)
	else:
		solution = algorithm(initial_state, dimension=dimension)


	if(solution):
		solution.print_solution()
	else:
		print("No solution was found")

# initial_state = [[1,2,5],[3,4,0],[6,7,8]]
# initial_state = [[4,1,2], [8,7,3], [5,6,0]]
# initial_state = [[8,1,4], [3,7,5], [0,2,6]]
# initial_state = [[3,8,5], [0,7,1],[2,6,4]]
# initial_state = [[1,2,3], [4,5,6], [7,0,8]]
# initial_state = [[8,7,6], [2,5,4], [3,0,1]]
# initial_state = [[1, 2, 3, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
