from util import is_var

class Predicate(object):
    """Represents a predicate in our problem definition or a domain file

    Attributes:
        name (str): the name of the predicate
        args (triple): the arguments of the predicate
        value (boolean): false represents 'not'
    """
    def __init__(self, name, args, value=None):
        """Constructor for Fact setting up useful flags and generating appropriate statement

        Args:
            name (str): The name of the predicate
            args (of arguements): The variable arguments or the actual arguments of the predicate.
        """
        super(Predicate, self).__init__()
        
        self.name = name
        self.args = [t if isinstance(t, Term) else Term(t) for t in args]
        
        # self.name = name # 'in-room'
        # self.args = args # ['noah', 'room1']
        self.value = value # True

        

    def __repr__(self):
        """Define internal string representation
        """
        return '(PREDICATE: {!r}, {!r}, {!r})'.format(
                self.name, self.args, self.value)

    def __str__(self):
        """Define external representation when printed
        """
        return '(PREDICATE: {!r}, {!r}, {!r})'.format(
                self.name, self.args, self.value)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return isinstance(other, Predicate) and self.name == other.name and self.args == other.args and other.value == self.value

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Action(object):
    """Represents an action from our domain file

    Attributes:
        name (str): the name of the action to be taken
        parameters (list of variables): the parameters for the action.
        precondition (list of Predicates): the preconditions of an action (LHS of a rule almost)
        effect (list of Predicates): the effect of the action (RHS of a rule almost)
    """
    def __init__(self, name, parameters, precondition, effect):
        """

        Args:
            name (str): the name of the action to be taken
            parameters (list of variables): the parameters for the action.
            precondition (list of Predicates): the preconditions of an action (LHS of a rule almost)
            effect (list of Predicates): the effect of the action (RHS of a rule almost)
        """
        super(Action, self).__init__()
        self.name = name
        self.parameters = parameters
        self.precondition = precondition
        self.effect = effect

    def __repr__(self):
        """Define internal string representation
        """
        return '(ACTION: Name: {!r}, Parameters: {!r}, Precondition: {!r}, Effect: {!r})'.format(
                self.name, self.parameters, self.precondition,
                self.effect)

    def __str__(self):
        """Define external representation when printed
        """
        return '(ACTION: Name: {!r}, Parameters: {!r}, Precondition: {!r}, Effect: {!r})'.format(
                self.name, self.parameters, self.precondition,
                self.effect)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        is_action = isinstance(other, Action)
        return is_action and self.name == other.name and self.rhs == other.rhs

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

# class Statement(object):
#     """

#     Attributes:
#         terms (listof Term): List of terms (Variable or Constant) in the
#             statement, e.g. 'Nosliw' or '?d'
#         predicate (str): The predicate of the statement, e.g. isa, hero, needs
#     """
#     def __init__(self, statement_list=[]):
#         """Constructor for Statements with optional list of Statements that are
#             converted to appropriate terms (and one predicate)

#         Args:
#             statement_list (mostly listof str|Term, first element is str): The element at
#                 index 0 is the predicate of the statement (a str) while the rest of
#                 the list is either instantiated Terms or strings to be passed to the
#                 Term constructor
#         """
#         super(Statement, self).__init__()
#         self.terms = []
#         self.predicate = ""

#         if statement_list:
#             self.predicate = statement_list[0]
#             self.terms = [t if isinstance(t, Term) else Term(t) for t in statement_list[1:]]

#     def __repr__(self):
#         """Define internal string representation
#         """
#         return 'Statement({!r}, {!r})'.format(self.predicate, self.terms)

#     def __str__(self):
#         """Define external representation when printed
#         """
#         return "(" + self.predicate + " " + ' '.join((str(t) for t in self.terms)) + ")"

#     def __eq__(self, other):
#         """Define behavior of == when applied to this object
#         """
#         if self.predicate != other.predicate:
#             return False

#         for self_term, other_term in zip(self.terms, other.terms):
#             if self_term != other_term:
#                 return False

#         return True

#     def __ne__(self, other):
#         """Define behavior of != when applied to this object
#         """
#         return not self == other

class Term(object):
    """Represents a term (a Variable or Constant) in our knowledge base. Can
        sorta be thought of as a super class of Variable and Constant, though
        there is no inheritance implemented in the code.

    Attributes:
        term (Variable|Constant): The Variable or Constant that this term holds (represents)
    """
    def __init__(self, term):
        """Constructor for Term which converts term to appropriate form

        Args:
            term (Variable|Constant|string): Either an instantiated Variable or
                Constant, or a string to be passed to the appropriate constructor
        """
        super(Term, self).__init__()
        is_var_or_const = isinstance(term, Variable) or isinstance(term, Constant)
        self.term = term if is_var_or_const else (Variable(term) if is_var(term) else Constant(term))

    def __repr__(self):
        """Define internal string representation
        """
        return 'Term({!r})'.format(self.term)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.term)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.term.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Variable(object):
    """Represents a variable used in statements

    Attributes:
        element (str): The name of the variable, e.g. '?x'
    """
    def __init__(self, element):
        """Constructor for Variable

        Args:
            element (str): The name of the variable, e.g. '?x'
        """
        super(Variable, self).__init__()
        self.element = element

    def __repr__(self):
        """Define internal string representation
        """
        return 'Variable({!r})'.format(self.element)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.element)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.term.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Constant(object):
    """Represents a constant used in statements

    Attributes:
        element (str): The value of the constant, e.g. 'Nosliw'
    """
    def __init__(self, element):
        """Constructor for Constant

        Args:
            element (str): The value of the constant, e.g. 'Nosliw'
        """
        super(Constant, self).__init__()
        self.element = element

    def __repr__(self):
        """Define internal string representation
        """
        return 'Constant({!r})'.format(self.element)

    def __str__(self):
        """Define external representation when printed
        """
        return str(self.element)

    def __eq__(self, other):
        """Define behavior of == when applied to this object
        """
        return (self is other
            or isinstance(other, Term) and self.term.element == other.term.element
            or ((isinstance(other, Variable) or isinstance(other, Constant))
                and self.element == other.element))

    def __ne__(self, other):
        """Define behavior of != when applied to this object
        """
        return not self == other

