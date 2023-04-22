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
        print("Action:", actions[i])
        print()

        action_name = re.findall(':action.*?:', actions[i])
        action_name = action_name[0][7:-1].strip()
        # print("ACTION NAME", action_name)
        # print()

        parameters = re.findall(':parameters.*?:', actions[i])
        parameters = parameters[0][11:-2].strip()[1:].split()
        # print("PARAMETERS:", parameters)
        # print()

        precondition = re.findall(':precondition.*?:', actions[i])[0][13:-1].strip()
        precondition = re.findall('\\(.*?\\)', precondition)
        precondition_formatted = []
        for j in range(len(precondition)):
            if (precondition[j][1:].strip()[:3] == "and"):
                precondition_formatted.append(precondition[j][1:-1][3:].strip()[1:])
            else:
                precondition_formatted.append(precondition[j][1:-1].strip())
        
        precondition_dict = {}
        for condition in precondition_formatted:
            c = condition.split()
            print("HERE", c)
            if (c[0] in precondition_dict):
                precondition_dict[c[0]].append(c[1:])
            else:
                precondition_dict[c[0]] = [c[1:]]

        print("PRECONDITION:", precondition_dict)
        print()

        effect = re.findall(':effect.*?\\(:', actions[i])
        effect = re.findall('\\(.*?\\)\\)', effect[0])[0][1:-1].strip()
        if (effect[:3] == "and"):
            effect = effect[3:].strip()
        effect = re.findall('\\(.*?\\)', effect)

        effect_list = []
        for i in range(len(effect)):
            single_effect = effect[i][1:-1].strip()
            # check if the effect has a not
            not_present = (single_effect[:3] == "not")

            if (not_present):
                single_effect = single_effect[3:].strip()[1:]
                single_effect = single_effect.split()
                effect_list.append((False, single_effect[0], single_effect[1:]))
            else:
                single_effect = single_effect.split()
                effect_list.append((True, single_effect[0], single_effect[1:]))
        
        action_dict[action_name] = {'parameters':parameters, 'precondition':precondition_dict, 'effects':effect_list}
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
    print("HERE")
    print(domain_dict)


    
    
    # actions = {name: {'parameters': [(), ()], 'precondition': [(condition, false/true), (), ()], 'effect':[(), ()]}}
    # domain_dict = {domain: 'domain name', 
    #                predicates: {has-first-letter: [n, l], in-room: [n, r]}, 
    #                actions:{pass:{paramters:[?x, ?y, ?room], 
    #                         precondition:{'in-room':[[?x, ?room], [?y, ?room2]], 'has-ball':[[?y]]}, 
    #                         effect:[(True, 'in-room', ['?y', '?room'), (False, 'has-ball', '?x')]])]}} }