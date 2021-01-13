from abc import ABC

from stl.parsing.ast_collection.core import Primitive_Expr, Expr
from stl.parsing.ast_collection.val import Boolean_Val, Float_Val
from stl.tool import String_Builder
import stl.error as error
import stl.tool as tool
import stl.parsing.type as types
from stl.obj.result import STL_Expr_Eval_Result
from typing import Union, Tuple


#####################
# Binary Expression #
#####################

class Binary_Expr(Primitive_Expr, ABC):
    """super class for binary expressions"""

    #
    # def __init__(self, op_str, op_type, lhs_expr, rhs_expr):
    #     self.op_str = op_str
    #     self.op_type = op_type
    #     self.lhs_expr = lhs_expr
    #     self.rhs_expr = rhs_expr
    def __init__(self, operator: str, operator_type: str, lhs: Expr, rhs: Expr):
        super().__init__(operator, operator_type, lhs, rhs)

    def __str__(self):
        sb = String_Builder()
        sb.append("Binary_Expr: ( ")
        sb.append(str(self.lhs))
        sb.append(" ")
        sb.append(str(self.operator))
        sb.append(" ")
        sb.append(str(self.rhs))
        sb.append(" ) ")
        return str(sb)


# expr implementation
class Binary_Comp_Expr(Binary_Expr):
    """expr super class for binary comparison expression"""

    def type_check(self, type_context):
        # note that list of values are type checked to the common types in the list
        lhs_type = self.lhs.type_check(type_context)
        rhs_type = self.rhs.type_check(type_context)

        if (lhs_type == types.Int() and rhs_type == types.Float()) or \
                (lhs_type == types.Float() and rhs_type == types.Int()):
            return types.Boolean()

        elif lhs_type != rhs_type:
            raise error.Type_Error(
                "Type Mismatch for " + str(self) + "lhs type = " + str(lhs_type) + "rhs type = " + str(rhs_type))

        else:
            return types.Boolean()

    def robustness(self, lhs, rhs):
        """for atomic calculation - both lhs and rhs have to be a Int_Val or Float_Val"""
        # TODO: convert all result to float values

        result = None

        if self.operator_type == "GREATER" or self.operator_type == "GREATER_EQUAL":
            result = Float_Val(py_obj=(lhs - rhs).value)

        elif self.operator_type == "LESS" or self.operator_type == "LESS_EQUAL":
            result = Float_Val(py_obj=(rhs - lhs).value)

        elif self.operator_type == "EQUAL_EQUAL":
            if isinstance(lhs, Boolean_Val) or isinstance(rhs, Boolean_Val):
                pass
            else:
                result = Float_Val(-abs(lhs.value - rhs.value))

        elif self.operator_type == "NOT_EQUAL":
            if isinstance(lhs, Boolean_Val) or isinstance(rhs, Boolean_Val):
                pass
            else:
                result = Float_Val(abs(lhs.value - rhs.value))

        return result

    def satisfy(self, lhs, rhs):
        """for atomic calculation - both lhs and rhs have to be a Val"""

        if self.operator_type == "GREATER":
            result = lhs > rhs
        elif self.operator_type == "GREATER_EQUAL":
            result = lhs >= rhs
        elif self.operator_type == "LESS":
            result = lhs < rhs
        elif self.operator_type == "LESS_EQUAL":
            result = lhs <= rhs
        elif self.operator_type == "EQUAL_EQUAL":
            result = lhs == rhs
        elif self.operator_type == "NOT_EQUAL":
            result = lhs != rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.operator_type) + "\" for Binary Comparison Expression is invalid.")

        return result

    def eval(self, eval_context) -> Tuple[Union[Boolean_Val, list[Boolean_Val]], Union[Float_Val, list[Float_Val]]]:
        """
        when evaluating atomic lhs/rhs expressions, return (Boolean_Val, Float_Val)
        when evaluating expression lists (multiple values extracted from signal, return (list[Boolean_Val], list[Float_Val])
        """
        lhs = self.lhs.eval(eval_context)
        rhs = self.rhs.eval(eval_context)

        satisfy_list = list()
        robustness_list = list()

        # lhs = [...]
        # rhs = Val
        if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
            for lhs_expr in lhs:
                satisfy_val, robustness_val = Binary_Comp_Expr(
                    self.operator, self.operator_type, lhs_expr, rhs
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)
                robustness_list.append(robustness_val)
            return satisfy_list, robustness_list

        # lhs = Val
        # rhs = [...]
        elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
            for rhs_expr in rhs:
                satisfy_val, robustness_val = Binary_Comp_Expr(
                    self.operator, self.operator_type, lhs, rhs_expr
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)
                robustness_list.append(robustness_val)
            return satisfy_list, robustness_list

        # lhs = [...]
        # rhs = [...]
        elif (isinstance(lhs, list)) and (isinstance(rhs, list)):

            # case when lhs is a list, but not the rhs
            lhs_list_len = len(lhs)
            rhs_list_len = len(rhs)

            if lhs_list_len != rhs_list_len:
                raise RuntimeError(
                    "list values doesn't match! lhs = " + str(lhs) + " rhs = " + str(rhs))

            for index in range(lhs_list_len):
                satisfy_val, robustness_val = Binary_Comp_Expr(
                    self.operator, self.operator_type, lhs[index], rhs[index]
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)
                robustness_list.append(robustness_val)
            return satisfy_list, robustness_list

        else:
            """return a tuple consists of satisfy and robustness values"""
            return self.satisfy(lhs, rhs), self.robustness(lhs, rhs)


