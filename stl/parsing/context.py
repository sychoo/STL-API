# Simon Chu
# Sun Jan 10 21:10:06 EST 2021

import stl.error as error
from stl.parsing.ast_collection.val import Id_Val, Int_Val
from typing import Optional

class Eval_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the value associated with it

    Attributes:
        context: {"id_name": evaluated_id_value, ...}
        use id string for the key of the dictionary to boost the look up speed and efficiency
    """

    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_expr, id_value, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()"""
        id_name = id_expr.name

        # update the current context
        self.context.update({id_name: {"id_value": id_value, "attr": attr}})

    def has_id(self, id_expr):
        """check if the context has a particular identifier"""
        return id_expr.name in self.context.keys()

    def lookup(self, id_expr):
        try:
            return self.context[id_expr.name]["id_value"]
        except KeyError:
            raise error.Context_Error(
                "Identifier \"" + id_expr.name() + "\" specified is not in the scope of the evaluation context.")

    def __str__(self):
        return str(self.context)

    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Eval_Context()

    def get_current_context_id_names(self):
        """get a list of variable identifiers (in string) in the current context"""
        return self.context.keys()

    def lookup_signal(self, id_expr, begin_time: Optional[Int_Val] = None, end_time: Optional[Int_Val] = None):
        """look up the value for the corresponding identifier for the signal"""
        # get the signal data first
        signal = self.lookup(Id_Val("signal"))
        result: Optional[list] = None

        if begin_time != None and end_time != None:
            result: list = signal.lookup(id_expr.name, begin_time=begin_time.value, end_time=end_time.value, ll=True)
        else:
            result: list = signal.lookup(id_expr.name, ll=True)
            
        return result


class Type_Context:
    """store evaluation context, specifically dictionary containing identifier name
    and the type associated with it

    Attributes:
        context: {"id_name": evaluated_id_type, ...}
    """

    def __init__(self, context=dict(), outer_context=None):
        # by default, no outer_context (assume that it is top-level)
        self.context = context
        self.outer_context = outer_context

    def add(self, id_expr, id_value, attr=list()):
        """add new key values pairs for a new variable given Id_Expr()"""
        id_name = id_expr.name

        # update the current context
        self.context.update({id_name: {"id_type": id_value, "attr": attr}})

    def lookup(self, id_expr):
        try:
            return self.context[id_expr.name]["id_type"]
        except KeyError:
            raise error.Context_Error(
                "Identifier \"" + id_expr.name() + "\" specified is not in the scope of the type context.")

    def __str__(self):
        return str(self.context)

    def __len__(self):
        return len(self.context)

    @staticmethod
    def get_empty_context():
        return Type_Context()

    def get_current_context_id_names(self):
        """get a list of variable identifiers (in string) in the current context"""
        return self.context.keys()

    # TODO: look up the type of corresponding (list) of values corresponding to a particular identifier
    def lookup_signal(self, id_expr):
        """look up the type for the corresponding identifier for the signal"""
        pass

    def __str__(self):
        return str(self.context)

    def __len__(self):
        return len(self.context)

