import sys, regex as re


def parse_domain_name(domain_text):
    # get domain name
    return re.findall('domain.*?\\)', domain_text)[0][6:-1].strip()


def parse_predicates(domain_text):
    #get predicates
    predicates_list = re.findall(':predicates.*?\\)\\)', domain_text)[0]
    predicates_list = re.findall('\\(.*?\\)', predicates_list)
    predicates_dict = {}
    for i in range(len(predicates_list)):
        predicate = predicates_list[i][1:-1].split()
        predicates_dict[predicate[0]] = predicate[1:]

    return predicates_dict

'''
This function will parse the preconditions or effects of an action
The format of the precondition and effect are identical so the code is the same besides the regex
Parameters: string of the action block, whether it should parse the effect or precondition
'''
def parse_conditions(action, effect_precondition):
    # different regex for effect and precondition
    if (effect_precondition == "effect"):
        e_p = re.findall(':'+ effect_precondition + '.*?\\(.*:', action)
    else:
        e_p = re.findall(':'+ effect_precondition + '.*?\\.*:', action)
    # if the action is at the end of the file, the regex should be different because there is no ':'
    if (e_p == []):
        e_p = re.findall(':'+ effect_precondition + '.*', action)

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

def parse_actions(domain_text):
    #get actions
    # actions anywhere in the file except the end (middle of file)
    action_mof = re.findall(':action.*?\\(\s*:', domain_text, overlapped=True)
 
    # action at the end of the file if it exists
    reversed_domain_text = domain_text[::-1]
    action_eof = re.findall('.*?noitca:', reversed_domain_text)
    action_eof = [action_eof[0][::-1]]
    
    # combine all actions (middle of file + end of file if action is at end of file). 
    # actions always have 4 colons 
    if (":action" == action_eof[0][:7] and action_eof[0].count(":") == 4):
        actions = action_mof + action_eof
    else:
        actions = action_mof

    action_dict = {}
    for i in range(len(actions)):
        # name
        action_name = re.findall(':action.*?:', actions[i])
        action_name = action_name[0][7:-1].strip()

        # paramtersof
        parameters = re.findall(':parameters.*?:', actions[i])
        parameters = parameters[0][11:-2].strip()[1:].split()

        # preconditions
        precondition_dict = parse_conditions(actions[i], "precondition")

        # effects
        effect_dict = parse_conditions(actions[i], "effect")
        
        action_dict[action_name] = {'parameters':parameters, 'precondition':precondition_dict, 'effects':effect_dict}

    return action_dict


def parse_file(domain_filename):
    domain_file = open(domain_filename, 'r')
    
    # get domain file text
    domain_text = ''
    for line in domain_file:
        domain_text += line.strip()
    domain_text = domain_text[1:-1]

    return {'name':parse_domain_name(domain_text), 'predicates':parse_predicates(domain_text), 'actions':parse_actions(domain_text)}


if __name__ == "__main__":
    domain_filename = sys.argv[1]

    domain_dict = parse_file(domain_filename)
    print("name:", domain_dict["name"])
    print()
    print("predicates:", domain_dict["predicates"])
    print()
    for key in domain_dict["actions"]:
        print(key+":")
        for k in domain_dict["actions"][key]:
            print(k + ":", domain_dict["actions"][key][k])
        print()

    correctDict = {'name': 'pass-the-ball', 'predicates': {'has-first-letter': ['?n', '?l'], 'has-last-letter': ['?n', '?l'], 'in-room': ['?n', '?r'], 'has-ball': ['?n']}, 'actions': {'laugh': {'parameters': ['?from', '?to', '?letter', '?room'], 'precondition': {'in-room': [(True, ['?from', '?room']), (True, ['?to', '?room'])], 'has-ball': [(True, ['?from'])], 'has-first-letter': [(True, ['?to', '?letter'])], 'has-last-letter': [(True, ['?from', '?letter'])]}, 'effects': {'has-ball': [(False, ['?to']), (False, ['?from'])]}}, 'run': {'parameters': ['?from', '?to', '?letter', '?room'], 'precondition': {'in-room': [(False, ['?from', '?room']), (True, ['?to', '?room'])], 'has-ball': [(True, ['?from'])], 'has-first-letter': [(True, ['?to', '?letter'])], 'has-last-letter': [(True, ['?from', '?letter'])]}, 'effects': {'has-ball': [(True, ['?to']), (False, ['?from'])], 'in-room': [(True, ['?from', '?room'])]}}, 'pass': {'parameters': ['?from', '?to', '?letter', '?room'], 'precondition': {'in-room': [(True, ['?from', '?room']), (True, ['?to', '?room'])], 'has-ball': [(True, ['?from'])], 'has-first-letter': [(True, ['?to', '?letter'])], 'has-last-letter': [(True, ['?from', '?letter'])]}, 'effects': {'has-ball': [(True, ['?to']), (False, ['?from'])]}}, 'move': {'parameters': ['?from', '?to', '?person'], 'precondition': {'in-room': [(True, ['?person', '?from'])]}, 'effects': {'in-room': [(True, ['?person', '?to']), (False, ['?person', '?from'])], 'has-ball': [(True, ['?to'])]}}}}
    print("TEST")
    print("Dictionaries Equal:", domain_dict == correctDict)


    
    
    # actions = {name: {'parameters': [(), ()], 'precondition': [(condition, false/true), (), ()], 'effect':[(), ()]}}
    # domain_dict = {domain: 'domain name', 
    #                predicates: {has-first-letter: [n, l], in-room: [n, r]}, 
    #                actions:{pass:{paramters:[?x, ?y, ?room], 
    #                         precondition:{'in-room':[[?x, ?room], [?y, ?room2]], 'has-ball':[[?y]]}, 
    #                         effect:[(True, 'in-room', ['?y', '?room'), (False, 'has-ball', '?x')]])]}} }
    # in-room:[(True, [?x, ?y]), (False, [?z, ?y])]


