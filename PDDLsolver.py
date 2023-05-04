import sys
import queue
import DomainParser, ProblemParser, GraphGeneration
import time

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
    def __init__(self, state, totalDistance = 0, aTobDistance = 0, parent = None, action = None):
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
        if (other == None):
            return False

        for element in self.state:
            if element not in other.state:
                return False

        return True

def breadth_first_search(initial_state, goal_state, domain, problem):
    cur_state = State_Node(initial_state)
    cur_state.totalDistance = heuristic(cur_state.state, goal_state)
    visited_list = []
    state_queue = queue.Queue()
    state_queue.put(cur_state)

    count = 0
    while (not state_queue.empty()):
        cur_state = state_queue.get()
        # if cur has not been visited then we can check it and expand it
        if not in_visited(cur_state.state, visited_list):
            if goal_check(cur_state.state, goal_state):
                # return the list of actions from start to goal
                return solve_path(cur_state)
  
            # add to visited list
            visited_list.append(cur_state.state)

            expansion = GraphGeneration.expand(problem["objects"], cur_state.state, domain)
            # print("Pretty Print:")
            # for element in expansion:
            #     print(element[0])

            for state in expansion:
                new_state = State_Node(state[1])
                new_state.parent = cur_state
                new_state.action = state[0]
                state_queue.put(new_state)
        # count += 1
        # print("current state")
        # for state in cur_state.state:
        #     print(state)
        # if count == 50:
        #     return []
    # indicates no solution
    return []


def depth_first_search(initial_state, goal_state, domain, problem):
    stack = []    
    visited = []
    cur_state = State_Node(initial_state)
    stack.append(cur_state)
    
    while len(stack) != 0:
        cur_state = stack.pop()
        if not in_visited(cur_state.state, visited):
            visited.append(cur_state.state)
            if goal_check(cur_state.state, goal_state):
                return solve_path(cur_state)
            else:
                expansion = GraphGeneration.expand(problem["objects"], cur_state.state, domain)
                for item in expansion:
                    state = State_Node(item[1])
                    state.parent = cur_state
                    state.action = item[0]
                    stack.append(state)

    return []

'''
Pick the state with the best hueristic 
'''
def greedy_best_first_search(initial_state, goal_state, domain, problem):
    cur_state = State_Node(initial_state)
    cur_state.totalDistance = heuristic(cur_state.state, goal_state)
    visited_list = []
    state_queue = queue.PriorityQueue()
    state_queue.put(cur_state)


    while (not state_queue.empty()):
        cur_state = state_queue.get()
        # if cur has not been visited then we can check it and expand it
        if not in_visited(cur_state.state, visited_list):
            if goal_check(cur_state.state, goal_state):
                # return the list of actions from start to goal
                return solve_path(cur_state)
  
            # add to visited list
            visited_list.append(cur_state.state)

            # print(cur_state)

            expansion = GraphGeneration.expand(problem["objects"], cur_state.state, domain)
            for item in expansion:
                new_state = State_Node(item[1])
                new_state.totalDistance = heuristic(item[1], goal_state)
                new_state.parent = cur_state
                new_state.action = item[0]
                state_queue.put(new_state)
    
    # indicates no solution path
    return []


            
    # while cur_state.state not in visited

'''
takes in state of the node ... state_node.state
'''
def pretty_print_list(input_list):
    print("Pretty Print:")
    for element in input_list:
        print(GraphGeneration.action_params_to_string(element))
   
'''
Find the state that will get you to goal in shortest path
We assume moveing from one state to the next is just a cost of 1 so we do not need a cost_map just a huerstic to estimate the cost
'''
def a_star_search(initial_state, goal_state, domain, problem):	
    visited_list = []
    state_queue = queue.PriorityQueue()
    cur_state = State_Node(initial_state)
    cur_state.totalDistance = heuristic(cur_state.state, goal_state)


	# add initial state to fringe
    state_queue.put(cur_state)

    while(not state_queue.empty()):
        # choose node to examine from fringe
        cur_state = state_queue.get()
        
        # if curr is not closed
        if not in_visited(cur_state.state, visited_list):
            # 	answer found if goal state
            if goal_check(cur_state.state, goal_state):
                return solve_path(cur_state)
        
            # 	keep exapnding
            else:
                expansion = GraphGeneration.expand(problem["objects"], cur_state.state, domain)
                for item in expansion:
                    h_n = heuristic(item[1], goal_state)
                    g_n = cur_state.aTobDistance + 1
                    totalDistance = g_n + h_n 
                    # new node to add to queue
                    new_state = State_Node(item[1], totalDistance, h_n, cur_state, item[0])
                    state_queue.put(new_state)
            
            visited_list.append(cur_state.state)
                
    return []

'''
This function returns true if the cur state is in visited list and false if it is not
visited_list = list of visited states
cur_state = current state ... cur_state.state
'''
def in_visited(cur_state, visited_list):
    for state in visited_list:
        in_state = True
        for predicate in cur_state:
            if predicate not in state:
                in_state = False
                break
    
        if in_state:
            return True

    return False

'''
cur_state - list of predicates representing the current state... State_Node.state
goa_State - list of predicates included in the goal state
'''
def goal_check(cur_state, goal_state):
    # loop through all predicates "has-ball", "in-room"...
    for predicate in goal_state:
        if (predicate not in cur_state):
            return False
    
    return True

'''
The state Node representing the current state
'''
def solve_path(cur_state):
    actions_to_goal = [cur_state.action]
    while cur_state.parent != None:
        cur_state = cur_state.parent
        actions_to_goal.insert(0, cur_state.action)

    # remove the None that is added from the start state because it has no actions to get to it
    actions_to_goal.pop(0)

    return actions_to_goal


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

    # print("DOMAIN DICT:")
    # print(domain_dict)
    # pretty_print_list(domain_dict["actions"])
    # print()
    # print("PROBLEM DICT")
    # print(problem_dict)
    # print()
    # pretty_print_list(problem_dict["state"])

    start = time.time()
    bfs_solution = breadth_first_search(problem_dict["state"], problem_dict["goal"], domain_dict, problem_dict)
    end = time.time()
    print("BFS Runtime:", end - start)
    pretty_print_list(bfs_solution)
    print()

    start = time.time()
    dfs_solution = depth_first_search(problem_dict["state"], problem_dict["goal"], domain_dict, problem_dict)
    end = time.time()
    print("DFS Runtime:", end - start)
    pretty_print_list(dfs_solution)
    print()

    start = time.time()
    greedy_solution = greedy_best_first_search(problem_dict["state"], problem_dict["goal"], domain_dict, problem_dict)
    end = time.time()
    print("Greedy Best First Search Runtime:", end - start)
    pretty_print_list(greedy_solution)
    print()

    start = time.time()
    a_star_search_solution = a_star_search(problem_dict["state"], problem_dict["goal"], domain_dict, problem_dict)
    end = time.time()
    print("A* Search Runtime:", end - start)
    pretty_print_list(a_star_search_solution)
    print()

    
    # GraphGeneration.expand(problem_dict['objects'], problem_dict['state'], domain_dict)
