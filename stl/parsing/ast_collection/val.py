# Created by Simon Chu
# 2020-11-06 08:00:03
#
# references:
# python operator overload
# https://www.geeksforgeeks.org/operator-overloading-in-python/


import stl.tool as tool
from stl.tool import String_Builder
from stl.parsing.ast_collection.core import Val, Primitive_Val
import stl.parsing.type as types
from stl.obj.result import Val_Eval_Result
import stl.error as error
import stl.parsing.type as types
from stl.obj.result import Eval_Result_Transformer
from typing import Any


class Int_Val(Primitive_Val):
    def __init__(self, value: str, value_type: types.Type = types.Int()):
        super().__init__(int(value), value_type)

    def __neg__(self):
        # unary minus for Int_Val
        result = Int_Val(-self.value)
        return result

    def __add__(self, rhs):
        """return Int_Val class type. Type signature not hardcoded for future modification"""
        # assume rhs is also a Int_Val type
        result = Int_Val(self.value + rhs.value)
        return result

    def __sub__(self, rhs):
        result = Int_Val(self.value - rhs.value, self.value_type)
        return result

    def __mul__(self, rhs):
        result = Int_Val(self.value * rhs.value, self.value_type)
        return result

    def __truediv__(self, rhs):
        # note that integer division will return integer
        result = Int_Val(self.value // rhs.value, self.value_type)
        return result

    def __ge__(self, rhs):
        # greater or equal to
        result = None

        if self.value >= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __gt__(self, rhs):
        # greater or equal to
        result = None

        if self.value > rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __le__(self, rhs):
        # greater or equal to
        result = None

        if self.value <= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __lt__(self, rhs):
        # greater or equal to
        result = None

        if self.value < rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result


class Float_Val(Primitive_Val):
    def __init__(self, value: str, value_type: types.Type = types.Float()):
        super().__init(float(value), value_type)

    def __neg__(self):
        # unary minus for Float_Val
        result = Float_Val(-self.value)
        return result

    def __add__(self, rhs):
        """return Float_Val class type. Type signature not hardcoded for future modification"""
        # assume rhs is also a Float_Val type
        result = Float_Val(self.value + rhs.value)
        return result

    def __sub__(self, rhs):
        result = Float_Val(self.value - rhs.value)
        return result

    def __mul__(self, rhs):
        result = Float_Val(self.value * rhs.value)
        return result

    def __truediv__(self, rhs):
        # note that integer division will return integer
        result = Float_Val(self.value / rhs.value)
        return result

    def __ge__(self, rhs):
        # greater or equal to
        result = None

        if self.value >= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __gt__(self, rhs):
        # greater or equal to
        result = None

        if self.value > rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __le__(self, rhs):
        # greater or equal to
        result = None

        if self.value <= rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result

    def __lt__(self, rhs):
        # greater or equal to
        result = None

        if self.value < rhs.value:
            result = Boolean_Val("true")
        else:
            result = Boolean_Val("false")

        return result


class String_Val(Primitive_Val):
    def __init__(self, value: str, value_type: types.Type = types.String()):
        super().__init__(value, value_type)

    def __neg__(self):
        # unary minus for Int_Val
        result = Int_Val(-self.value)
        return result

    def __add__(self, rhs):
        """return Int_Val class type. Type signature not hardcoded for future modification"""
        # assume rhs is also a Int_Val type
        result = String_Val(self.value + rhs.value)
        return result

    def to_str(self):
        """strip the double quotes for the string"""
        return self.value[1:-1]


class Boolean_Val(Primitive_Val):
    def __init__(self, value: str, value_type: types.Type = types.Boolean()):
        super().__init__(tool.str_to_bool(value), value_type)

    def to_str(self):
        return tool.bool_to_str(self.value)

    def logical_and(self, rhs):
        # short-circuit evaluation
        return Boolean_Val(tool.bool_to_str(self.value and rhs.value))

    def logical_or(self, rhs):
        return Boolean_Val(tool.bool_to_str(self.value or rhs.value))

    def logical_implies(self, rhs):
        return Boolean_Val(tool.bool_to_str((not self.value) or rhs.value))

    def logical_not(self):
        return Boolean_Val(Tools.bool_to_str(not self.value))

    @staticmethod
    def logical_and_list(boolean_val_list):
        # set the result to true by default
        result = Boolean_Val("true")

        # loop through the boolean value list and calculate the logical and value
        for boolean_val in boolean_val_list:
            result = boolean_val.logical_and(result)

            # short circuit for the multiple logical and connectives
            if result == Boolean_Val("false"):
                return result

        return result


class Id_Val(Val):
    """stores identifier of the variable, variable expression
    stores
            type signature
            variable identifier signature
            and STL formula operator
    """

    def __init__(self, value: str, value_type: types.Type = types.Unresolved()):
        super().__init__(value, value_type)
        self.cached_eval_result_val = None

    # alias to value field
    @property
    def name(self):
        if self.value_val:
            return self.value
        else:
            raise error.AST_Error("name attribute does not exist")

    @name.setter
    def name(self, value: str):
        self.value(value)

    @property
    def cached_eval_result(self):
        if self.cached_eval_result:
            return self.cached_eval_result_val
        else:
            raise error.AST_Error("cached_eval_result attribute does not exist")

    @cached_eval_result.setter
    def cached_eval_result(self, cached_eval_result: Val):
        self.cached_eval_result_val = cached_eval_result

    def __str__(self):
        sb = String_Builder()
        sb.append("Id_Val: ( ")
        sb.append(self.name)
        sb.append(" )")

        return str(sb)

    def eval(self, eval_context):
        return eval_context.lookup(self)

    def type_check(self, type_context):
        """
        ensure the variable for all signal entries are homogenous
        return the common type across all signal entries of the particular variable
        """
        # get the signal
        # signal_var_type = type_context.lookup_signal(self)
        # self.value_type(signal_var_type)
        # return signal_var_type
        # TODO: uncomment the type return expression
        return types.Float

    def to_py_obj(self) -> Any:
        """return cache if available, otherwise, return None"""
        if self.cached_eval_result:
            return Eval_Result_Transformer(self.cached_eval_result).transform()
        else:
            return None


class Meta_Id_Val(Val):
    """stores identifier of the variable, variable expression
    stores
            type signature
            variable identifier signature
            and STL formula operator
    """

    def __init__(self, var_id):
        """take the identifier name of the variable"""
        self.var_id = var_id

    def __str__(self):
        sb = String_Builder()
        sb.append("Meta_Id_Val: ( ")
        sb.append(self.var_id)
        sb.append(" )")

        return str(sb)

    def get_id(self):
        return self.var_id

    def eval(self, eval_context):
        """eval function for Meta_Identifier will generate a list of evaluations for further comparisons for relational operators"""
        # debugger

        # next step:
        # for each binary/unary comparison, logic, arithmetic operations,
        # add comparison of [] list, which will check whether all list of values satisfies the condition
        # evalute a meta identifier
        # $1.content -> {"param" : param}
        # return a list of values?

        # self.var_id : meta variable's name, i.e. $param
        # lookup_value_list = list()

        # context_var_ids = eval_context.get_current_conext_var_id()

        # loop through all the variable ids
        # for var_id in context_var_ids:

        # list for accumulating the overall value
        value_list = list()

        # look for the valid signal dictionary in the evaluation context
        # this will look something like {"1": {"content": {}}, "2": {"content": {}}, ... }
        valid_signal_dict = eval_context.lookup(Meta_Id_Val("$this")).get_signal_dict()

        # get rid of the "$" - dollar sign at the beginning
        self.var_id = self.var_id[1:]

        # parse the self.var_id - the variable name for the current meta variable
        splited_var_id_list = self.var_id.split(".")

        # look up the concrete variable in the signal dictionary
        for time_index in valid_signal_dict.keys():
            valid_signal_dict_content = valid_signal_dict[time_index]["content"]

            # recursively look up the splited var id until reaching the right level
            for splited_var_id in splited_var_id_list:
                valid_signal_dict_content = valid_signal_dict_content[splited_var_id]

            # only allow int -> Int_Val at current stage
            # TODO: array -> Array_Val
            if isinstance(valid_signal_dict_content, int):
                # append the obtained value to the value_list
                value_list.append(Int_Val(valid_signal_dict_content))

                # signal_content_dict = eval_context.lookup(Meta_Id_Val(var_id))
        # get rid of the $ sign when looking it up in the signal dictionary
        # lookup_value_list.append(signal_content_dict[self.var_id[1:]])
        # return eval_context.lookup(self)
        # print(value_list)

        return value_list

    def type_check(self, type_context):
        # do not require type check, simply pass
        pass
