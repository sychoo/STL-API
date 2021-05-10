# 2020-11-06 07:57:20

from stl.parsing.ast_collection.primitive_expr import Binary_Arith_Expr, Binary_Comp_Expr
from stl.tool import String_Builder
import stl.error as error

from stl.parsing.ast_collection.core import Expr
from stl.parsing.ast_collection.val import Boolean_Val, Float_Val

import stl.parsing.type as types
from typing import Optional, Union
from abc import ABC

from stl.parsing.ast_collection.val import Id_Val, Int_Val
from stl.obj.result import STL_Expr_Eval_Result


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
        """evaluate the time interval specified by the user"""
        # calculate local (actual) time for conditional expression signal slicing
        # add local_begin_time and local_end_time to the context for accessing from conditional expression evaluation

        global_begin_time = eval_context.lookup(Id_Val("global_begin_time"))

        if self.begin_time is not None:
            stl_expr_begin_time = self.begin_time.eval(eval_context)
            local_begin_time = global_begin_time + stl_expr_begin_time
            eval_context.add(Id_Val("local_begin_time"), local_begin_time)

        if self.end_time is not None:
            stl_expr_end_time = self.end_time.eval(eval_context)
            local_end_time = global_begin_time + stl_expr_end_time
            eval_context.add(Id_Val("local_end_time"), local_end_time)




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


class Unary_STL_Expr(STL_Expr, ABC):
    def __init__(self, operator: str, begin_time: Expr, end_time: Optional[Expr], condition: Expr):
        """end_time is optional for (X: next) operator"""
        super().__init__(operator, begin_time=begin_time, end_time=end_time,
                         begin_condition=condition)

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_STL_Expr: ( ")
        sb.append(self.operator)
        sb.append(" [")
        sb.append(str(self.begin_time))

        # exception for X: next operator
        if self.end_time:
            sb.append(", ")
            sb.append(str(self.end_time))

        sb.append("] (")
        sb.append(str(self.begin_condition))
        sb.append(")")

        return str(sb)


# /expr implementation


class Binary_STL_Expr(STL_Expr, ABC):
    def __init__(self, operator, begin_time, end_time, begin_condition, end_condition):
        super().__init__(operator, begin_time=begin_time, end_time=end_time,
                         begin_condition=begin_condition, end_condition=end_condition)

    def __str__(self):
        sb = String_Builder()
        sb.append("Binary_STL_Expr: ( ")
        sb.append("(")
        sb.append(str(self.begin_condition))
        sb.append(") ")
        sb.append(self.op)
        sb.append(" [")
        sb.append(str(self.begin_time))
        sb.append(", ")
        sb.append(str(self.end_time))
        sb.append("] (")
        sb.append(str(self.end_condition))
        sb.append(")")

        return str(sb)


class G_Expr(Unary_STL_Expr, ABC):
    """support the globally STL expression"""

    # def eval(self, eval_context):
    #     super().eval(eval_context)

    #     # return type Tuple[Union[Boolean_Val, list[Boolean_Val]], Union[Float_Val, list[Float_Val]]]
        
    #     satisfy = self.begin_condition.eval(eval_context, embedded=True)
    #     result = None

    #     if isinstance(satisfy, list):
    #         result_satisfy = Boolean_Val.logical_and_list(satisfy).value
    #         result = STL_Expr_Eval_Result(satisfy=result_satisfy, robustness=0.0)

    #     elif isinstance(satisfy, Boolean_Val):
    #         result = STL_Expr_Eval_Result(satisfy=satisfy.value, robustness=0.0)

    #     return result

    def weaken(self, option: str, *args):
        """weaken the STL formula on the AST level"""
        if option == "ap-range":
            self.begin_condition.weaken(option, *args)
        elif option == "time-range":
            self.begin_time = Binary_Arith_Expr("+", "PLUS", self.begin_time, Int_Val(py_obj=args[0]))
            self.end_time = Binary_Arith_Expr("-", "MINUS", self.end_time, Int_Val(py_obj=args[1]))
        else:
            raise RuntimeError("Not Implemented")

    def eval(self, eval_context):
        super().eval(eval_context)

        # return type Tuple[Union[Boolean_Val, list[Boolean_Val]], Union[Float_Val, list[Float_Val]]]
        
        satisfy, robustness = self.begin_condition.eval(eval_context, embedded=True)
        result = None

        if isinstance(satisfy, list) and isinstance(robustness, list):
            result_satisfy = Boolean_Val.logical_and_list(satisfy).value
            result_robustness = Float_Val.min_of_list(robustness).value
            result = STL_Expr_Eval_Result(satisfy=result_satisfy, robustness=result_robustness)

        elif isinstance(satisfy, Boolean_Val) and isinstance(robustness, Float_Val):
            result = STL_Expr_Eval_Result(satisfy=satisfy.value, robustness=robustness.value)

        return result


# TODO: what's robustness with respect to F?
class F_Expr(Unary_STL_Expr, ABC):
    """support the future STL expression"""

    def eval(self, eval_context):
        super().eval(eval_context)

        # return type Tuple[Union[Boolean_Val, list[Boolean_Val]], Union[Float_Val, list[Float_Val]]]
        satisfy, robustness = self.begin_condition.eval(eval_context, embedded=True)
        result = None

        if isinstance(satisfy, list) and isinstance(robustness, list):
            result_satisfy = Boolean_Val.logical_or_list(satisfy).value
            # result_robustness = Float_Val.min_of_list(robustness).value
            result = STL_Expr_Eval_Result(satisfy=result_satisfy)  #, robustness=result_robustness)

        elif isinstance(satisfy, Boolean_Val) and isinstance(robustness, Float_Val):
            result = STL_Expr_Eval_Result(satisfy=satisfy.value)  #, robustness=robustness.value)

        return result


class X_Expr(Unary_STL_Expr, ABC):
    """support the future STL expression"""

    # override Unary_STL_Expr init function, since X doesn't require the passing of a time interval.
    # instead it only requires a fixed time point
    def __init__(self, operator, begin_time: Expr, begin_condition: Expr):
        super().__init__(operator, begin_time, None, begin_condition)

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_STL_Expr: ( ")
        sb.append(self.operator)
        sb.append(" [")
        sb.append(str(self.begin_time))
        sb.append("] (")
        sb.append(str(self.begin_condition))
        sb.append(")")

        return str(sb)

    def eval(self, eval_context):
        """override the super() eval, to adjust the offset of time"""
        global_begin_time = eval_context.lookup(Id_Val("global_begin_time"))

        stl_expr_begin_time = self.begin_time.eval(eval_context)
        local_begin_time = global_begin_time + stl_expr_begin_time
        eval_context.add(Id_Val("local_begin_time"), local_begin_time + Int_Val(1))  # offset by 1 for Next operator

        eval_context.add(Id_Val("local_end_time"), local_begin_time + Int_Val(1))

        satisfy_list, robustness_list = self.begin_condition.eval(eval_context, embedded=True)
        result_satisfy = Boolean_Val.logical_and_list(satisfy_list).value
        result_robustness = Float_Val.min_of_list(robustness_list).value

        return STL_Expr_Eval_Result(satisfy=result_satisfy, robustness=result_robustness)



class U_Expr(Binary_STL_Expr, ABC):
    pass


class R_Expr(Binary_STL_Expr, ABC):
    pass


class W_Expr(Binary_STL_Expr, ABC):
    pass


class M_Expr(Binary_STL_Expr, ABC):
    pass
