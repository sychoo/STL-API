# Created by Simon Chu
# Thu Jan  7 13:34:55 EST 2021
# interpreter to demonstrate simple arithmetic expression interpretation with a trivial signal

from stl.parsing.lexer import Lexer
from stl.parsing.parser import Parser

import stl.parsing.ast as ast
import stl.parsing.context as ctx
from stl.parsing.ast_collection.val import Int_Val

import stl.tool as tool
from stl import Signal
import stl.parsing.type as types

from typing import Optional
from stl.obj.result import Eval_Result, Eval_Result_Transformer

"""
Usage:
    >>> G[0, 1](x > y)
    false
"""


class Interpreter:

    def __init__(self, global_begin_time: int, signal: Signal,
                #  lexer: Optional[Lexer] = Lexer(), parser: Optional[Parser] = Parser(),
                # parsed_expr, 
                  debug: bool = False):
        self.global_begin_time = global_begin_time
        self.signal = signal
        # self.lexer = lexer
        # self.parser = parser
        self.debug = debug

    def interpret(self, parsed_expr) -> Eval_Result:
        """start the evaluation process, and return the evaluation result"""
        # token_stream = self.lexer.lex(expr)
        # parsed_expr = self.parser.parse(token_stream)

        # initialize type context, type check the AST
        type_ctx = ctx.Type_Context.get_empty_context()
        type_ctx.add(ast.Id_Val("global_begin_time"), types.Int())
        type_ctx.add(ast.Id_Val("signal"), types.Signal())
        parsed_expr.type_check(type_ctx)

        # initialize the evaluation context, evaluate the AST
        eval_ctx = ctx.Eval_Context.get_empty_context()
        eval_ctx.add(ast.Id_Val("global_begin_time"), Int_Val(py_obj=self.global_begin_time))
        eval_ctx.add(ast.Id_Val("signal"), self.signal)

        low_level_eval_result = parsed_expr.eval(eval_ctx)

        if self.debug:  # debug mode will print low-level result (parser-level AST representation)
            return low_level_eval_result

        else:  # non-debug mode will transform the result to high-level result (api)
            high_level_eval_result = Eval_Result_Transformer(low_level_eval_result).transform()
            return high_level_eval_result


def main():
    global_begin_time = 0
    tool.print_warning("Time Start: " + str(global_begin_time))

    signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}}, "1": {"content": {"x": 2, "y": 1}}})

    # signal generated:
    # {
    #     "0": {
    #         "content": {
    #             "x": 1,
    #             "y": 2
    #         }
    #     },
    #     "1": {
    #         "content": {
    #             "x": 2,
    #             "y": 1
    #         }
    #     }
    # }

    tool.print_warning("Signal:")
    print(signal)

    # note that debug mode allows interpreter to print the low-level AST instead of the high-level Eval_Result
    interpreter = Interpreter(global_begin_time, signal, debug=False)  # also initialize lexer and parser

    for expr in tool.repl(header="Please enter STL expressions to be interpreted."):
        print(interpreter.interpret(expr))


if __name__ == "__main__":
    main()
