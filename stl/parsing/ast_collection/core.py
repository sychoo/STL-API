# for implementing abstract method

from abc import ABC, ABCMeta, abstractmethod

from stl.tool import String_Builder
import stl.parsing.type as types  # for low-level internally defined types
import stl.error as error
from typing import Optional, Any
# from stl.parsing.ast_collection.val import Boolean_Val

class Node(metaclass=ABCMeta):  # metaclass=abc.ABCMeta support abstract method definition
    """super class for all nodes in the AST (abstract syntax tree)"""

    @abstractmethod
    def eval(self, eval_context):
        pass

    @abstractmethod
    def type_check(self, type_context):
        pass

    @abstractmethod
    def __str__(self):
        """method to display the string representation of the AST for parser"""
        pass


class Expr(Node, ABC):
    """super class for expressions"""
    pass


class Primitive_Expr(Expr, ABC):
    """super class for all primitive expressions, like arithmetic, logic and comparison expressions"""
    def __init__(self, operator: str, operator_type: str, lhs: Optional[Expr], rhs: Expr):
        # unary expr does not have lhs_expr, thus Optional
        self.operator_val = operator
        self.operator_type_val = operator_type
        self.lhs_val = lhs
        self.rhs_val = rhs

    #######################
    # getters and setters #
    #######################

    @property
    def operator(self):
        return self.operator_val

    @operator.setter
    def operator(self, operator: str):
        self.operator_val = operator

    @property
    def operator_type(self):
        return self.operator_type_val

    @operator_type.setter
    def operator_type(self, operator_type: str):
        self.operator_type = operator_type

    @property
    def lhs(self):
        return self.lhs_val

    @lhs.setter
    def lhs(self, lhs: Expr):
        self.lhs_val = lhs

    @property
    def rhs(self):
        return self.rhs_val

    @rhs.setter
    def rhs(self, rhs: Expr):
        self.rhs_val = rhs


class STL_Expr(Expr, ABC):
    """super class for STL expressions"""

    def __init__(self, operator: str, begin_time: Optional[Expr] = None, end_time: Optional[Expr] = None,
                 begin_condition: Optional[Expr] = None, end_condition: Optional[Expr] = None):
        """must supply an operator. all other parameters are optional"""

        self.operator_val = operator
        self.begin_time_val = begin_time
        self.end_time_val = end_time
        self.begin_condition_val = begin_condition
        self.end_condition_val = end_condition

    def type_check(self, type_context) -> types.Type:
        """type check all available attributes of STL expression"""
        if self.begin_time:
            begin_time_type = self.begin_time.type_check(type_context)

            if begin_time_type != types.Int():
                raise error.Type_Error(
                    "Begin time interval for STL expression must be of type Int. It is now of type " +
                    str(begin_time_type)
                )

        if self.end_time:
            end_time_type = self.end_time.type_check(type_context)

            if end_time_type != types.Int():
                raise error.Type_Error(
                    "End time interval for STL expression must be of type Int. It is now of type " +
                    str(end_time_type)
                )

        if self.begin_condition:
            begin_condition_type = self.begin_condition.type_check(type_context)

            if begin_condition_type != types.Boolean():
                raise error.Type_Error(
                    "Conditional expressions for STL expressions must be of type Boolean. It is now of type " +
                    str(begin_condition_type)
                )

        if self.end_condition:
            end_condition_type = self.end_condition.type_check(type_context)

            if end_condition_type != types.Boolean():
                raise error.Type_Error(
                    "End conditional expressions for STL expressions must be of type Boolean. It is now of type " +
                    str(end_condition_type)
                )

        return types.STL  # default behavior

    def eval(self, eval_context) -> None:
        """evaluate all available attributes of STL expression"""
        if self.begin_time:
            self.begin_time(self.begin_time.eval(eval_context))
        
        if self.end_time:
            self.end_time(self.end_time.eval(eval_context))
        
        if self.begin_condition:
            self.begin_condition(self.begin_condition.eval(eval_context))
        
        if self.end_condition:
            self.end_condition(self.end_condition.eval(eval_context))

    def __str__(self):
        pass

    #######################
    # getters and setters #
    #######################
    @property
    def operator(self):
        return self.operator_val

    @operator.setter
    def operator(self, operator: str):
        self.operator_val = operator

    @property
    def begin_time(self):
        return self.begin_time_val

    @begin_time.setter
    def begin_time(self, begin_time: Expr):
        self.begin_time_val = begin_time

    @property
    def end_time(self):
        return self.end_time_val

    @end_time.setter
    def end_time(self, end_time: Expr):
        self.end_time_val = end_time

    @property
    def begin_condition(self):
        return self.begin_condition_val

    @begin_condition.setter
    def begin_condition(self, begin_condition: Expr):
        self.begin_condition_val = begin_condition

    @property
    def end_condition(self):
        return self.end_condition_val

    @end_condition.setter
    def end_condition(self, end_condition: Expr):
        self.end_condition_val = end_condition


class Val(Expr, ABC, metaclass=ABCMeta):
    """super class for values, store primitive value types"""

    def __init__(self, value: Any, value_type: types.Type):
        self.value_val = value
        self.value_type_val = value_type  # note that type is a reserved word

    @abstractmethod
    def to_py_obj(self) -> Any:
        """convert internal representation of value in AST to Python object"""
        pass

    #######################
    # getters and setters #
    #######################
    @property
    def value(self):
        if self.value_val is not None:
            return self.value_val
        else:
            raise error.AST_Error("value attribute does not exist")

    @value.setter
    def value(self, value):
        self.value_val = value

    @property
    def value_type(self):
        if self.value_type_val is not None:
            return self.value_type_val
        else:
            raise error.AST_Error("value_type attribute does not exist")

    @value_type.setter
    def value_type(self, value_type):
        self.value_type_val = value_type

    def __str__(self):
        sb = String_Builder()
        sb.append("Val: ( ")
        sb.append(str(self.value))
        sb.append(", ")
        sb.append(str(self.value_type))
        sb.append(" )")
        return str(sb)

    def to_str(self):
        return str(self.value)

    def eval(self, eval_context):
        return self

    def type_check(self, type_context):
        return self.value_type



