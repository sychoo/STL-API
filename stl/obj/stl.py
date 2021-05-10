# Created by Simon Chu
# contains all objects related to the evaluation of STL expressions

from stl.parsing.lexer import Lexer
from stl.parsing.parser import Parser
from stl.obj.signal import Signal
from stl.parsing.interpreter import Interpreter
from stl.obj.result import Eval_Result
from typing import Optional
import stl.error as error
import copy

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

    def __init__(self, value: Optional[str], parsed_expr = None):
        
        self.value_val = value  # do not evaluate when user has not passed in the time_begin and signal

        if parsed_expr == None:
            # lex and parse the token immediately upon creation of STL object
            self.token_stream = self.lexer.lex(self.value)
            self.parsed_expr = self.parser.parse(self.token_stream)
        else:
            self.parsed_expr = parsed_expr

        self.eval_result_cache_val = None

    def eval(self, time_begin: int, signal: Signal) -> Eval_Result:
        # interpreter = Interpreter(time_begin, signal, self.lexer, self.parser)
        interpreter = Interpreter(time_begin, signal)
        # return interpreter.interpret(self.value)
        return interpreter.interpret(self.parsed_expr)

    def weaken(self, option: str, *args) -> "STL": # return AST node of modified STL expression
        """weaken the STL formula, then """

        # note that here use deep copy module
        # https://www.educative.io/edpresso/how-to-make-a-deep-copy-in-python
        copied_parsed_expr = copy.deepcopy(self.parsed_expr)
        copied_parsed_expr.weaken(option, *args)
        return STL(None, copied_parsed_expr)

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

    def __str__(self):
        return "original input expr : " + str(self.value) + "\nparsed         expr : " + str(self.parsed_expr) + "\n"
        
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
