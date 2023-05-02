from util import *
from logical_classes import *
import itertools


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


    get_possible_actions(state, actions)





    return



def get_possible_actions(predicates, actions):
    
    for act in actions:
        print(act.name)
        parameters = act.parameters
        precondition = act.precondition
        effect = act.effect

        filtered_predicates = filter_predicates(predicates, precondition)

        filtered_objects = filter_objects(filtered_predicates)

        infer_precondition(filtered_predicates, precondition)
        # possible_parameters = itertools.permutations(filtered_objects, parameters)
        possible_actions = []

def infer_precondition(predicates, precondition, bindings_list=[]):
    total_list = []
    for condition in precondition:
        bindings_list = ask(condition, predicates)
        if bindings_list != False:
            total_list.append(bindings_list)
            print(condition.name)
            print(bindings_list)
            print()
        else:
            return False
    firstCondition = precondition[0]
    

        

    
def get_param_index(param, parameters):
    return parameters.index(param)

def ask(condition, predicates):
    
    bindingsList = ListOfBindings()
    for pred in predicates:
        binding = match(pred, condition)

        if binding != False:
            bindingsList.add_bindings(binding)

    if bindingsList.list_of_bindings != []:
        return bindingsList
    else:
        return False


def filter_predicates(predicates, precondition):
    names = []
    for condition in precondition:
        names.append(condition.name)
    
    filtered = []
    for predicate in predicates:
        if predicate.name in names:
            filtered.append(predicate)

    return filtered

def filter_objects(predicates):
    objects = []
    for predicate in predicates:
        for arg in predicate.args:
            if arg not in objects:
                objects.append(arg)
    return objects

def computeAction(parameters, action, state):
    pass

