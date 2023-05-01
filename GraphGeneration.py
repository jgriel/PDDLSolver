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

        # infer_precondition(filtered_predicates, precondition)



    # print(possible_parameters)

def infer_precondition(predicates, precondition):
    firstCondition = precondition[0]
    possible_bindings = ask(firstCondition, predicates)
    possible_new_conditions = []
    if possible_bindings != False:
        for binding in possible_bindings:
                newCondition = []
                for condition in precondition[1:]:
                    print("HERE")
                    newCondition.append(instantiate(condition, binding))
                    print("HERE2")
                recursive_conditions = infer_precondition(predicates, newCondition[1:])
                
                if not recursive_conditions:
                    newCondition = [instantiate(firstCondition, binding)]
                    for recur_cond in recursive_conditions:
                        newCondition.append(recur_cond)
                else:
                    return False
        possible_new_conditions.append(newCondition)
    else:
        return False



def ask(condition, predicates):
    
    bindingsList = ListOfBindings()
    predicateList = []
    for pred in predicates:
        binding = match(pred, condition)

        if binding != False:
            bindingsList.add_bindings(binding)
            predicateList.append(pred)

    return (predicateList, bindingsList)



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



def computeAction(parameters, action, state):
    pass

