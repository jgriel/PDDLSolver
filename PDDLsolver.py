import sys
import queue
import DomainParser, ProblemParser, GraphGeneration

# Use a visited
'''
A node representing a state of the problem
state - list of statements of the state [('has-ball', ["Noah"], True), ('in-room', ["Noah"], True)]
totalDistance - totalDistance from the start to current state
aTobDistance - distance to get from 
parent - parent state of current state
action - action taken to get to this state

'''
class State_Node:
    def __init__(self, state, totalDistance, aTobDistance, parent = None, action = None):
        self.totalDistance = totalDistance # f_n 
        self.state = state
        self.aTobDistance = aTobDistance # g_n
        self.parent = parent
        self.action = action

    def __repr__(self):
        """Define internal string representation
        """
        return '(STATE: {!r}, {!r}, {!r}, {!r}, {!r})'.format(
                self.totalDistance, self.state, self.aTobDistance, self.parent, self.action)
    
    def __str__(self):
        return '(STATE: {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.totalDistance, self.state, self.aTobDistance, self.parent, self.action)
    
    def __gt__(self, other):
        return (self.totalDistance, self.aTobDistance) > (other.totalDistance, other.aTobDistance)
            
    def __lt__(self, other):
        return (self.totalDistance, self.aTobDistance) < (other.totalDistance, other.aTobDistance)

    def __eq__(self, other):
        return self.state == other.state

def breadth_first_search(initial_state, goal_state, domain):
    pass


def depth_first_search(initial_state, goal_state, domain):
    pass


'''
Pick the state with the best hueristic 
'''
def greedy_best_first_search(initial_state, goal_state, domain):
    cur_state = State_Node(initial_state, 0, 0, None, None)
    visited = []

    pass


'''
Find the state that will get you to goal in shortest path
We assume moveing from one state to the next is just a cost of 1 so we do not need a cost_map just a huerstic to estimate the cost
'''
def a_star_search(initial_state, goal_state, domain):
	# path = []
	
	# visited = set()
	# state_queue = queue.PriorityQueue()
	# cur_state = initial_state
	
	# # add initial state to fringe
	# state_queue.put(cur_state)

	# continueSearch = True
	# while(continueSearch):
	# 	# choose node to examine from fringe
	# 	if (not state_queue.empty()):
	# 		curLandmark = state_queue.get()
	# 	else:
	# 		return []
		
	# 	# if curr is not closed
	# 	if (cur_state not in visited):
	# 		# 	answer found if goal state
	# 		if (cur_state == goal_state):
	# 			continueSearch = False
		
	# 		# 	keep exapnding
	# 		else:
	# 			expansion = GraphGeneration.expand(cur_state, actions)
	# 			for neighbor in expansion:
	# 				h_n = hueristic[cur_state][goal_state]
	# 				g_n = curLandmark.aTobDistance + time_map[curLandmark.landmark][neighbor]
	# 				totalDistance = g_n + h_n 
	# 				# new node to add to queue
	# 				newLandmark = Node(totalDistance, neighbor, g_n, curLandmark)
	# 				landmarkQueue.put(newLandmark)
			
	# 		visited.add(curLandmark.landmark)
				
	# # back track to find path
	# while (curLandmark.parent != None):
	# 	path.append(curLandmark.landmark)
	# 	curLandmark = curLandmark.parent

	# path.append(curLandmark.landmark)
	# path.reverse()
	
	# return path
    pass

'''
cur_state - list of predicates representing the current state
goa_State - list of predicates included in the goal state
'''
def goal_check(cur_state, goal_state):
    # loop through all predicates "has-ball", "in-room"...
    for predicate in goal_state:
        if (predicate not in cur_state):
            return False
    
    return True

def heuristic(cur_state, goal_state):
    # count number of missing values in goal state compared to cur state
    minimum_moves_remaining = 0

    # check if the condition from the goal_state in cur_state
    for predicate in goal_state:
        if (predicate not in cur_state):
            minimum_moves_remaining += 1

    return minimum_moves_remaining

if __name__ == "__main__":
    domain_file = sys.argv[1]
    problem_file = sys.argv[2]

    domain_dict = DomainParser.parse_file(domain_file)
    problem_dict = ProblemParser.parse_file(problem_file)
    
    
    # print(heuristic(problem_dict["init"], problem_dict["goal"]))
    greedy_best_first_search(problem_dict["init"], problem_dict["goal"], domain_dict)
    # how to call search function
    # depth_first_search(problem_dict["init"], problem_dict["goal"])
    
    
    print("DOMAIN DICT:")
    print(domain_dict)
    print()
    print("PROBLEM DICT")
    print(problem_dict)
