import sys
import math
from copy import deepcopy
from itertools import chain
from queue import Queue, LifoQueue, PriorityQueue

from Node import Node
from Board import Board
from Frontier import Frontier

def search(initial_state, frontier, dimension, cost_fn=None):
	initial_node = Node(Board(initial_state, dimension=dimension), cost_fn=cost_fn)
	frontier.insert(initial_node)

	explored = []

	while(not frontier.empty()):
		node = frontier.get()
		explored.append(node)

		if(node.state.check_final_state()):
			return node

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
			if (puzzle.board[i][j] != puzzle.final_state[i][j]): count += 1

	return count

def greedy(initial_state, dimension=3):
	"""  Searches for solution applying greedy search algorithm with misplaced nodes heuristic. """

	def add_cost(node):
		node.cost = misplaced_nodes(node.state)

	return search(initial_state, Frontier(PriorityQueue), dimension, cost_fn=add_cost)

def a_star(initial_state, dimension=3):
	"""  Searches for solution applying a star search algorithm with manhattan distance heuristic. """

	def add_cost(node):
		node.cost = node.depth + manhattan_distance(node.state)

	return search(initial_state, Frontier(PriorityQueue), dimension, cost_fn=add_cost)

if __name__ == "__main__":
	# initial_state = [[1,2,5],[3,4,0],[6,7,8]]
	# initial_state = [[4,1,2], [8,7,3], [5,6,0]]
	initial_state = [[8,1,4], [3,7,5], [0,2,6]]
	# initial_state = [[1, 2, 3, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]

	result_node = a_star(initial_state)

	print("Solution:", result_node.state.board)
	print("Solution depth:", result_node.depth)
