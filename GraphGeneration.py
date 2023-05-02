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

        infer_precondition(parameters, filtered_objects, filtered_predicates, precondition)
        # possible_parameters = itertools.permutations(filtered_objects, parameters)
        possible_actions = []

def infer_precondition(predicates, precondition, bindings_list=[]):
    firstCondition = precondition[0]

    bindings_list = ask(firstCondition, predicates)

    if bindings_list == False:
        return False
    for bindings in bindings_list:
        if len(precondition) != 1:
            newCondition = []
            for condition in precondition[1:]:
                newCondition.append(instantiate(condition, bindings)) 
            bindings_list = infer_precondition(predicates, newCondition)
        


    
def get_param_index(param, parameters):
    return parameters.index(param)
    
def contains_binding():
    pass


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



def bind_conditions(paramteters, bindings):
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

def filter_objects(predicates):
    objects = []
    for predicate in predicates:
        for arg in predicate.args:
            if arg not in objects:
                objects.append(arg)
    return objects

def computeAction(parameters, action, state):
    pass

