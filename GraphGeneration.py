from util import *
from logical_classes import *


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
    newState = state


    get_possible_parameters(state, actions)





    return



def get_possible_parameters(predicates, actions):
    
    for act in actions:
        parameters = act.parameters
        precondition = act.precondition
        effect = act.effect

        filtered_predicates = filter_predicates(predicates, precondition)

        possible_parameters = []

        for condition in precondition:
            possible_bindings = ask(condition, filtered_predicates)
            possible_parameters.append(possible_bindings)



    print(possible_parameters)

def ask(condition, predicates):
    
    bindingsList = ListOfBindings()
    
    for pred in predicates:
        binding = match(pred, condition)

        if binding != False:
            bindingsList.add_bindings(binding)

    return bindingsList  



def bind_parameters(paramteters, bindings):
    pass



def filter_predicates(predicates, precondition):
    names = []
    for condition in precondition:
        names.append(condition.name)
    
    filtered = []
    for predicate in predicates:
        if predicate.name in names:
            filtered.append(predicate)

    return filtered



def computeAction(parameters, action, state):
    pass

