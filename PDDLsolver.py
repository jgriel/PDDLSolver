import DomainParser, ProblemParser, sys

# Use a visited

def breadth_first_search(initial_state, goal_state):
    pass


def depth_first_search(initial_state, goal_state):
    pass


'''
Pick the state with the best hueristic 
'''
def greedy_search(initial_state, goal_state):
    pass


'''
Find the state that will get you to goal in shortest path
'''
def a_star_search(initial_state, goal_state):
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
