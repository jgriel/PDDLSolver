import sys
import regex as re
# We love regex!!!

def parse_file(file_name):
    problem_file = open(file_name, "r")
        
    # Condense file of text into 1 line to rid of newline characters
    text = ""
    for line in problem_file:
        line = line.strip()
        text += line
        
    text = text[1:-1]
    
    return { "domain": parse_domain(text), "objects": parse_objects(text), "init": parse_init(text), "goal": parse_goal(text) }
    
    
def parse_domain(text):
    reg = re.findall(":domain.*?\\)", text)
    domain_name = reg[0][7:-1].strip()
    
    return domain_name


def parse_objects(text):
    reg = re.findall(":objects.*?\\)", text)
    objects = reg[0][:-1].strip().split(" ")
    objects.pop(0)
    
    return objects
    
    
def parse_init(text):
    inital_state = {}
    reg = re.findall(":init.*?\\)\\)", text)
    reg = re.findall("\\(.*?\\)", reg[0][5:-1].strip())
    
    # Go thorugh all predicates in init
    for predicate in reg:
        predicate = predicate[1:-1]
        values = predicate.split()
        bindings = []
        
        # Go through all bindings to the predicate
        for i in range(1, len(values)):
            bindings.append(values[i])
        
        predicate_name = values[0]
        
        if predicate_name in inital_state.keys():
            inital_state[predicate_name].append((True, bindings))
        else:
            inital_state[predicate_name] = [(True, bindings)]
        
    return inital_state
    # FORMAT: { predicate_name1: [  [?x1, ?y1],  [?x2, ?y2], …,  [?xN, ?yN]  ],
    #           predicate_name2: [  [?x1, ?y1],  [?x2, ?y2], …,  [?xN, ?yN]  ] }

    
def parse_goal(text):    
    reg = re.findall(":goal.*?\\)", text)
    reg = re.findall("\\(.*?\\)", reg[0])
    goal = reg[0][1:-1].strip()

    return goal


if __name__ == "__main__":
    file_name = sys.argv[1]
    print(parse_file(file_name))
    