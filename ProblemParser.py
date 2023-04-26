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
    # FORMAT: { predicate_name1: [  (T/F, [?x1, ?y1]),  (T/F, [?x2, ?y2]), …,  (T/F, [?xN, ?yN])  ],
    #           predicate_name2: [  (T/F, [?x1, ?y1]),  (T/F, [?x2, ?y2]), …,  (T/F, [?xN, ?yN])  ] }

    
def parse_goal(text):    
    e_p = re.findall(':goal.*', text)

    # find all individual conditions
    e_p = re.findall('\\(.*?\\)', e_p[0])

    e_p_dict = {}
    for i in range(len(e_p)):
        single_effect = e_p[i]

        if (single_effect[1:].strip()[:3] == "and"):
            single_effect = single_effect[1:].strip()[3:].strip() 
        
        # check if the effect has a not
        not_present = (single_effect[1:].strip()[:3] == "not")
        if (not_present):
            single_effect = single_effect[4:].strip()[1:-1].strip()
            single_effect = single_effect.split()
            effect_name = single_effect[0]
            single_effect = (False, single_effect[1:])
        else:
            single_effect = single_effect[1:-1].strip().split()
            effect_name = single_effect[0]
            single_effect =(True, single_effect[1:])
        if (effect_name in e_p_dict):
            e_p_dict[effect_name].append(single_effect)
        else:
            e_p_dict[effect_name] = [single_effect]

    return e_p_dict
    


if __name__ == "__main__":
    file_name = sys.argv[1]
    print(parse_file(file_name))
    