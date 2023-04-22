import sys, regex as re

if __name__ == "__main__":
    domain_filename = sys.argv[1]

    domain_file = open(domain_filename, 'r')
    
    # get domain file
    domain_text = ''
    for line in domain_file:
        domain_text += line.strip()
    domain_text = domain_text[1:-1]

    # get domain name
    domain_name = re.findall('domain.*?\\)', domain_text)[0][6:-1].strip()
    print("Domain:", domain_name)
    print()

    #get predicates
    predicates_list = re.findall(':predicates.*?\\)\\)', domain_text)[0]
    predicates_list = re.findall('\\(.*?\\)', predicates_list)
    predicates_dict = {}
    for i in range(len(predicates_list)):
        predicate = predicates_list[i][1:-1].split()
        predicates_dict[predicate[0]] = predicate[1:]
    print("Predicates:", predicates_dict)
    print()

    #get actions
    # true = (condition)
    # false = not (conidition)
    actions_in_middle_of_file = re.findall(':action.*?\\(:', domain_text, overlapped=True)
    print("Actions:", actions_in_middle_of_file)
    print()

    reversed_domain_text = domain_text[::-1]
    print(reversed_domain_text)
    print()
    actions_end_of_file = re.findall('.*?noitca:', reversed_domain_text)
    print(actions_end_of_file[0][::-1])
    print()
    # for i in range(len(actions)):
        # print("Action:", actions[i])
    
    # actions = {'parameters': [(), ()], 'precondition': [(condition, false/true), (), ()], 'effect':[(), ()]}
    # {domain: '', predicates: {has-first-letter: [n, l], in-room: [n, r]}, actions:{pass:{paramters:[], precondition:[], effect:[]} } }