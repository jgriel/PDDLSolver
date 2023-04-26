import sys
import queue
import DomainParser, ProblemParser, GraphGeneration

# Use a visited

def breadth_first_search(initial_state, goal_state, domain):
    pass


def depth_first_search(initial_state, goal_state, domain):
    pass


'''
Pick the state with the best hueristic 
'''
def greedy_search(initial_state, goal_state, hueristic, domain):
    pass


'''
Find the state that will get you to goal in shortest path
We assume moveing from one state to the next is just a cost of 1 so we do not need a cost_map just a huerstic to estimate the cost
'''
def a_star_search(initial_state, goal_state, hueristic, domain):
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

def goalcheck(cur_state, goal_state):
    # loop through all predicates "has-ball", "in-room"...
    for predicate in goal_state:
        goal_predicate = goal_state[predicate]
        cur_predicate = cur_state[predicate]
        # loop through the tuples in the list. If predicate is has-ball then tuple_value is (True, ["Noah"])
        for tuple_value in goal_predicate:
            if (tuple_value not in cur_predicate):
                return False
    
    return True


if __name__ == "__main__":
    domain_file = sys.argv[1]
    problem_file = sys.argv[2]

    domain_dict = DomainParser.parse_file(domain_file)
    problem_dict = ProblemParser.parse_file(problem_file)
    
    # how to call search function
    # depth_first_search(problem_dict["init"], problem_dict["goal"])
    
    
    print("DOMAIN DICT:")
    print(domain_dict)
    print()
    print("PROBLEM DICT")
    print(problem_dict)
