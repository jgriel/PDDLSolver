import sys, re

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

    #get predicates
    predicates = re.findall(':predicates.*?\\)\\)', domain_text)[0]
    predicates = re.findall('\\(.*?\\)', predicates)
    for i in range(len(predicates)):
        predicates[i] = predicates[i][1:-1]
    print("Predicates:", predicates)

    #get actions
    actions = re.findall(':actions.*?\\)\\)', domain_text)
    print("Actions:", actions)
    
    # {domain: '', predicates: {has-first-letter: [n, l], in-room: [n, r]}, actions:{pass:{paramters:[], precondition:[], effect:[]} } }