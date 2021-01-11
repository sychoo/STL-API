from abc import ABC

from stl.parsing.ast_collection.core import Primitive_Expr
from stl.parsing.ast_collection.val import Boolean_Val
from stl.tool import String_Builder
import stl.error as error
import stl.tool as tool
import stl.parsing.type as types


#####################
# Binary Expression #
#####################

class Binary_Expr(Primitive_Expr, ABC):
    """super class for binary expressions"""

    def __init__(self, op_str, op_type, lhs_expr, rhs_expr):
        self.op_str = op_str
        self.op_type = op_type
        self.lhs_expr = lhs_expr
        self.rhs_expr = rhs_expr

    def __str__(self):
        sb = String_Builder()
        sb.append("Binary_Expr: ( ")
        sb.append(str(self.lhs_expr))
        sb.append(" ")
        sb.append(str(self.op_str))
        sb.append(" ")
        sb.append(str(self.rhs_expr))
        sb.append(" ) ")
        return str(sb)


# expr implementation
class Binary_Comp_Expr(Binary_Expr):
    """stores binary comparison operation expression AST, except Binary STL expressions
    handles the evaluation of meta variable

    There are 3 scenarios in term of the position of meta variables

    - Meta varible can be on the LHS of the binary comparison
        - simply convert the entire Binary_Comp_Expr to a list of Binary_Comp_Expr's (with no meta variables), evaluate them separately, and result in a final value using logical_and

    - Similar thing happens on the RHS (similar to when meta variable is located on the LHS)

    - When meta variable exists on both side of the binary expression, compare each element of the list separately (comparison will only exist on individual time/moment level)
    """

    def type_check(self, type_context):
        # lhs and rhs can be of "list" type or
        # type have to be consistent
        lhs_expr_type = self.lhs_expr.type_check(type_context)
        rhs_expr_type = self.rhs_expr.type_check(type_context)

        if lhs_expr_type != rhs_expr_type:
            raise error.Type_Error("Type Mismatch for " + str(self))

        else:
            return types.Boolean()

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.lhs_expr = self.lhs_expr.eval(eval_context)
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        result = None

        if (isinstance(self.lhs_expr, list)) and (not isinstance(self.rhs_expr, list)):
            # evaluated boolean value list
            evaluated_boolean_val_list = list()

            # case when lhs is a list, but not the rhs
            for single_lhs_expr in self.lhs_expr:
                # connect them with a huge boolean and
                evaluated_boolean_val_list.append(
                    Binary_Comp_Expr(self.op_str, self.op_type, single_lhs_expr, self.rhs_expr).eval(eval_context))

            return Boolean_Val.logical_and_list(evaluated_boolean_val_list)

        elif (not isinstance(self.lhs_expr, list)) and (isinstance(self.rhs_expr, list)):
            # evaluated boolean value list
            evaluated_boolean_val_list = list()

            # case when lhs is a list, but not the rhs
            for single_rhs_expr in self.rhs_expr:
                # connect them with a huge boolean and
                evaluated_boolean_val_list.append(
                    Binary_Comp_Expr(self.op_str, self.op_type, self.lhs_expr, single_rhs_expr).eval(eval_context))

            return Boolean_Val.logical_and_list(evaluated_boolean_val_list)

        elif (isinstance(self.lhs_expr, list)) and (isinstance(self.rhs_expr, list)):
            # evaluated boolean value list
            evaluated_boolean_val_list = list()

            # case when lhs is a list, but not the rhs
            lhs_expr_list_length = len(self.lhs_expr)
            rhs_expr_list_length = len(self.rhs_expr)

            if lhs_expr_list_length != rhs_expr_list_length:
                raise RuntimeError(
                    "list values doesn't match! lhs = " + str(self.lhs_expr) + " rhs = " + str(self.rhs_expr))

            for index in range(lhs_expr_list_length):
                # connect them with a huge boolean and
                evaluated_boolean_val_list.append(
                    Binary_Comp_Expr(self.op_str, self.op_type, self.lhs_expr[index], self.rhs_expr[index]).eval(
                        eval_context))

            return Boolean_Val.logical_and_list(evaluated_boolean_val_list)


        else:
            if self.op_type == "GREATER":
                result = self.lhs_expr > self.rhs_expr
            elif self.op_type == "GREATER_EQUAL":
                result = self.lhs_expr >= self.rhs_expr
            elif self.op_type == "LESS":
                result = self.lhs_expr < self.rhs_expr
            elif self.op_type == "LESS_EQUAL":
                result = self.lhs_expr <= self.rhs_expr
            elif self.op_type == "EQUAL_EQUAL":
                result = self.lhs_expr == self.rhs_expr
            elif self.op_type == "NOT_EQUAL":
                result = self.lhs_expr != self.rhs_expr
            else:
                raise exceptions.Operator_Not_Found_Error(
                    "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Binary_Logic_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        # make sure lhs and rhs are of consistent types
        # return the common type information

        pass

    def eval(self, eval_context):
        """support short-circuit evaluation? sure but under the premise that the type must be the same"""
        # initialize result to None
        result = None

        # evaluate both left and right side expressions
        self.lhs_expr = self.lhs_expr.eval(eval_context)
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        if self.op_type == "LOGICAL_AND":
            result = self.lhs_expr.logical_and(self.rhs_expr)

        elif self.op_type == "LOGICAL_OR":
            result = self.lhs_expr.logical_or(self.rhs_expr)

        elif self.op_type == "LOGICAL_IMPLIES":
            result = self.lhs_expr.logical_implies(self.rhs_expr)

        else:
            raise exceptions.Operator_Not_Found_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Binary_Arith_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        # intialize result to None
        result = None

        # the type on both sides of the operator must be the same
        # print(type_context)
        self.lhs_expr_type = self.lhs_expr.type_check(type_context)
        self.rhs_expr_type = self.rhs_expr.type_check(type_context)

        # print("lhs type_checked : " + str(type(self.lhs_expr_type)))
        # print("rhs type_checked : " + str(type(self.rhs_expr_type)))
        # print("true? " + str(self.lhs_expr_type != self.rhs_expr_type))

        if self.lhs_expr_type != self.rhs_expr_type:
            raise error.Type_Error("Type Mismatch in Binary Arithmetic Expression: lhs type = " + str(
                self.lhs_expr_type) + " rhs type = " + str(self.rhs_expr_type))

        else:
            # when the type is consistent
            result = self.lhs_expr_type

        return result

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.lhs_expr = self.lhs_expr.eval(eval_context)
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        # print("lhs : " + str(type(self.lhs_expr)))
        # print("rhs : " + str(type(self.rhs_expr)))
        result = None

        if self.op_type == "PLUS":
            result = self.lhs_expr + self.rhs_expr
        elif self.op_type == "MINUS":
            result = self.lhs_expr - self.rhs_expr
        elif self.op_type == "MULTIPLY":
            result = self.lhs_expr * self.rhs_expr
        elif self.op_type == "DIVIDE":
            result = self.lhs_expr / self.rhs_expr
        else:
            raise exceptions.Operator_Not_Found_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        # the result is wrapped by primitive object
        return result


####################
# Unary Expression #
####################

class Unary_Expr(Binary_Expr, ABC):
    """super class for unary expressions"""

    def __init__(self, op_str, op_type, rhs_expr):
        # the string of the operator
        self.op_str = op_str

        # the type of the operator (PLUS)
        self.op_type = op_type

        # right hand expr
        self.rhs_expr = rhs_expr

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_Expr: ( ")
        sb.append(str(self.op_str))
        sb.append(" ")
        sb.append(str(self.rhs_expr))
        sb.append(" ) ")
        return str(sb)


class Unary_Logic_Expr(Unary_Expr):
    def type_check(self, type_context):
        return self.rhs_expr.type_check(type_context)

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        result = None

        if self.op_type == "LOGICAL_NOT":
            result = self.rhs_expr.logical_not()
        else:
            raise exceptions.Operator_Not_Found_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Unary_Arith_Expr(Unary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        result = self.rhs_expr.type_check(type_context)
        return result

    def eval(self, eval_context):
        # evaluate both left and right side expressions
        self.rhs_expr = self.rhs_expr.eval(eval_context)

        result = None

        if self.op_type == "PLUS":
            result = self.rhs_expr
        elif self.op_type == "MINUS":
            result = -self.rhs_expr
        else:
            raise exceptions.Operator_Not_Found_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result

