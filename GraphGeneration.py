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

        bindings_list = get_bindings(filtered_predicates, precondition)

        match_conditions(precondition, bindings_list)



def get_bindings(predicates, precondition, bindings_list=[]):
    total_list = []
    for condition in precondition:
        bindings_list = ask(condition, predicates)
        if bindings_list != False:
            total_list.append(bindings_list)
            print()
            print(condition.name)
            print(bindings_list)
            print()
        else:
            return False

    return total_list

def match_conditions(precondition, bindings_list):
    if len(bindings_list) == 0:
        return False            #False means no bindings

    for binding in bindings_list[0]:
        print(binding)

        
# def match_condition_recursive(precondition, bindings_list):

#     pass
    
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

