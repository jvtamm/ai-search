import sys, math, argparse, time
from queue import Queue, LifoQueue, PriorityQueue

from Node import Node
from Board import Board
from Frontier import Frontier
from Solution import Solution

# TODO: Remove global variable and convert to class
explored_nodes = 0

def search(initial_state, frontier, dimension, cost_fn=None, check_explored=True):
	global explored_nodes

	initial_node = Node(Board(initial_state, dimension=dimension), cost_fn=cost_fn)
	frontier.insert(initial_node)
	# steps = 0

	explored = []

	while(not frontier.empty()):
		node = frontier.get()
		# steps += 1

		explored_nodes += 1
		if(node.state.check_final_state()):
			solution = Solution(node, len(explored), frontier.length())
			return solution

		explored.append(node)

		for child in node.expand():
			# Checks if node in frontier and get reference if it is
			alternative_node = frontier.check_node(child)
			should_expand = (not check_explored) or (child not in explored)

			# If not explored and not in frontier just add it
			if(should_expand and not alternative_node):
				frontier.update(child)

			# If node already in frontier but with higher cost just replace it
			if(alternative_node and alternative_node.cost > child.cost):
				alternative_node.update(child.parent, child.depth, child.cost)

	return False

def bfs(initial_state, dimension=3):
	"""  Searches for solution applying breadth first search algorithm. """
	
	return search(initial_state, Frontier(Queue), dimension)

def ids(initial_state, dimension=3):
	"""  Searches for solution applying iterative deepening search algorithm. """

	global explored_nodes

	for max_depth in range(sys.maxsize):
		solution = search(
			initial_state, 
			Frontier(LifoQueue, update_filter=lambda x: False if x.depth > max_depth else x), 
			dimension, 
			check_explored=False
		)

		if(solution):
			solution.explored = explored_nodes
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

def hill_climbing(initial_state, heuristic, limit=10, dimension=3):
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
	parser.add_argument("file", type=str, help ='File with initial state')
	parser.add_argument("algo", metavar="algorithm", choices=[1,2,3,4,5,6], type=int, help ='The algorithm to be use. 1 = Breadth First, 2 = Iterative Deepening, 3 = Uniform Cost, 4 = Greedy, 5 = A Star, 6 = Hill Climbing')
	parser.add_argument("--heuristic", metavar="", choices=[1,2], action = 'store', dest = 'heuristic', required = False, type=int, help='The heuristic to be use in Greedy, A-Star and Hill Climbing algorithms. 1 = Manhattan distance, 2 = Missplaced Tiles.')
	parser.add_argument('--k', action='store', dest='k', required=False, type=int, default=10, help='The max number of lateral movements in Hill Climbing. The default is 10.')

	args = parser.parse_args()

	if (args.algo > 3 and not args.heuristic):
		parser.error("For Greedy, A Star or Hill Climbing heuristic is required")

	return args

def main():
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

	start_time = time.time()

	if(arguments.heuristic):
		heuristic = heuristics_options[arguments.heuristic - 1]
		if(arguments.algo == 6): 
			solution = algorithm(initial_state, heuristic, limit=arguments.k, dimension=dimension)
		else: 
			solution = algorithm(initial_state, heuristic, dimension=dimension)
	else:
		solution = algorithm(initial_state, dimension=dimension)


	if(solution):
		solution.print_solution()
		print("Execution Time: ", time.time() - start_time)
		# solution.print_to_plot(time.time() - start_time)
	else:
		print("No solution was found")

if __name__ == "__main__":
	main()
