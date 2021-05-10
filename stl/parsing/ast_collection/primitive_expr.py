from abc import ABC

from stl.parsing.ast_collection.core import Primitive_Expr, Expr, Val
from stl.parsing.ast_collection.val import Boolean_Val, Float_Val, Int_Val
from stl.tool import String_Builder
import stl.error as error
import stl.tool as tool
import stl.parsing.type as types
from stl.obj.result import STL_Expr_Eval_Result
from typing import Union, Tuple, Optional


##########################
# Non-Ternary Expression #
##########################

class Non_Ternary_Expr(Expr, ABC):
    """super class for all non-ternary expressions (including unary and binary expressions), like binary arithmetic, logic and comparison expressions"""

    def __init__(self, op: str, op_type: str, lhs: Optional[Expr], rhs: Expr):
        # unary expr does not have lhs_expr, thus Optional
        self.op_val = op
        self.op_type_val = op_type
        self.lhs_val = lhs
        self.rhs_val = rhs

    #######################
    # getters and setters #
    #######################

    @property
    def op(self):
        return self.op_val

    @op.setter
    def op(self, operator: str):
        self.op_val = operator

    @property
    def op_type(self):
        return self.op_type_val

    @op_type.setter
    def op_type(self, op_type: str):
        self.op_type = op_type

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


######################
# Ternary Expression #
######################

class Ternary_Expr(Primitive_Expr, ABC):
    """super class for all primitive expressions, like binary arithmetic, logic and comparison expressions"""

    def __init__(self, op1: str, op1_type: str,
                 op2: str, op2_type: str, opd1: Expr, opd2: Expr, opd3: Expr):
        self.op1_val = op1
        self.op2_val = op2

        self.op1_type = op1_type
        self.op2_type = op2_type

        self.opd1_val = opd1
        self.opd2_val = opd2
        self.opd3_val = opd3

    #######################
    # getters and setters #
    #######################

    @property
    def op1(self):
        return self.op1_val

    @op1.setter
    def op1(self, op: str):
        self.op1_val = op

    @property
    def op2(self):
        return self.op2_val

    @op2.setter
    def op2(self, op: str):
        self.op2_val = op

    @property
    def op1_type(self):
        return self.op1_type_val

    @op1_type.setter
    def op1_type(self, op_type: str):
        self.op1_type_val = op_type

    @property
    def op2_type(self):
        return self.op2_type_val

    @op2_type.setter
    def op2_type(self, op_type: str):
        self.op2_type_val = op_type

    @property
    def opd1(self):
        return self.opd1_val

    @opd1.setter
    def opd1(self, opd):
        self.opd1_val = opd

    @property
    def opd2(self):
        return self.opd2_val

    @opd2.setter
    def opd2(self, opd):
        self.opd2_val = opd

    @property
    def opd3(self):
        return self.opd3_val

    @opd3.setter
    def opd3(self, opd):
        self.opd3_val = opd

    def __str__(self):
        sb = String_Builder()
        sb.append("Ternary_Expr: ( ")
        sb.append(str(self.opd1))
        sb.append(" ")
        sb.append(str(self.op1))
        sb.append(" ")
        sb.append(str(self.opd2))
        sb.append(" ")
        sb.append(str(self.op2))
        sb.append(" ")
        sb.append(str(self.opd3))
        sb.append(" ) ")
        return str(sb)