class Binary_Logic_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        # TODO: make sure lhs and rhs are of consistent types
        # return the types.Boolean type

        pass

    def eval(self, eval_context):
        """support short-circuit evaluation? sure but under the premise that the type must be the same"""
        lhs = self.lhs.eval(eval_context)
        rhs = self.rhs.eval(eval_context)

        if self.operator_type == "LOGICAL_AND":
            result = lhs.logical_and(rhs)

        elif self.operator_type == "LOGICAL_OR":
            result = lhs.logical_or(rhs)

        elif self.operator_type == "LOGICAL_IMPLIES":
            result = lhs.logical_implies(rhs)

        elif self.operator_type == "LOGICAL_EQUALS":
            result = lhs.logical_equals(rhs)

        else:
            raise error.AST_Error(
                "Operator \"" + str(self.operator_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Binary_Arith_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        lhs_type = self.lhs.type_check(type_context)
        rhs_type = self.rhs.type_check(type_context)

        if lhs_type != rhs_type:
            raise error.Type_Error("Type Mismatch in Binary Arithmetic Expression: lhs type = " + str(
                lhs_type) + " rhs type = " + str(rhs_type))

        else:
            # when the type is consistent
            result = lhs_type

        return result

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        lhs = self.lhs.eval(eval_context)
        rhs = self.rhs.eval(eval_context)

        if self.operator_type == "PLUS":
            result = lhs + rhs
        elif self.operator_type == "MINUS":
            result = lhs - rhs
        elif self.operator_type == "MULTIPLY":
            result = lhs * rhs
        elif self.operator_type == "DIVIDE":
            result = lhs / rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.operator_type) + "\" for Binary Comparison Expression is invalid.")

        # the result is wrapped by primitive object
        return result


####################
# Unary Expression #
####################

class Unary_Expr(Binary_Expr, ABC):
    """super class for unary expressions"""

    def __init__(self, operator: str, operator_type: str, rhs: Expr):
        super().__init__(operator, operator_type, None, rhs)
        # the string of the operator
        # self.op_str = op_str

        # the type of the operator (PLUS)
        # self.op_type = op_type

        # right hand expr
        # self.rhs_expr = rhs_expr

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_Expr: ( ")
        sb.append(str(self.operator))
        sb.append(" ")
        sb.append(str(self.rhs))
        sb.append(" ) ")
        return str(sb)


class Unary_Logic_Expr(Unary_Expr):
    def type_check(self, type_context):
        return self.rhs.type_check(type_context)

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.rhs = self.rhs.eval(eval_context)

        result = None

        if self.operator_type == "LOGICAL_NOT":
            result = self.rhs.logical_not()
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.operator_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Unary_Arith_Expr(Unary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        result = self.rhs.type_check(type_context)
        return result

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        rhs = self.rhs.eval(eval_context)

        result = None

        if self.operator_type == "PLUS":
            result = rhs
        elif self.operator_type == "MINUS":
            result = -self.rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.operator_type) + "\" for Binary Comparison Expression is invalid.")

        return result
