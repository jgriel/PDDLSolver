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


    get_possible_parameters(state, actions)





    return



def get_possible_parameters(predicates, actions):
    
    for act in actions:
        print(act.name)
        parameters = act.parameters
        precondition = act.precondition
        effect = act.effect

        filtered_predicates = filter_predicates(predicates, precondition)

        filtered_objects = filter_objects(filtered_predicates)
        possible_parameters = generate_combinations(filtered_objects, parameters)
        possible_actions = []
        print(possible_parameters)
        print()

def generate_combinations(objects, parameters):
    print(objects)
    combinations = list(itertools.permutations(objects, len(parameters)))
    for combo in combinations:
        string = "["
        for ob in combo:
            string += str(ob) + ", "
        string = string[:-2] + "]"
        print(string)
    return combinations

def iterate_conditions(objects, predicates, precondition):            

    pass



def infer_precondition(predicates, precondition):
    firstCondition = precondition[0]
    bindings = ask(firstCondition, predicates)

    



def ask(condition, predicates):
    
    bindingsList = ListOfBindings()
    for pred in predicates:
        binding = match(pred, condition)

        if binding != False:
            bindingsList.add_bindings(binding)

    return bindingsList



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

