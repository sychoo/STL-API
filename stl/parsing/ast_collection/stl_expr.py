# 2020-11-06 07:57:20

from stl.tool import String_Builder
import stl.error as error

from stl.parsing.ast_collection.core import Expr, STL_Expr
import stl.parsing.type as types
from typing import Optional
from abc import ABC

from stl.parsing.ast_collection.val import Id_Val
from stl.obj.result import STL_Expr_Eval_Result


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


class G_STL_Expr(Unary_STL_Expr, ABC):
    """support the globally STL expression"""

    def eval(self, eval_context):
        global_begin_time = eval_context.lookup(Id_Val("global_begin_time"))

        stl_expr_begin_time = self.begin_time.eval(eval_context)
        stl_expr_end_time = self.end_time.eval(eval_context)

        # calculate local (actual) time for conditional expression signal slicing
        local_begin_time = global_begin_time + stl_expr_begin_time
        local_end_time = global_begin_time + stl_expr_end_time

        # add local_begin_time and local_end_time to the context for accessing from conditional expression evaluation
        eval_context.add(Id_Val("local_begin_time"), local_begin_time)
        eval_context.add(Id_Val("local_end_time"), local_end_time)

        # todo return STL_Expr_Eval_Result in the conditional expression evaluation
        # return self.condition_expr.eval(eval_context)
        # todo: return Binary_Comp_Expr evaluation
        #print(STL_Expr_Eval_Result(True, 0.0))

        # todo: unimport STL_Expr_Eval_Result
        return STL_Expr_Eval_Result(True, 0.0)


    def eval2(self, eval_context):
        """add the pointer to the signal val to the context "$this$ -> signal_dict"""

        # debug
        # print(eval_context)

        # op, begin_expr, end_expr, condition_expr, time, signal):
        # evaluate the begin and the end time and time (time start for the signal)
        self.begin_expr = self.begin_expr.eval(eval_context)
        self.end_expr = self.end_expr.eval(eval_context)

        # print("signal val type: " + str(type(self.signal_val)))

        # cheat
        # convert both time to Python Int object
        self.begin_expr_int = self.begin_expr.to_py_obj()
        self.end_expr_int = self.end_expr.to_py_obj()

        # only keep the signal value between certain time interval
        # $this -> slided Signal val
        # add $this meta variable to the context that refer to the signal that is currently begin evaluated
        # sliced signal will be offset by self.time_expr
        offset_begin_expr_int = self.begin_expr_int + self.time_expr_int
        offset_end_expr_int = self.end_expr_int + self.time_expr_int

        # print("slice begin: " + str(offset_begin_expr_int))
        # print("slide end: " + str(offset_end_expr_int))
        eval_context.add(Meta_Id_Val("$this"),
                         self.signal_val.slice_signal_by_time_interval(offset_begin_expr_int, offset_end_expr_int))

        # print(eval_context)
        # for time in range(self.begin_expr_int + self.time_expr_int, self.end_expr_int + 1 + self.time_expr_int):
        # eval_context.add(Meta_Id_Val("$" + str(time) + ".content"), self.signal_val.get_signal_dict()[str(time)])

        # TODO: add values in the signal (self.signal) to the evaluation_context
        # loop through time_begin to time_end (int)

        # add to_py_obj(self) to primitive values and signal value (dictionary)
        # i.e. [2, 3] evaluate $2.param and $3.param

        # $1.param -> 7
        # $2.param -> 10
        # $3.param -> 15
        # Lexer: META_IDENTIFIER = $ IDENTIFIER
        # META_IDENTIFIER.eval(context, signal)
        # eval function will evaluate all META_IDENTIFIERS associated with the param

        # implicitly evaluate the meta variables
        self.condition_expr = self.condition_expr.eval(eval_context)

        return self.condition_expr


class F_STL_Expr(Unary_STL_Expr, ABC):
    """support the future STL expression"""
    pass


class X_STL_Expr(Unary_STL_Expr, ABC):
    """support the future STL expression"""

    # override Unary_STL_Expr init function, since X doesn't require the passing of a time interval.
    # instead it only requires a fixed time point
    def __init__(self, op, time_interval_expr, condition_expr):
        self.op = op
        self.time_interval_expr = time_interval_expr
        self.condition_expr = condition_expr

    def __str__(self):
        sb = String_Builder()
        sb.append("Unary_STL_Expr: ( ")
        sb.append(self.op)
        sb.append(" [")
        sb.append(str(self.time_interval_expr))
        sb.append("] (")
        sb.append(str(self.condition_expr))
        sb.append(")")

        return str(sb)

    def eval(self, eval_context):
        """add the pointer to the signal val to the context "$this$ -> signal_dict"""
        # op, time_interval_expr, condition_expr, time_expr, signal_val
        # debug
        # print(eval_context)

        # op, begin_expr, end_expr, condition_expr, time, signal):
        # evaluate the begin and the end time and time (time start for the signal)
        self.time_interval_expr = self.time_interval_expr.eval(eval_context)
        self.time_expr = self.time_expr.eval(eval_context)
        self.signal_val = self.signal_val.eval(eval_context)

        # print("signal val type: " + str(type(self.signal_val)))

        # convert both time to Python Int object
        self.time_interval_expr_int = self.time_interval_expr.to_py_obj()
        self.time_expr_int = self.time_expr.to_py_obj()

        # only keep the signal value between certain time interval
        # $this -> slided Signal val
        # add $this meta variable to the context that refer to the signal that is currently begin evaluated
        # sliced signal will be offset by self.time_expr
        # offset_begin_expr_int = self.begin_expr_int + self.time_expr_int
        # offset_end_expr_int = self.end_expr_int + self.time_expr_int
        offset_time_interval_int = self.time_interval_expr_int + self.time_expr_int

        # print("slice begin: " + str(offset_begin_expr_int))
        # print("slide end: " + str(offset_end_expr_int))
        eval_context.add(Meta_Id_Val("$this"), self.signal_val.slice_signal_by_time_interval(offset_time_interval_int,
                                                                                             offset_time_interval_int))

        # print(eval_context)
        # for time in range(self.begin_expr_int + self.time_expr_int, self.end_expr_int + 1 + self.time_expr_int):
        # eval_context.add(Meta_Id_Val("$" + str(time) + ".content"), self.signal_val.get_signal_dict()[str(time)])

        # TODO: add values in the signal (self.signal) to the evaluation_context
        # loop through time_begin to time_end (int)

        # add to_py_obj(self) to primitive values and signal value (dictionary)
        # i.e. [2, 3] evaluate $2.param and $3.param

        # $1.param -> 7
        # $2.param -> 10
        # $3.param -> 15
        # Lexer: META_IDENTIFIER = $ IDENTIFIER
        # META_IDENTIFIER.eval(context, signal)
        # eval function will evaluate all META_IDENTIFIERS associated with the param

        # implicitly evaluate the meta variables
        self.condition_expr = self.condition_expr.eval(eval_context)

        return self.condition_expr


class U_STL_Expr(Binary_STL_Expr, ABC):
    pass


class R_STL_Expr(Binary_STL_Expr, ABC):
    pass


class W_STL_Expr(Binary_STL_Expr, ABC):
    pass


class M_STL_Expr(Binary_STL_Expr, ABC):
    pass
