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

