import sys
import re

if __name__ == "__main__":
    problem_filename = sys.argv[1]
    problem_file = open(problem_filename, "r")
    
    # Condense file into 1 line
    problem_text = ""
    for line in problem_file:
        line = line.strip()
        problem_text += line
        
    problem_text = problem_text[1:-1]
    
    
    # DOMAIN
    reg = re.findall(":domain.*?\\)", problem_text)
    domain_name = reg[0][7:-1].strip()
    print("DOMAIN:", domain_name, "\n")
    
    # OBJECTS
    reg = re.findall(":objects.*?\\)", problem_text)
    objects = reg[0][:-1].split(" ")
    objects.pop(0)
    print("OBJECTS:", objects, "\n")
    
    # INIT
    inital_state = {}
    reg = re.findall(":init.*?\\)\\)", problem_text)
    inits = reg[0][5:-1].strip()
    reg = re.findall("\\(.*?\\)", reg[0][5:-1].strip())
    for predicate in reg:
        predicate = predicate[1:-1]
        values = predicate.split()
        bindings = []
        for i in range(1, len(values)):
            bindings.append(values[i])
        
        predicate_name = values[0]
        if predicate_name in inital_state.keys():
            inital_state[predicate_name].append(bindings)
        else:
            inital_state[predicate_name] = [bindings]
        
    print("INNIT:", inital_state, "\n")
        
    # GOAL
    reg = re.findall(":goal.*?\\)", problem_text)
    reg = re.findall("\\(.*?\\)", reg[0])
    goal = reg[0][1:-1]
    print("GOAL:", goal, "\n")
    