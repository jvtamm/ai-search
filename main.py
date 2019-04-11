import sys
from copy import deepcopy
from itertools import chain
from queue import Queue, LifoQueue, PriorityQueue

from Node import Node
from Board import Board

def search(initial_state, creator, update, dimension, args=None):
	frontier = creator()
	frontier.put(Node(Board(initial_state, dimension=dimension)))
	explored = []

	while(not frontier.empty()):
		node = frontier.get()
		explored.append(node)

		if(node.state.check_final_state()):
			return node

		for child in node.expand():
			if(child not in explored and child not in frontier.queue): 
				update(frontier, child, args)

		# print([node.state.board for node in frontier.queue])
		# print()
	
	return False

def update_queue(queue, new_element, filter_fn=None):
	""" Updates the queue based on a condition/filter """
	if(filter_fn):
		new_element = filter_fn(new_element)
		if not new_element: return
	
	queue.put(new_element)

def bfs(initial_state, dimension=3):
	"""  Searches for solution applying breadth first search algorithm. """

	return search(initial_state, Queue, update_queue, dimension)

def ids(initial_state, dimension=3):
	"""  Searches for solution applying iterative deepening search algorithm. """

	for max_depth in range(sys.maxsize):
		solution = search(initial_state, LifoQueue, update_queue, dimension, args=lambda x: x if x.depth <= max_depth else False)
		if(solution):
			return solution

def uniform_cost(initial_state, dimension=3):
	return search(initial_state, PriorityQueue, update_queue, dimension)

def misplaced_nodes(puzzle):
	""" Heuristic Function to calculate number of nodes that are in the wrong position """
	
	count = 0
	for i in range(len(puzzle.dimension)):
		for j in range(len(puzzle.dimension)):
			if (puzzle.board[i][j] != puzzle.final_state[i][j]): count += 1

	return count

if __name__ == "__main__":
	initial_state = [[1,2,5],[3,4,0],[6,7,8]]
	# initial_state = [[1, 2, 3, 0], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
	result_node = ids(initial_state)

	print("Solution:", result_node.state.board)
	print("Solution depth:", result_node.depth)
