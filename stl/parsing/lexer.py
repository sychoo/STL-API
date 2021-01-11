# Simon Chu
# Created on Sun Nov  1 18:32:24 EST 2020
# Modified on Wed 2021-01-06 09:30:08
#
# lexer.py
# lexer definition file
#
# reference:
# https://rply.readthedocs.io/en/latest/

from rply import LexerGenerator
import stl.tool as tool


class Lexer:
    """lexical analyzer class

    Attributes:
            self._lexer: the lexer that is built
    """

    def __init__(self):
        """Initialize Lexical Analyzer"""

        lg = LexerGenerator()
        # lg.ignore(r"(\t|\ |\v|\r)+")  # ignore all whitespaces except newline
        lg.ignore(r"\s+")

        # reserved stl operators
        lg.add("GLOBALLY", r"\[\]")
        lg.add("EVENTUALLY", r"\<\>")

        # logical operators
        lg.add("LOGICAL_EQ", r"\<\=\>")
        lg.add("LOGICAL_AND", r"\&\&")
        lg.add("LOGICAL_OR", r"\|\|")
        lg.add("LOGICAL_IMPLIES", r"\=\>")

        # binary operators for numerical (Int, Float) operations
        lg.add("GREATER_EQUAL", r"\>\=")
        lg.add("LESS_EQUAL", r"\<\=")
        lg.add("GREATER", r"\>")
        lg.add("LESS", r"\<")

        # binary logical operators for both numerical (Int, Float) and Boolean operations
        lg.add("EQUAL_EQUAL", r"\=\=")
        lg.add("NOT_EQUAL", r"\!\=")

        # additional logic operators
        lg.add("LOGICAL_NOT", r"\!")  # must be placed after NOT_EQUAL (!=) due to conflict

        # content grouping structures
        lg.add("L_PAREN", r"\(")
        lg.add("R_PAREN", r"\)")
        lg.add("L_SQ_BRACE", r"\[")
        lg.add("R_SQ_BRACE", r"\]")

        # primary arithmetic operators
        lg.add("EQUAL", r"\=")
        lg.add("PLUS", r"\+")
        lg.add("MINUS", r"-")
        lg.add("MULTIPLY", r"\*")
        lg.add("DIVIDE", r"/")

        # separators/delimiters
        lg.add("COMMA", r",")
        # lg.add("NEWLINE", r"\n")

        # values
        # support 1.2, 1E7, 1.E7, 1.02E2 (equivalent to 102.0) as floating-point numbers
        lg.add("FLOAT", r"[0-9]*(\.[0-9]+([eE][-+]?[0-9]+)?)|([0-9]+([eE][-+]?[0-9]+))")
        lg.add("INT", r"\d+")
        lg.add("STRING", r"\".*\"")
        lg.add("BOOLEAN", r"true|false")

        # identifiers (variable identifiers/type identifiers/STL operator identifier)
        # note that STL operators are included in identifiers to avoid variable name conflict with the operator name
        lg.add("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_.]*")  # identifier cannot begin with numerical values

        # build the lexer
        self._lexer = lg.build()

    # parse raw program string to token stream
    def lex(self, stl_expr):
        return self._lexer.lex(stl_expr)


def main():
    # create lexer
    lexer = Lexer()

    for expr in tool.repl(header="Please enter STL expressions to be lexically analyzed."):

        token_stream = lexer.lex(expr)

        for token in token_stream:
            print(token)


if __name__ == "__main__":
    main()
