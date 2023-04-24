import DomainParser, ProblemParser, sys

# Use a visited

def breadth_first_search():
    pass

def depth_first_search():
    pass

'''
Pick the state with the best hueristic 
'''
def greedy_search():
    pass

'''
Find the state that will get you to goal in shortest path
'''
def a_star_search():
    pass


if __name__ == "__main__":
    domain_file = sys.argv[1]
    problem_file = sys.argv[2]

    domain_dict = DomainParser.parse_file(domain_file)
    problem_dict = ProblemParser.parse_file(problem_file)
    print("DOMAIN DICT:")
    print(domain_dict)
    print()
    print("PROBLEM DICT")
    print(problem_dict)
