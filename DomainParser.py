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

def parse_conditions(action, effect_precondition):
    e_p = re.findall(':'+ effect_precondition + '.*?\\(.*:', action)
    # print(effect)

    e_p = re.findall('\\(.*?\\)', e_p[0])
    # print(effect)
    # print()

    e_p_dict = {}
    for i in range(len(e_p)):
        single_effect = e_p[i]
        # print(single_effect)

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
    action_mof = re.findall(':action.*?\\(:', domain_text, overlapped=True)
 
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
    
    # print("ACTIONS:", actions)
    # print()

    action_dict = {}
    for i in range(len(actions)):
        action_name = re.findall(':action.*?:', actions[i])
        action_name = action_name[0][7:-1].strip()
        

        parameters = re.findall(':parameters.*?:', actions[i])
        parameters = parameters[0][11:-2].strip()[1:].split()
      
        precondition_dict = parse_conditions(actions[i], "precondition")
        
        effect_dict = parse_conditions(actions[i], "effect")
        
        action_dict[action_name] = {'parameters':parameters, 'precondition':precondition_dict, 'effects':effect_dict}

    return action_dict


def parse_file(file_name):
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
    print(domain_dict)


    
    
    # actions = {name: {'parameters': [(), ()], 'precondition': [(condition, false/true), (), ()], 'effect':[(), ()]}}
    # domain_dict = {domain: 'domain name', 
    #                predicates: {has-first-letter: [n, l], in-room: [n, r]}, 
    #                actions:{pass:{paramters:[?x, ?y, ?room], 
    #                         precondition:{'in-room':[[?x, ?room], [?y, ?room2]], 'has-ball':[[?y]]}, 
    #                         effect:[(True, 'in-room', ['?y', '?room'), (False, 'has-ball', '?x')]])]}} }
    # in-room:[(True, [?x, ?y]), (False, [?z, ?y])]