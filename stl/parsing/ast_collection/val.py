# Created by Simon Chu
# 2020-11-06 08:00:03
#
# references:
# python operator overload
# https://www.geeksforgeeks.org/operator-overloading-in-python/


import stl.tool as tool
from stl.tool import String_Builder
from stl.parsing.ast_collection.core import Val
import stl.parsing.type as types
from stl.obj.result import Val_Eval_Result
import stl.error as error
import stl.parsing.type as types
from stl.obj.result import Eval_Result_Transformer
from typing import Any, Optional
from abc import ABC


class Primitive_Val(Val, ABC):
    """super class for values, store primitive value types"""

    def __eq__(self, rhs):
        # this check is necessary because the program seems to pass None sometimes for rhs
        if rhs is not None:

            # greater or equal to
            result = None

            if self.value == rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            result = Boolean_Val("false")

        return result

    def __ne__(self, rhs):
        # debug
        # this check is necessary because the program seems to pass None sometimes for rhs
        # print(str(rhs) + str(type(rhs)))
        if rhs is not None:

            # greater or equal to
            result = None

            if self.value != rhs.value:
                result = Boolean_Val("true")
            else:
                result = Boolean_Val("false")

        else:
            # if rhs is None, return true since they are not equal
            result = Boolean_Val("true")

        return result

    def to_py_obj(self) -> object:
        # convert to python object
        return self.value


class Int_Val(Primitive_Val):
    def __init__(self, value: Optional[str] = None, value_type: types.Type = types.Int(), py_obj: Optional[int] = None):
        if py_obj is not None:
            super().__init__(py_obj, value_type)
        else:
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
    def __init__(self, value: Optional[str] = None, value_type: types.Type = types.Float(),
                 py_obj: Optional[float] = None):
        if py_obj is not None:
            super().__init__(py_obj, value_type)
        else:
            super().__init__(float(value), value_type)

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

    @staticmethod
    def min_of_list(float_val_list: list):  # accept list of Float_Val
        py_obj_list = list()
        for float_val in float_val_list:
            py_obj_list.append(float_val.value)
        return Float_Val(py_obj=min(py_obj_list))


class String_Val(Primitive_Val):
    def __init__(self, value: str, value_type: types.Type = types.String(), py_obj: Optional[bool] = None):
        if py_obj is not None:
            super().__init__(py_obj, value_type)
        else:
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
    def __init__(self, value: Optional[str] = None,
                 value_type: types.Type = types.Boolean(),
                 py_obj: Optional[bool] = None):

        if py_obj is not None:
            super().__init__(py_obj, value_type)
        else:
            super().__init__(tool.str_to_bool(value), value_type)

    def to_str(self):
        return tool.bool_to_str(self.value)

    def logical_and(self, rhs):
        # short-circuit evaluation
        return Boolean_Val(py_obj=(self.value and rhs.value))

    def logical_or(self, rhs):
        return Boolean_Val(py_obj=(self.value or rhs.value))

    def logical_implies(self, rhs):
        return Boolean_Val(py_obj=((not self.value) or rhs.value))

    def logical_not(self):
        return Boolean_Val(py_obj=(not self.value))

    def logical_equals(self, rhs):
        return Boolean_Val(py_obj=(self.value == rhs.value))

    @staticmethod
    def logical_and_list(boolean_val_list):
        """support for G: Globally operator"""
        result = Boolean_Val(py_obj=True)   # by default result is set to True

        # loop through the boolean value list and calculate the logical and value
        for boolean_val in boolean_val_list:
            result = boolean_val.logical_and(result)

            # short circuit for the multiple logical and connectives
            if result == Boolean_Val(py_obj=False):
                return result

        return result

    @staticmethod
    def logical_or_list(boolean_val_list):
        """super for F: Eventually operator"""
        result = Boolean_Val(py_obj=False)  # by default result is set to True

        # loop through the boolean value list and calculate the logical and value
        for boolean_val in boolean_val_list:
            result = boolean_val.logical_or(result)

            # short circuit for the multiple logical and connectives
            if result == Boolean_Val(py_obj=True):
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
        if self.value_val is not None:
            return self.value
        else:
            raise error.AST_Error("name attribute does not exist")

    @name.setter
    def name(self, value: str):
        self.value(value)

    @property
    def cached_eval_result(self):
        if self.cached_eval_result is not None:
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
        """return a list of low-level values sliced by the local_begin_time and local_end_time"""
        local_begin_time: Int_Val = eval_context.lookup(Id_Val("local_begin_time"))
        local_end_time: Int_Val = eval_context.lookup(Id_Val("local_end_time"))

        result: list = eval_context.lookup_signal(self, begin_time=local_begin_time, end_time=local_end_time)
        return result

    def type_check(self, type_context):
        """
        ensure the variable for all signal entries are homogenous
        return the common type across all signal entries of the particular variable
        """
        # get the signal
        # signal_var_type = type_context.lookup_signal(self)
        # self.value_type(signal_var_type)
        # return signal_var_type
        # TODO: uncomment the type return expression by default all signal entries returns float
        return types.Float()

    def to_py_obj(self) -> Any:
        """return cache if available, otherwise, return None"""
        if self.cached_eval_result:
            return Eval_Result_Transformer(self.cached_eval_result).transform()
        else:
            return None
