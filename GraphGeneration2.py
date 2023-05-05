from util import *
from logical_classes import *

def expand(objects, state, domain):

    """Finds all the possible actions that can be taken 
        from the current state.

    Args:
        state: state Dictionary containing the information of the state. 
        domain: The representation of the domain file with all of the actions and predicates.

    Returns:
        list of tuples, that are the action name with the parameters and the state that is reach with
        that action taken

    """
    actions = domain['actions']
    possible_actions = get_possible_actions(state, actions)
    effect_list = []
    for key in possible_actions:
            for possibility in possible_actions[key]:
                # print("possibility:")
                # print(key, effect_to_string(possibility), "\n")
                # print(len(possibility), len(get_domain_action(actions, key).parameters))
                valid = True
                
                for item in possibility:
                    if possibility.count(item) > 1:
                        valid = False
                        break

                if valid:
                    next_effect = compute_effect(possibility, get_domain_action(actions, key))
                    if contains_unbound_parameters(next_effect[0]):
                        additional_effects = compute_additional_effects(objects, next_effect[0][1:], next_effect, get_domain_action(actions, key))
                        for additional_effect in additional_effects:
                            effect_list.append(additional_effect)
                    else:
                        effect_list.append(compute_effect(possibility, get_domain_action(actions, key)))
    
    # for effect in effect_list:
    #     print(action_params_to_string(effect[0]))

    state_list = generate_new_states(state, effect_list)

    # print("ORIGINAL STATE")
    # print(state_to_string(state))
    # print()
    # for state in state_list:
    #     print("NEW STATE:")
    #     print(action_params_to_string(state[0]) + ": \n" + state_to_string(state[1]))
    #     print()      

    # print(len(state_list))
    # print(len(objects))
    return state_list

#Get Binding Methods
def get_possible_actions(predicates, actions):
    action_dict = dict()
    
    for act in actions:
        print("\n", act.name)
        precondition = act.precondition
        filtered_predicates = filter_predicates(predicates, precondition)
        bindings_list = get_bindings(filtered_predicates, precondition)
        # for binding in bindings_list:
        #     print(binding)
        # print()
        matched = match_conditions(precondition, bindings_list, predicates)
        # print(act.name)
        # print(effect_to_string(act.precondition))
        # for match in matched:
        #     print(effect_to_string(match))
        #     print()
        action_dict[act.name] = matched

    print("DONE GET POSSIBLE ACTIONS")
    return action_dict

def get_bindings(predicates, precondition):
    total_list = []
    for condition in precondition:
        bindings_list = ask(condition, predicates)
        if bindings_list != False:
            total_list.append(bindings_list)
            # print()
            # print(condition.name)
            # print(bindings_list)
            # print()

    # print(total_list)
    
    return total_list

def match_conditions(precondition, bindings_list, predicates):
    first_condition = precondition[0]
    if len(bindings_list) == 1:
        new_precondition = []
        if not contains_variables(first_condition):
            return [precondition]
        else:
            for binding in bindings_list[0]:
                first_condition = instantiate(first_condition, binding, first_condition.value)
                new_precondition.append([first_condition])
            return new_precondition
    else:
        possible_conditions = []
        for binding in bindings_list[0]:
            if not contains_variables(precondition):
                new_precondition = []
                first_condition = instantiate(first_condition, binding, precondition.value)
                
            

            
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


# Effect Methods
def compute_effect(parameters, action, bindings = False):
    pass

def compute_additional_effects(objects, parameters, current_effect, action):
    pass


def generate_new_states(state, effects):
    pass


#Helper Methods....
def get_domain_action(actions, key):
    for action in actions:
        if action.name == key:
            return action
    return None

def filter_predicates(predicates, precondition):
    names = []
    for condition in precondition:
        names.append(condition.name)
    
    filtered = []
    for predicate in predicates:
        if predicate.name in names:
            filtered.append(predicate)

    return filtered

def filter_objects(objects, parameters):
    filtered_objects = []
    for ob in objects:
        if ob.term.element not in parameters:
            filtered_objects.append(ob)

    return filtered_objects

def get_predicate(predicate, predicates):
    for pred in predicates:
        if pred.name == predicate.name and pred.args == predicate.args:
           return pred
    return False

def contains_unbound_parameters(parameters):
    unbound_parameters = False
    for term in parameters:
        unbound_parameters = ("?" in term)
        if unbound_parameters:
            break
    return unbound_parameters

def contains_variables(condition):
    # print("\nCondition", condition)
    for term in condition.args:
        if is_var(term):
            return True
    return False

def copy_state(state):
    new_state = []

    for predicate in state:
        new_state.append(predicate)

    return new_state

def state_to_string(state):
    string = ""
    for predicate in state:
        string += predicate_to_string(predicate) + "\n"
    return string

def action_params_to_string(effect):
    string = "(" + str(effect[0])
    for predicate in effect[1:]:
            string += " " + str(predicate)
    return string + ")" 

def effect_to_string(effect):
    string = ""
    for predicate in effect:
        if not predicate.value:
            string += "(not " + predicate_to_string(predicate) + ") "
        else:
            string += predicate_to_string(predicate) + " "
    return string.strip()

def predicate_to_string(predicate):
    string = "(" + predicate.name
    for arg in predicate.args:
            string += " " + arg.term.element
    string += ")"

    return string
