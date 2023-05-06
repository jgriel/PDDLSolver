import itertools
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

    possible_actions = get_possible_actions(objects, state, actions)

    state_list = []

    combined_list = []

    for key in possible_actions:
        for action in possible_actions[key]:
            combined_list.append(action)
    
    new_states = generate_new_states(state, combined_list)


    # generate_new_states()

    return new_states



#Get Binding Methods
def get_possible_actions(objects, predicates, actions):
    action_dict = dict()
    
    for act in actions:
        # print("\n", act.name)

        filtered_predicates = filter_predicates(predicates, act.precondition)

        # filtered_objects = filter_objects(objects, filtered_predicates)

        possible_preconditions = match_conditions(objects, act.parameters, filtered_predicates, act)

        bound_effects = instantiate_effects(possible_preconditions, act)
        
        # print(bound_effects)

        # for i in range(len(possible_preconditions)): #precondition in possible_preconditions:
        #     print("\n", action_params_to_string(possible_preconditions[i][0], act))
        #     print(effect_to_string(possible_preconditions[i][1]))
        #     print(effect_to_string(bound_effects[i][1]))

        action_dict[act.name] = bound_effects

    return action_dict

def match_conditions(objects, parameters, predicates, action):

    precondition = action.precondition

    possible_objects = list(itertools.permutations(objects, len(parameters)))
    possible_matches = []
    for combination in possible_objects:
        bindings = Bindings()
        for i in range(len(parameters)):
            # print(parameters[i], combination[i])
            bindings.add_binding(parameters[i].term, combination[i].term)
        matched_precondition = []
        invalid = False
        for predicate in precondition:
            condition = instantiate(predicate, bindings, predicate.value)
            contained = ask(condition, predicates)
            if (condition.value and contained) or ((not condition.value) and (not contained)):
                matched_precondition.append(condition)
            else:
                invalid = True
                break
        if not invalid:
            possible_matches.append((bindings, matched_precondition))

        # possible_bindings.add_bindings(bindings)


    return possible_matches

def ask(condition, predicates):
    return condition in predicates


# Effect Methods
def instantiate_effects(bindings, action):
    effect = action.effect
    new_effect_list = []
    for binding in bindings:
        new_effect = []
        for predicate in effect:
            condition = instantiate(predicate, binding[0], predicate.value)
            new_effect.append(condition)
        new_effect_list.append((action_params_to_string(binding[0], action), new_effect))
    
    return new_effect_list

def generate_new_states(state, effects):
    # print(state)
    state_list = []
    for effect in effects:
        new_state = copy_state(state)
        # print()
        # print(effect[1])
        for predicate in effect[1]:
            # print(predicate)
            if predicate.value and (not (predicate in state)):
                new_state.append(predicate)
            elif (not predicate.value) and (get_predicate(predicate, state)):
                predicate.value = not predicate.value
                # print(predicate)
                if predicate in new_state:
                    new_state.remove(predicate)
                predicate.value = not predicate.value
        
        state_list.append((effect[0], new_state))

    return state_list


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

def filter_objects(objects, predicates):
    filtered_objects = []
    for ob in objects:
        for predicate in predicates:
            if ob.term not in predicate.args:
                filtered_objects.append(ob)

    return filtered_objects

def get_predicate(predicate, predicates):
    for pred in predicates:
        if pred.name == predicate.name and pred.args == predicate.args:
           return pred
    return False

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

def action_params_to_string(bindings, action):
    string = "(" + action.name
    for param in action.parameters:
        string += " " + bindings.bindings_dict[param.term.element]
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