class Chain_Comp_Expr(Ternary_Expr, ABC):
    def __init__(self, op1: str, op1_type: str,
                 op2: str, op2_type: str, opd1: Expr, opd2: Expr, opd3: Expr):
        super().__init__(op1, op1_type, op2, op2_type, opd1, opd2, opd3)

    def weaken(self, option: str, *args):
        # print(len(args))
        # print(self.op1_type)
        # print(self.op2_type)

        # const </<= X </<= const, args = (x, y)
        if len(args) == 2 and option == "ap-range" and (self.op1_type == "LESS" or self.op1_type == "LESS_EQUAL") and (self.op2_type == "LESS" or self.op2_type == "LESS_EQUAL"):
            self.opd1 = Binary_Arith_Expr(
                "-", "MINUS", self.opd1, Int_Val(py_obj=args[0]))
            self.opd3 = Binary_Arith_Expr(
                "+", "PLUS", self.opd3, Int_Val(py_obj=args[1]))
        
        else:
            raise RuntimeError("Not Implemented")

    def eval(self, eval_context, embedded=False):
        # desugar the chain comparison expression to two binary comparison expressions
        # binary_expr_1 = Binary_Comp_Expr(self.op1, self.op1_type, self.opd1, self.opd2).eval(eval_context)
        # binary_expr_2 = Binary_Comp_Expr(self.op2, self.op2_type, self.opd2, self.opd3).eval(eval_context)
        # print(binary_expr_1)
        # print(binary_expr_2)
        # result = (Binary_Logic_Expr("&&", "LOGICAL_AND", binary_expr_1[0], binary_expr_2[0]).eval(eval_context), 0)

        # ideal but doesn't work so freakin sophisticated
        binary_expr_1 = Binary_Comp_Expr(
            self.op1, self.op1_type, self.opd1, self.opd2)
        binary_expr_2 = Binary_Comp_Expr(
            self.op2, self.op2_type, self.opd2, self.opd3)
        result = Binary_Logic_Expr(
            "&&", "LOGICAL_AND", binary_expr_1, binary_expr_2).eval(eval_context, embedded)
        return result

    # def type_check_numeric(self, arg_type):
        # return arg_type == types.Int or arg_type
    def type_check(self, type_context):
        opd1_type = self.opd1.type_check(type_context)
        opd2_type = self.opd2.type_check(type_context)
        opd3_type = self.opd3.type_check(type_context)

        if types.is_numeric(opd1_type, opd2_type, opd3_type) or (opd1_type == opd2_type == opd3_type):
            return types.Boolean()
        else:
            raise error.AST_Error("Chain Comparison Expression, Type Mismatch, opd1 = " + str(
                opd1_type) + " opd2 = " + str(opd2_type) + " opd3 = " + str(opd3_type))
#####################
# Binary Expression #
#####################


class Binary_Expr(Non_Ternary_Expr, ABC):
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
        sb.append(str(self.op))
        sb.append(" ")
        sb.append(str(self.rhs))
        sb.append(" ) ")
        return str(sb)


