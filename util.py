import logical_classes as lc

def is_var(var):
    """Check whether an element is a variable (either instance of Variable, 
        instance of Term (where .term is a Variable) or a string starting with 
        `'?'`, e.g. `'?d'`)

    Args:
        var (any): value to check

    Returns:
        bool
    """
    if type(var) == str:
        return var[0] == "?"
    if isinstance(var, lc.Term):
        return isinstance(var.term, lc.Variable)

    return isinstance(var, lc.Variable)

def match(pred1, pred2, bindings=None):
    """Match two statements and return the associated bindings or False if there
        is no binding

    Args:
        pred1 (Statement): statement to match with pred2
        pred2 (Statement): statement to match with pred1
        bindings (Bindings|None): already associated bindings

    Returns:
        Bindings|False: either associated bindings or no match found
    """
    if len(pred1.args) != len(pred2.args) or pred1.name != pred2.name:
        return False
    if not bindings:
        bindings = lc.Bindings()
    return match_recursive(pred1.args, pred2.args, bindings)

def match_recursive(args1, args2, bindings):  # recursive...
    """Recursive helper for match

    Args:
        args1 (listof Term): terms to match with args2
        args2 (listof Term): terms to match with args1
        bindings (Bindings): already associated bindings

    Returns:
        Bindings|False: either associated bindings or no match found
    """
    if len(args1) == 0:
        return bindings
    if is_var(args1[0]):
        if not bindings.test_and_bind(args1[0], args2[0]):
            return False
    elif is_var(args2[0]):
        if not bindings.test_and_bind(args2[0], args1[0]):
            return False
    elif args1[0] != args2[0]:
        return False
    return match_recursive(args1[1:], args2[1:], bindings)

def instantiate(statement, bindings):
    """Generate Statement from given statement and bindings. Constructed statement
        has bound values for variables if they exist in bindings.

    Args:
        statement (Statement): statement to generate new statement from
        bindings (Bindings): bindings to substitute into statement
    """
    def handle_term(term):
        if is_var(term):
            bound_value = bindings.bound_to(term.term)
            return lc.Term(bound_value) if bound_value else term
        else:
            return term

    new_terms = [handle_term(t) for t in statement.args]
    return lc.Predicate([statement.predicate] + new_terms)

def predq(element):
    """Check if element is a fact

    Args:
        element (any): element to check

    Returns:
        bool
    """
    return isinstance(element, lc.Predicate)

def acteq(element):
    """Check if element is a rule

    Args:
        element (any): element to check

    Returns:
        bool
    """
    return isinstance(element, lc.Action)

def printv(message, level, verbose, data=[]):
    """Prints given message formatted with data if passed in verbose flag is greater than level

    Args:
        message (str): message to print, if format string data should have values
            to format with
        level (int): value of verbose required to print
        verbose (int): value of verbose flag
        data (listof any): optional data to format message with
    """
    if verbose > level:
        print(message.format(*data) if data else message)