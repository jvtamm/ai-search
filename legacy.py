def queue(type):
	def structure(elements, new_elements, filter_fn=None):
		if(filter_fn): new_elements = list(filter(filter_fn, new_elements))
		
		if(type == "fifo"):
			elements.extend(new_elements)
			return elements
		elif(type == "lifo"):
			new_elements.extend(elements)
			return new_elements

	return structure

# def queue(elements, new_elements, filter_fn=None):
# 	""" 
# 	Function creates a list that acts like a queue.
# 	New elements are inserted in the end so pop(0) removes always older elements first.
# 	"""

# 	if(filter_fn): new_elements = list(filter(filter_fn, new_elements))

# 	elements.extend(new_elements)
# 	return elements

# def stack(elements, new_elements, filter_fn= None):
# 	"""
# 	Function creates a list that acts like a stack.
# 	New elements are inserted at the top so pop(0) removes always newer elements first.
# 	"""

# 	if(filter_fn): new_elements = list(filter(filter_fn, new_elements))

# 	new_elements.extend(elements)
# 	return new_elements

def search(initial_state, frontier_fn,  dimension, args=None):
	# frontier = frontier_fn([], [Node(Board(initial_state, dimension=dimension))], args)
    frontier = initial_state
    explored = []

    while (frontier):
        node = frontier.pop(0)
        # explored.append(node.state.board)
        explored.append(node)

        if(node.state.check_final_state()):
            return node.state.board

        new_states = []
        for child in node.expand():
            # if(child.state.board not in explored and child not in frontier): new_states.append(child)
            if(child not in explored and child not in frontier): new_states.append(child)

        frontier = frontier_fn(frontier, new_states)
        # print([node.state.board for node in frontier])
        # print()

    return False

# def search_1(initial_state, creator, update, dimension, args=None):
# 	frontier = creator()
# 	frontier.put(Node(Board(initial_state, dimension=dimension)))
# 	explored = []

# 	while(not frontier.empty()):
# 		node = frontier.get()
# 		explored.append(node)

# 		if(node.state.check_final_state()):
# 			return node

# 		for child in node.expand():
# 			if(child not in explored and child not in frontier.queue):
# 				print(child.depth) 
# 				update(frontier, child, args)

# 		# print([node.state.board for node in frontier.queue])
# 		# print([vars(node) for node in frontier.queue])
# 		# print()
	
# 	return False

def bfs(initial_state, dimension=3):
	return search(initial_state, queue("fifo"), dimension)

def dfs(initial_state, dimension=3):
	return search(initial_state, queue("lifo"), dimension)