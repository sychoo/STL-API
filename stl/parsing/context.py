# Simon Chu
# Sun Jan 10 21:10:06 EST 2021

class Eval_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the value associated with it

    Attributes:
        context: {"var_id": evaluated_var_value, ...}
        use id string for the key of the dictionary to boost the look up speed and efficiency
    """

    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_val, var_value, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()"""
        var_id = id_val.get_id()

        # update the current context
        self.context.update({var_id: {"var_value": var_value, "attr": attr}})

        # if identifier (key) is defined in the outer context, also
        # update the binding for the outer context

        # if this is not on the top-level
        if self.outer_context != None:
            if (var_id in self.get_outer_context_var_id()):
                self.outer_context.update({var_id: {"var_value": var_value, "attr": attr}})

    def lookup(self, id_expr):
        try:
            return self.context[id_expr.get_id()]["var_value"]
        except KeyError:
            raise error.Context_Error(
                "Identifier \"" + id_expr.get_id() + "\" specified is not in the scope of the evaluation context.")

    def __str__(self):
        return str(self.context)

    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Eval_Context()

    def get_current_context_var_id(self):
        # get a list of variable identifier (in string) in the current context
        return self.context.keys()

    def get_outer_context_var_id(self):
        if self.outer_context != None:
            # get a list of variable identifier (in string) in the outer context
            return self.outer_context.keys()


class Type_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the type associated with it

    Attributes:
        context: {"var_id": evaluated_var_type, ...}
    """

    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_expr, var_type, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()
        attr: attributes of the id_expr (by declaration)
        """
        var_id = id_expr.get_id()

        # update the current context
        self.context.update({var_id: {"var_type": var_type, "attr": attr}})

        # if identifier (key) is defined in the outer context, also
        # update the binding for the outer context

        # if this is not on the top-level
        if self.outer_context != None:
            if (var_id in self.get_outer_context_var_id()):
                self.outer_context.update({var_id: {"var_type": var_type, "attr": attr}})

    def lookup(self, id_expr):
        try:
            return self.context[id_expr.get_id()]["var_type"]
        except KeyError:
            raise exceptions.Context_Lookup_Error(
                "Identifier \"" + id_expr.get_id() + "\" specified is not in the scope of the type context.")

    def __str__(self):
        return str(self.context)

    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Type_Context()

    def get_current_context_var_id(self):
        # get a list of variable identifier (in string) in the current context
        return self.context.keys()

    def get_outer_context_var_id(self):
        if self.outer_context != None:
            # get a list of variable identifier (in string) in the outer context
            return self.outer_context.keys()
