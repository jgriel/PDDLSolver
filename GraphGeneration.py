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
    predicates = domain['predicates']

    currState = state['state']


    getPossible(predicates, actions)



def getPossible(predicates, actions):
    
    for act in actions:
        parameters = act['parameters']
        preconditions = act['precondition']
        effects = act['effect']

        possible_predicates = []

        for cond in preconditions:

            for pred in predicates:
                match(cond, pred)




def instantiate(parameters, action):
    pass


def ask(predicates, precondition):

    bindings_list = ListOfBindings()
    for predicate in predicates:
        bindings = match(predicate.args, precondition.args)

        bindings_list.add_bindings(bindings)

    return bindings_list if bindings_list.list_of_bindings else []
    