# expr implementation
class Binary_Comp_Expr(Binary_Expr):
    """expr super class for binary comparison expression"""

    def weaken(self, option: str, *args):
        # X </<= const, args = (x)
        if len(args) == 1 and option == "ap-range" and (self.op_type == "LESS" or self.op_type == "LESS_EQUAL"):
            self.rhs = Binary_Arith_Expr("+", "PLUS", self.rhs, Int_Val(py_obj=args[0]))

        # X >/>= const, args = (x)
        elif len(args) == 1 and option == "ap-range" and (self.op_type == "GREATER" or self.op_type == "GREATER_EQUAL"):
            self.rhs = Binary_Arith_Expr("-", "MINUS", self.rhs, Int_Val(py_obj=args[0]))
        
        else:
            raise RuntimeError("Not Implemented!")
            
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

        if self.op_type == "GREATER" or self.op_type == "GREATER_EQUAL":
            result = Float_Val(py_obj=(lhs - rhs).value)

        elif self.op_type == "LESS" or self.op_type == "LESS_EQUAL":
            result = Float_Val(py_obj=(rhs - lhs).value)

        elif self.op_type == "EQUAL_EQUAL":
            if isinstance(lhs, Boolean_Val) or isinstance(rhs, Boolean_Val):
                pass
            else:
                result = Float_Val(-abs(lhs.value - rhs.value))

        elif self.op_type == "NOT_EQUAL":
            if isinstance(lhs, Boolean_Val) or isinstance(rhs, Boolean_Val):
                pass
            else:
                result = Float_Val(abs(lhs.value - rhs.value))

        return result

    def satisfy(self, lhs, rhs):
        """for atomic calculation - both lhs and rhs have to be a Val"""

        if self.op_type == "GREATER":
            result = lhs > rhs
        elif self.op_type == "GREATER_EQUAL":
            result = lhs >= rhs
        elif self.op_type == "LESS":
            result = lhs < rhs
        elif self.op_type == "LESS_EQUAL":
            result = lhs <= rhs
        elif self.op_type == "EQUAL_EQUAL":
            result = lhs == rhs
        elif self.op_type == "NOT_EQUAL":
            result = lhs != rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result

    def compute_satisfaction(self, lhs, rhs, eval_context, embedded: bool):
        satisfy_list = list()

        # lhs = [...]
        # rhs = Val
        if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
            for lhs_expr in lhs:
                satisfy_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs_expr, rhs
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)

        # lhs = Val
        # rhs = [...]
        elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
            for rhs_expr in rhs:
                satisfy_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs, rhs_expr
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)

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
                satisfy_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs[index], rhs[index]
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)

        # lhs = Val
        # rhs = Val
        else:
            '''return a list of satisfaction'''
            return self.satisfy(lhs, rhs)

        # depends whether expression is embedded in the STL expr, return single value if not embeded
        # something like x > 1
        if not embedded:
            # if it is not embedded in the STL expr, return a single value
            return Boolean_Val.logical_and_list(satisfy_list)
        else:
            # if it is embedded in the STL expr, return a list of them
            return satisfy_list

    def compute_robustness(self, lhs, rhs, eval_context, embedded: bool):
        robustness_list = list()

        # lhs = [...]
        # rhs = Val
        if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
            for lhs_expr in lhs:
                _, robustness_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs_expr, rhs
                ).eval(eval_context, embedded=True)
                robustness_list.append(robustness_val)

        # lhs = Val
        # rhs = [...]
        elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
            for rhs_expr in rhs:
                _, robustness_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs, rhs_expr
                ).eval(eval_context, embedded=True)
                robustness_list.append(robustness_val)

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
                _, robustness_val = Binary_Comp_Expr(
                    self.op, self.op_type, lhs[index], rhs[index]
                ).eval(eval_context, embedded=True)
                robustness_list.append(robustness_val)

        # lhs = Val
        # rhs = Val
        else:
            """return a tuple consists of satisfy and robustness values"""
            return self.robustness(lhs, rhs)

        return robustness_list

    # embedded signals whether expression is embedded in STL Expr
    def eval(self, eval_context, embedded=False) -> Union[Val, list]:
        """note that satisfaction and robustness are separated"""
        lhs = self.lhs.eval(eval_context)
        rhs = self.rhs.eval(eval_context)

        satisfy_result: Union[Val, list] = self.compute_satisfaction(
            lhs, rhs, eval_context, embedded)
        robustness_result: Optional[Union[Float_Val, list]] = None

        if not embedded:
            # only return satisfaction when not embedded in STL
            return satisfy_result
        else:
            # compute both satisfaction and robustness when evaluating STL expression
            robustness_result = self.compute_robustness(
                lhs, rhs, eval_context, embedded)
            return satisfy_result, robustness_result

    # def eval(self, eval_context) -> Tuple[Union[Boolean_Val, list[Boolean_Val]], Union[Float_Val, list[Float_Val]]]:
    #     """
    #     when evaluating atomic lhs/rhs expressions, return (Boolean_Val, Float_Val)
    #     when evaluating expression lists (multiple values extracted from signal, return (list[Boolean_Val], list[Float_Val])
    #     """
    #     lhs = self.lhs.eval(eval_context)
    #     rhs = self.rhs.eval(eval_context)

    #     satisfy_list = list()
    #     robustness_list = list()

    #     # lhs = [...]
    #     # rhs = Val
    #     if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
    #         for lhs_expr in lhs:
    #             satisfy_val, robustness_val = Binary_Comp_Expr(
    #                 self.op, self.op_type, lhs_expr, rhs
    #             ).eval(eval_context)
    #             satisfy_list.append(satisfy_val)
    #             robustness_list.append(robustness_val)
    #         return satisfy_list, robustness_list

    #     # lhs = Val
    #     # rhs = [...]
    #     elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
    #         for rhs_expr in rhs:
    #             satisfy_val, robustness_val = Binary_Comp_Expr(
    #                 self.op, self.op_type, lhs, rhs_expr
    #             ).eval(eval_context)
    #             satisfy_list.append(satisfy_val)
    #             robustness_list.append(robustness_val)
    #         return satisfy_list, robustness_list

    #     # lhs = [...]
    #     # rhs = [...]
    #     elif (isinstance(lhs, list)) and (isinstance(rhs, list)):

    #         # case when lhs is a list, but not the rhs
    #         lhs_list_len = len(lhs)
    #         rhs_list_len = len(rhs)

    #         if lhs_list_len != rhs_list_len:
    #             raise RuntimeError(
    #                 "list values doesn't match! lhs = " + str(lhs) + " rhs = " + str(rhs))

    #         for index in range(lhs_list_len):
    #             satisfy_val, robustness_val = Binary_Comp_Expr(
    #                 self.op, self.op_type, lhs[index], rhs[index]
    #             ).eval(eval_context)
    #             satisfy_list.append(satisfy_val)
    #             robustness_list.append(robustness_val)
    #         return satisfy_list, robustness_list

    #     # lhs = Val
    #     # rhs = Val
    #     else:
    #         """return a tuple consists of satisfy and robustness values"""
    #         return self.satisfy(lhs, rhs), self.robustness(lhs, rhs)


