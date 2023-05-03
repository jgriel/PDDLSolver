from util import *
from logical_classes import *
import itertools


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

    # print(objects)

    effect_list = []
    for key in possible_actions:
            for possibility in possible_actions[key]:
                # print("possibility:")
                # print(possibility, "\n")
                next_effect = compute_effect(possibility, get_domain_action(actions, key))
                if contains_unbound_parameters(next_effect[0]):
                    additional_effects = compute_additional_effects(objects, next_effect[0][1:], next_effect, get_domain_action(actions, key))
                    for additional_effect in additional_effects:
                        effect_list.append(additional_effect)
                else:
                    effect_list.append(compute_effect(possibility, get_domain_action(actions, key)))

    state_list = generate_new_states(state, effect_list)

    print("ORIGINAL STATE")
    print(state_to_string(state))
    print()
    for state in state_list:
        print("NEW STATE:")
        print(action_params_to_string(state[0]) + ": \n" + state_to_string(state[1]))
        print()      

    print(len(state_list))
    print(len(objects))
    return state_list

#Get Binding Methods
def get_possible_actions(predicates, actions):

    action_dict = dict()
    
    for act in actions:
        # print(act.name)
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
    effect = action.effect
    if not bindings:
        bindings = Bindings()

        precondition = action.precondition

        for i in range(len(precondition)):
            for j in range(len(precondition[i].args)):
                # print("PRECONDITION:", precondition[i])
                # print("PARAMETERS:" , parameters[i])
                bindings.add_binding(precondition[i].args[j].term, parameters[i].args[j].term)

        # print("New Action")
        # print("Parameters: ", parameters)
        # print()
        # print("Precondition: ", precondition)
        # print()
        # print("Bindings: ", bindings)
        # print()


        params = action.parameters
        input = [action.name]
        for param in params:
            binding = bindings[param.term.element]
            if binding == None:
                input.append(param.term.element)
            else:
                input.append(bindings[param.term.element])

    new_effect = []
    for predicate in effect:
        new_effect.append(instantiate(predicate, bindings, predicate.value))
    
    # print("General Effect: ", effect)
    # print()
    # print("Computed Effect: ", new_effect)
    # print()

    return (input, new_effect)

def compute_additional_effects(objects, parameters, current_effect, action):
    # print(current_effect)

    filtered_objects = filter_objects(objects, parameters)
    # print()
    # print("PARAMETERS:\n", parameters)
    # print("OBJECTS:\n", filtered_objects)
    # print()
    effect = current_effect[1]
    unbound_parameters = []
    for predicate in effect:
        for term in predicate.args:
            if is_var(term):
                if term not in unbound_parameters:
                    unbound_parameters.append(term)
    if not unbound_parameters:
        return [current_effect]
    else:
        # print()
        # print("Unbound Parameters")
        # print(unbound_parameters)
        # print("Objects:")
        # print(filtered_objects)
        # print()
        possible_bindings = []
        for param in unbound_parameters:
            for ob in filtered_objects:
                # print(ob)
                bindings = Bindings()
                bindings.add_binding(param.term, ob.term)
                possible_bindings.append(bindings)
                # print(binding)
                # print()

        # print()
        # print(possible_bindings)
        # print()
        # print("Objects:\n", filtered_objects)
        # print("\nEffect: \n", effect)
        

        
        new_effects = []
        for binding in possible_bindings:
            # print("BINDING:", binding)
            new_effect = []
            for predicate in effect:
                new_effect.append(instantiate(predicate, binding, predicate.value))
            
            new_input = [action.name]
            for term in parameters:
                bind = binding[term]
                if bind == None:
                    new_input.append(term)
                else:
                    new_input.append(binding[term])
            
            new_effects.append((new_input, new_effect))

        new_new_effects = []
        for possible_effect in new_effects:
            new_new_effect_list = compute_additional_effects(filtered_objects, possible_effect[0][1:], possible_effect, action)
            for new_new_effect in new_new_effect_list:
                new_new_effects.append(new_new_effect)

            



        # print()
        # print(new_effects)
        # print()
        
        return new_new_effects


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
