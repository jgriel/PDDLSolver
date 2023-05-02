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
            print("KEY:", key)
            for possibility in possible_actions[key]:
                print("PARAMETERS: ", possibility)
                print()
                new_state = compute_action(possibility, get_domain_action(actions, key), state)
            print()





    return

def get_domain_action(actions, key):
    for action in actions:
        if action.name == key:
            return action
    return None

def get_possible_actions(predicates, actions):

    action_dict = dict()
    
    for act in actions:
        print(act.name)
        precondition = act.precondition

        filtered_predicates = filter_predicates(predicates, precondition)

        bindings_list = get_bindings(filtered_predicates, precondition)

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
        print("IN GET BINDINGS: ", bindings_list)

    # print(total_list)
    
    return total_list

def match_conditions(precondition, bindings_list, predicates):
    # print("PRECONDITION:" , precondition)
    if len(bindings_list) == 1:
        new_preconditions = []
        for binding in bindings_list[0]:
            last_condition = instantiate(precondition[0], binding, precondition[0].value)
            contained = get_predicate(last_condition, predicates)

            if not contained:
                valid = (last_condition.value == False)
            else:
                valid = (contained.value == last_condition.value)

            if valid and not contains_variables(last_condition):
                    new_preconditions.append([last_condition])
        if new_preconditions != []: 
            return new_preconditions
        else:
            return False         #False means no bindings
    possible_conditions = []
    for binding in bindings_list[0]:
        first_precondition = instantiate(precondition[0], binding, precondition[0].value)
        contained = get_predicate(first_precondition, predicates)
        if not contained:
            valid = (first_precondition.value == False)
        else:
            valid = (contained.value == first_precondition.value)
        if valid:
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

def get_predicate(predicate, predicates):
    for pred in predicates:
        if pred.name == predicate.name and pred.args == predicate.args:
           return pred
    return False
        
def contains_variables(condition):
    for term in condition.args:
        if is_var(term):
            return True
    return False

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

