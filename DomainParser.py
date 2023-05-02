import sys, regex as re
import logical_classes as lc

def parse_file(domain_filename):
    domain_file = open(domain_filename, 'r')
    
    # get domain file text
    domain_text = ''
    for line in domain_file:
        if (len(line.strip()) > 0 and line.strip()[0] != ";"):
            domain_text += line.strip()
    domain_text = domain_text[1:-1]
    
    return {'name':parse_domain_name(domain_text), 'predicates':parse_predicates(domain_text), 'actions':parse_actions(domain_text)}


def parse_domain_name(domain_text):
    # get domain name
    return re.findall('domain.*?\\)', domain_text)[0][6:-1].strip()


def parse_predicates(domain_text):
    #get predicates
    predicates_list = re.findall(':predicates.*?\\)\\)', domain_text)[0]
    predicates_list = re.findall('\\(.*?\\)', predicates_list)
    predicates = []
    for i in range(len(predicates_list)):
        predicate = predicates_list[i][1:-1].split()
        predicates.append(lc.Predicate(predicate[0], predicate[1:], None))

    return predicates


'''
This function will parse the preconditions or effects of an action
The format of the precondition and effect are identical so the code is the same besides the regex
Parameters: string of the action block, whether it should parse the effect or precondition
'''
def parse_precondition_effect(action, precondition_effect):
    # different regex for effect and precondition
    if (precondition_effect == "effect"):
        e_p = re.findall(':'+ precondition_effect + '.*?\\(.*:', action)
    else:
        e_p = re.findall(':'+ precondition_effect + '.*?\\.*:', action)
    # if the action is at the end of the file, the regex should be different because there is no ':'

    if (e_p == []):
        e_p = re.findall(':'+ precondition_effect + '.*', action)

    # find all individual conditions
    e_p = re.findall('\\(.*?\\)', e_p[0])

    e_p_list = []
    for i in range(len(e_p)):
        single_e_p = e_p[i]

        if (single_e_p[1:].strip()[:3] == "and"):
            single_e_p = single_e_p[1:].strip()[3:].strip() 
        
        # check if the effect has a not
        not_present = (single_e_p[1:].strip()[:3] == "not")
        if (not_present):
            single_e_p = single_e_p[4:].strip()[1:-1].strip()
            single_e_p = single_e_p.split()
            e_p_name = single_e_p[0]
            
            single_e_p = lc.Predicate(e_p_name, single_e_p[1:], False)
        else:
            single_e_p = single_e_p[1:-1].strip().split()
            e_p_name = single_e_p[0]

            single_e_p = lc.Predicate(e_p_name, single_e_p[1:], True)
        
        e_p_list.append(single_e_p)

    return e_p_list


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

    action_list = []
    for i in range(len(actions)):
        # name
        action_name = re.findall(':action.*?:', actions[i])
        action_name = action_name[0][7:-1].strip()

        # paramtersof
        parameters = re.findall(':parameters.*?:', actions[i])
        params = parameters[0][11:-2].strip()[1:].split()
        parameters = []
        for param in params:
            parameters.append(lc.Term(param))

        # preconditions
        precondition_list = parse_precondition_effect(actions[i], "precondition")

        # effects
        effect_list = parse_precondition_effect(actions[i], "effect")
        
        
        action = lc.Action(action_name, parameters, precondition_list, effect_list)
        action_list.append(action)
       
    return action_list


if __name__ == "__main__":
    domain_filename = sys.argv[1]

    domain_dict = parse_file(domain_filename)
    print(domain_dict)
    