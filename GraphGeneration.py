
def expand(state, domain):

    """Finds all the possible actions that can be taken 
        from the current state.

    Args:
        state: state Dictionary containing the information of the state. 
        domain: The representation of the domain file with all of the actions and predicates.

    Returns:
        list of states that are able to be reached from the current state
        with one action taken

    """

    actions = domain['actions']
    predicates = domain['predicates']

def match(predicates, actions): 
    
    for act in actions:
        parameters = act['parameters']
        preconditions = act['precondition']
        effects = act['effect']


        for pred in predicates:
            pass


    pass


def match_recursive(predicates, actions):
    pass