class Binary_Logic_Expr(Binary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        # TODO: make sure lhs and rhs are of consistent types
        # return the types.Boolean type

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

    def satisfy(self, lhs, rhs):
        if self.op_type == "LOGICAL_AND":
            result = lhs.logical_and(rhs)

        elif self.op_type == "LOGICAL_OR":
            result = lhs.logical_or(rhs)

        elif self.op_type == "LOGICAL_IMPLIES":
            result = lhs.logical_implies(rhs)

        elif self.op_type == "LOGICAL_EQUALS":
            result = lhs.logical_equals(rhs)

        else:
            raise error.AST_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result

    def is_quantifiable_op(self):
        # check whether the operator is quantifiable
        return self.op_type == "LOGICAL_AND" or self.op_type == "LOGICAL_OR"

    def robustness(self, lhs, rhs):
        """for atomic calculation - both lhs and rhs have to be a Int_Val or Float_Val"""
        # TODO: convert all result to float values

        result = None

        if self.op_type == "LOGICAL_AND":
            result = Float_Val(py_obj=min(lhs.value, rhs.value))

        elif self.op_type == "LOGICAL_OR":
            result = Float_Val(py_obj=max(lhs.value, rhs.value))

        else:
            raise RuntimeError(
                "operator " + str(self.op_type) + " is not quantifiable!")
        return result

    def compute_satisfaction(self, lhs, rhs, eval_context, embedded: bool):
        satisfy_list = list()

        if isinstance(lhs, tuple):
            lhs, _ = lhs  # unpack lhs satisfaction value

        if isinstance(rhs, tuple):
            rhs, _ = rhs  # unpack rhs satisfaction value

        # lhs = [...]
        # rhs = Val
        if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
            raise RuntimeError("Form not allowed! lhs = list, rhs = Val")

        # lhs = Val
        # rhs = [...]
        elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
            raise RuntimeError("Form not allowed! lhs = Val, rhs = list")

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
                satisfy_val = Binary_Logic_Expr(
                    self.op, self.op_type, lhs[index], rhs[index]
                ).eval(eval_context)
                satisfy_list.append(satisfy_val)

        # lhs = Val
        # rhs = Val
        else:
            '''return a list of satisfaction'''
            # print(lhs)
            # print(rhs)
            return self.satisfy(lhs, rhs)

        # depends whether expression is embedded in the STL expr, return single value if not embeded
        if not embedded:
            # if it is not embedded in the STL expr, return a single value
            return Boolean_Val.logical_and_list(satisfy_list)
        else:
            # if it is embedded in the STL expr, return a list of them
            return satisfy_list

    def compute_robustness(self, lhs, rhs, eval_context, embedded: bool):
        robustness_list = list()

        if isinstance(lhs, tuple):
            _, lhs = lhs  # unpack lhs robustness value

        if isinstance(rhs, tuple):
            _, rhs = rhs  # unpack rhs robustness value

        # lhs = [...]
        # rhs = Val
        if (isinstance(lhs, list)) and (not isinstance(rhs, list)):
            raise RuntimeError("Form not allowed! lhs = list, rhs = Val")

        # lhs = Val
        # rhs = [...]
        elif (not isinstance(lhs, list)) and (isinstance(rhs, list)):
            raise RuntimeError("Form not allowed! lhs = Val, rhs = list")

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
                robustness_val = self.robustness(lhs[index], rhs[index])
                # _, robustness_val = Binary_Logic_Expr(
                # self.op, self.op_type, lhs[index], rhs[index]
                # ).eval(eval_context, embedded=True)
                robustness_list.append(robustness_val)

        # lhs = Val
        # rhs = Val
        else:
            return self.robustness(lhs, rhs)

        return robustness_list

    def eval(self, eval_context, embedded=False):
        """support short-circuit evaluation? sure but under the premise that the type must be the same"""

        lhs = self.lhs.eval(eval_context, embedded)
        rhs = self.rhs.eval(eval_context, embedded)

        satisfy_result: Union[Val, list] = self.compute_satisfaction(
            lhs, rhs, eval_context, embedded)
        robustness_result: Optional[Union[Float_Val, list]] = None

        if embedded and self.is_quantifiable_op():
            robustness_result = self.compute_robustness(
                lhs, rhs, eval_context, embedded)
            return satisfy_result, robustness_result

        else:
            return satisfy_result


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

    def eval(self, eval_context, embedded=False):
        # evaluate both left and right side expressions
        lhs = self.lhs.eval(eval_context)
        rhs = self.rhs.eval(eval_context)

        if self.op_type == "PLUS":
            result = lhs + rhs
        elif self.op_type == "MINUS":
            result = lhs - rhs
        elif self.op_type == "MULTIPLY":
            result = lhs * rhs
        elif self.op_type == "DIVIDE":
            result = lhs / rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

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
        sb.append(str(self.op))
        sb.append(" ")
        sb.append(str(self.rhs))
        sb.append(" ) ")
        return str(sb)


class Unary_Logic_Expr(Unary_Expr):
    def type_check(self, type_context):
        return self.rhs.type_check(type_context)

    def eval(self, eval_context, embedded=False):
        # evaluate both left and right side expressions
        self.rhs = self.rhs.eval(eval_context)

        result = None

        if self.op_type == "LOGICAL_NOT":
            result = self.rhs.logical_not()
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result


class Unary_Arith_Expr(Unary_Expr):
    """stores binary logic operation expressions AST"""

    def type_check(self, type_context):
        result = self.rhs.type_check(type_context)
        return result

    def eval(self, eval_context, embedded=False):
        # evaluate both left and right side expressions
        rhs = self.rhs.eval(eval_context)

        result = None

        if self.op_type == "PLUS":
            result = rhs
        elif self.op_type == "MINUS":
            result = -self.rhs
        else:
            raise error.AST_Error(
                "Operator \"" + str(self.op_type) + "\" for Binary Comparison Expression is invalid.")

        return result
