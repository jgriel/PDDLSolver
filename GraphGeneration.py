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


    possible_actions = get_possible_actions(state, actions)

    for key in possible_actions:
        for possibility in possible_actions[key]:
            new_state = compute_action(possibility, actions[key], state)





    return



def get_possible_actions(predicates, actions):

    action_dict = dict
    
    for act in actions:
        # print(act.name)
        parameters = act.parameters
        precondition = act.precondition
        effect = act.effect

        filtered_predicates = filter_predicates(predicates, precondition)

        bindings_list = get_bindings(filtered_predicates, precondition)

        # match_conditions(precondition, bindings_list)
        matched = match_conditions(precondition, bindings_list, predicates)
            
        # for match in matched:
        #     print(match)
        #     print()
        action_dict[act.name] = matched

    return action_dict



def get_bindings(predicates, precondition, bindings_list=[]):
    total_list = []
    for condition in precondition:
        bindings_list = ask(condition, predicates)
        if bindings_list != False:
            total_list.append(bindings_list)
            # print()
            # print(condition.name)
            # print(bindings_list)
            # print()
        else:
            return False

    return total_list

def match_conditions(precondition, bindings_list, predicates):
    # print("PRECONDITION:" , precondition)
    if len(bindings_list) == 1:
        new_preconditions = []
        for binding in bindings_list[0]:
            last_condition = instantiate(precondition[0], binding, precondition[0].value)
            if last_condition in predicates:
                if not contains_variables(last_condition):
                    new_preconditions.append([last_condition])
        if new_preconditions != []: 
            return new_preconditions
        else:
            return False         #False means no bindings
    possible_conditions = []
    for binding in bindings_list[0]:
        first_precondition = instantiate(precondition[0], binding, precondition[0].value)
        if first_precondition in predicates:
            new_precondition = []
            for condition in precondition[1:]:
                new_precondition.append(instantiate(condition, binding, condition.value))
            
            bound_precondition_list = match_conditions(new_precondition, bindings_list[1:], predicates)
            
            if bound_precondition_list != False:
                for bound_precondition in bound_precondition_list:
                    # print(bound_precondition)
                    bound_precondition.insert(0, first_precondition)
                    if bound_precondition not in possible_conditions:
                        possible_conditions.append(bound_precondition)
    
    return possible_conditions
        
def contains_variables(condition):
    for term in condition.args:
        if is_var(term):
            return True
    return False
        
# def match_condition_recursive(precondition, bindings_list):

#     pass
    
def get_param_index(param, parameters):
    return parameters.index(param)

def contains_predicate(predicates, predicate):
    return predicate in predicates

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

def compute_action(parameters, action, state):
    pass

