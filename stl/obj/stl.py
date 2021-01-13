# Created by Simon Chu
# contains all objects related to the evaluation of STL expressions

from stl.parsing.lexer import Lexer
from stl.parsing.parser import Parser
from stl.obj.signal import Signal
from stl.parsing.interpreter import Interpreter
from stl.obj.result import Eval_Result
from typing import Optional
import stl.error as error


class STL:
    """stores STL expression, note that STL is an immutable object

    Usage:
        >>> stl_expr = STL("G[0, 10]($x > $y)")
        >>> signal = Signal(py_dict = {"0": {"content": {"x": 0, "y": 0}}})
        >>>
        >>> stl_eval_expr = stl_expr.eval(0, signal) # store results in a temporary data structure for quicker access
        >>> stl_eval_expr.satisfy()
        False
        >>> # Alternatively
        >>> stl_expr.satisfy(0, signal) # does not store results
        False
    """

    lexer = Lexer()
    parser = Parser()

    def __init__(self, value: str):
        self.value_val = value  # do not evaluate when user has not passed in the time_begin and signal
        self.eval_result_cache_val = None

    def eval(self, time_begin: int, signal: Signal) -> Eval_Result:
        interpreter = Interpreter(time_begin, signal, self.lexer, self.parser)
        return interpreter.interpret(self.value)

    def satisfy(self, time_begin: Optional[int] = None, signal: Optional[Signal] = None) -> bool:
        if self.eval_result_cache is not None:
            return self.eval_result_cache.satisfy
        else:
            if time_begin is not None and signal is not None:
                return self.eval(time_begin, signal).satisfy
            else:
                raise error.STL_Error(
                    "No Cached Evaluation Result Available." +
                    "Please Supply time_begin and signal parameter for evaluations")

    def robustness(self, time_begin: Optional[int] = None, signal: Optional[Signal] = None) -> float:
        if self.eval_result_cache is not None:
            return self.eval_result_cache.robustness
        else:
            if time_begin is not None and signal is not None:
                return self.eval(time_begin, signal).robustness
            else:
                raise error.STL_Error(
                    "No Cached Evaluation Result Available." +
                    "Please Supply time_begin and signal parameter for evaluations")

    def probability(self, time_begin: Optional[int] = None, signal: Optional[Signal] = None):
        if self.eval_result_cache is not None:
            return self.eval_result_cache.probability
        else:
            if time_begin is not None and signal is not None:
                return self.eval(time_begin, signal).probability
            else:
                raise error.STL_Error(
                    "No Cached Evaluation Result Available." +
                    "Please Supply time_begin and signal parameter for evaluations")

    @property
    def value(self):
        return self.value_val

    @value.setter
    def value(self, value: str):
        self.value_val = value

    @property
    def eval_result_cache(self):
        return self.eval_result_cache_val

    @eval_result_cache.setter
    def eval_result_cache(self, eval_result_cache: Eval_Result):
        self.eval_result_cache_val = eval_result_cache