class Binding(object):
    """Represents a binding of a constant to a variable, e.g. 'Nosliw' might be
        bound to'?d'

    Attributes:
        variable (Variable): The name of the variable associated with this binding
        constant (Constant): The value of the variable
    """
    def __init__(self, variable, constant):
        """Constructor for Binding

        Args:
            variable (Variable): The name of the variable associated with this binding
            constant (Constant): The value of the variable
        """
        super(Binding, self).__init__()
        self.variable = variable
        self.constant = constant

    def __repr__(self):
        """Define internal string representation
        """
        return 'Binding({!r}, {!r})'.format(self.variable, self.constant)

    def __str__(self):
        """Define external representation when printed
        """
        return self.variable.term.element.upper() + " : " + self.constant.term.element

class Bindings(object):
    """Represents Binding(s) used while matching two statements

    Attributes:
        bindings (listof Bindings): bindings involved in match
        bindings_dict (dictof Bindings): bindings involved in match where key is
            bound variable and value is bound value,
            e.g. some_bindings.bindings_dict['?d'] => 'Nosliw'
    """
    def __init__(self):
        """Constructor for Bindings creating initially empty instance
        """
        self.bindings = []
        self.bindings_dict = {}

    def __repr__(self):
        """Define internal string representation
        """
        return 'Bindings({!r}, {!r})'.format(self.bindings_dict, self.bindings)

    def __str__(self):
        """Define external representation when printed
        """
        if self.bindings == []:
            return "No bindings"
        return ", ".join(((str(binding) + " : " + str(self.bindings_dict[binding])) for binding in self.bindings_dict))

    def __getitem__(self,key):
        """Define behavior for indexing, e.g. random_bindings[key] returns
            random_bindings.bindings_dict[key] when the dictionary is not empty
            and the key exists, otherwise None
        """
        return (self.bindings_dict[key] 
                if (self.bindings_dict and key in self.bindings_dict)
                else None)

    def add_binding(self, variable, value):
        """Add a binding from a variable to a value

        Args:
            variable (Variable): the variable to bind to
            value (Constant): the value to bind to the variable
        """
        self.bindings_dict[variable.element] = value.element
        self.bindings.append(Binding(variable, value))

    def bound_to(self, variable):
        """Check if variable is bound. If so return value bound to it, else False.

        Args:
            variable (Variable): variable to check for binding

        Returns:
            Variable|Constant|False: returns bound term if variable is bound else False
        """
        if variable.element in self.bindings_dict.keys():
            value = self.bindings_dict[variable.element]
            if value:
                return Variable(value) if is_var(value) else Constant(value)

        return False

    def test_and_bind(self, variable_term, value_term):
        """Check if variable_term already bound. If so return whether or not passed
            in value_term matches bound value. If not, add binding between
            variable_terma and value_term and return True.

        Args:
            value_term (Term): value to maybe bind
            variable_term (Term): variable to maybe bind to
        
        Returns:
            bool: if variable bound returns whether or not bound value matches value_term,
                else True
        """
        bound = self.bound_to(variable_term.term)
        if bound:
            return value_term.term == bound
            
        self.add_binding(variable_term.term, value_term.term)
        return True


class ListOfBindings(object):
    """Container for multiple Bindings

        Attributes:
            list_of_bindings (listof Bindings): collects Bindings
    """
    def __init__(self):
        """Constructor for ListOfBindings
        """
        super(ListOfBindings, self).__init__()
        self.list_of_bindings = []

    def __repr__(self):
        """Define internal string representation
        """
        return 'ListOfBindings({!r})'.format(self.list_of_bindings)

    def __str__(self):
        """Define external representation when printed
        """
        string = ""
        for binding, associated_fact_rules in self.list_of_bindings:
            string += "Bindings for Predicates and Terms: " + str(binding) + "\n"
        return string

    def __len__(self):
        """Define behavior of len, when called on this class, 
            e.g. len(ListOfBindings([])) == 0
        """
        return len(self.list_of_bindings)

    def __getitem__(self,key):
        """Define behavior for indexing, e.g. random_list_of_bindings[i] returns
            random_list_of_bindings[i][0]
        """
        return self.list_of_bindings[key][0]

    def add_bindings(self, bindings, facts_rules=[]):
        """Add given bindings to list of Bindings along with associated rules or facts

            Args:            
                bindings (Bindings): bindings to add
                facts_rules (listof Fact|Rule): rules or facts associated with bindings

            Returns:
                Nothing
        """
        self.list_of_bindings.append((bindings, facts_rules))
