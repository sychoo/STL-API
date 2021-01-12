from rply import ParserGenerator
from stl.parsing.lexer import Lexer
import stl.parsing.ast as AST
import stl.tool as tool
import stl.error as error
import stl.parsing.type as types


class Parser:
    """parser class

    Acronyms:
        expr : expression
        val : value

    Attributes:
        self._parser: the parser that is built
    """

    def __init__(self):
        # define the reserved words for the parser
        # list of all token names accepted by the parser.
        pg = ParserGenerator([

            # reserved stl operators
            "GLOBALLY",
            "EVENTUALLY",

            # logical operators
            "LOGICAL_EQUALS",
            "LOGICAL_AND",
            "LOGICAL_OR",
            "LOGICAL_IMPLIES",
            "LOGICAL_NOT",

            # binary operators for numerical (Int, Float) operations
            "GREATER_EQUAL",
            "LESS_EQUAL",
            "GREATER",
            "LESS",

            # binary logical operators for both numerical (Int, Float) and Boolean operations
            "EQUAL_EQUAL",
            "NOT_EQUAL",

            # content grouping structures
            "L_PAREN",
            "R_PAREN",
            "L_SQ_BRACE",
            "R_SQ_BRACE",

            # primary arithmetic operators
            "EQUAL",
            "PLUS",
            "MINUS",
            "MULTIPLY",
            "DIVIDE",

            # separators/delimiters
            "COMMA",
            # "NEWLINE",

            # values
            "FLOAT",
            "INT",
            "STRING",
            "BOOLEAN",

            # identifiers
            "IDENTIFIER",
        ],

            # A list of precedence rules with ascending precedence, to disambiguate ambiguous production rules.
            # top has the highest precedence
            # `nonassoc` for non-associative tokens
            #
            # references:
            # https://www.mathcs.emory.edu/~valerie/courses/fall10/155/resources/op_precedence.html
            precedence=[
                ('left', ['L_PAREN', 'R_PAREN']),
                ('left', ['PLUS', 'MINUS']),
                ('left', ['MULTIPLY', 'DIVIDE']),
                ('left', ['GREATER_EQUAL', 'LESS_EQUAL', 'GREATER', 'LESS', 'EQUAL_EQUAL', 'NOT_EQUAL']),
                ('left', ['LOGICAL_NOT']),
                ('left', ['LOGICAL_AND']),
                ('left', ['LOGICAL_OR']),
                ('left', ['LOGICAL_IMPLIES']),
                ('left', ['LOGICAL_EQUALS']),
                ('right', ['EQUAL']),
            ])

        # section to define the parser

        @pg.production("main : expr")
        def main_entry(s):
            """top level expressions"""
            return s[0]

        @pg.production("expr : L_PAREN expr R_PAREN")
        def parent_expr(s):
            """extract parenthesis content"""
            return s[1]

        @pg.production("expr : expr GREATER expr")
        @pg.production("expr : expr GREATER_EQUAL expr")
        @pg.production("expr : expr LESS expr")
        @pg.production("expr : expr LESS_EQUAL expr")
        @pg.production("expr : expr EQUAL_EQUAL expr")
        @pg.production("expr : expr EQUAL expr")  # "=" equivalent to "==" for comparison
        @pg.production("expr : expr NOT_EQUAL expr")
        def binary_comp_expr(s):
            """binary comparison expressions"""
            return AST.Binary_Comp_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])

        @pg.production("expr : LOGICAL_NOT expr")
        def unary_logic_expr(s):
            """unary logical expressions"""
            return AST.Unary_Logic_Expr(s[0].getstr(), s[0].gettokentype(), s[1])

        @pg.production("expr : expr LOGICAL_AND expr")
        @pg.production("expr : expr LOGICAL_OR expr")
        @pg.production("expr : expr LOGICAL_IMPLIES expr")
        @pg.production("expr : expr LOGICAL_EQUALS expr")
        def binary_logic_expr(s):
            """binary logical expressions"""
            return AST.Binary_Logic_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])

        @pg.production("expr : PLUS expr")
        @pg.production("expr : MINUS expr")
        def unary_arith_expr(s):
            """unary arithmetic expressions"""
            return AST.Unary_Arith_Expr(s[0].getstr(), s[0].gettokentype(), s[1])

        @pg.production("expr : expr PLUS expr")
        @pg.production("expr : expr MINUS expr")
        @pg.production("expr : expr DIVIDE expr")
        @pg.production("expr : expr MULTIPLY expr")
        def binary_arith_expr(s):
            """binary arithmetic expressions"""
            return AST.Binary_Arith_Expr(s[1].getstr(), s[1].gettokentype(), s[0], s[2])

        @pg.production("val : IDENTIFIER")
        def var_expr(s):
            return AST.Id_Val(s[0].getstr())

        @pg.production("expr : IDENTIFIER L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN")
        @pg.production("expr : GLOBALLY L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN")
        @pg.production("expr : EVENTUALLY L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN")
        def unary_stl_expr_1(s):
            """unary STL expressions (G: Globally/Always, F: Eventually)

            Example:
               G[1, 10](x > y)
               [][1, 10](x > y) : equivalent to G[1, 10](x > y)

               F[1, 10](x > y)
               <>[1, 10](x, y)  : equivalent to F[1, 10](x > y)

            Reference:
                FLTL: https://www.doc.ic.ac.uk/~jnm/book/ltsa/Appendix-A-2e.html
            """

            # obtain the operator of the STL expression
            op_type = s[0].gettokentype()
            op = s[0].getstr()

            if op == "G" or op_type == "GLOBALLY":
                return AST.G_STL_Expr(op, s[2], s[4], s[7])
            elif op == "F" or op_type == "EVENTUALLY":
                return AST.F_STL_Expr(op, s[2], s[4], s[7])
            else:
                raise error.Parser_Error("STL Operator: " + op + " not recognized.")

        @pg.production(
            "expr : IDENTIFIER L_SQ_BRACE expr R_SQ_BRACE L_PAREN expr R_PAREN")
        def unary_stl_expr_2(s):
            """unary STL expressions (X: Next)

            Example:
                X[1](x > y)
            """
            op = s[0].getstr()
            if op == "X":
                return AST.X_STL_Expr(op, s[2], s[5])

        @pg.production(
            "expr : L_PAREN expr R_PAREN IDENTIFIER L_SQ_BRACE expr COMMA expr R_SQ_BRACE L_PAREN expr R_PAREN")
        def binary_stl_expr(s):
            """binary STL expressions (U: Until, R: Release, W: Weak until, M: Strong release)

            Example:
                (x > y) U [0, 10] (x < y)
                (x > y) R [0, 10] (x < y)
                (x > y) W [0, 10] (x < y)
                (x > y) M [0, 10] (x < y)
            """

            op = s[3].getstr()

            if op == "U":
                return AST.U_STL_Expr(s[3].getstr(), s[5], s[7], s[1], s[10])
            elif op == "R":
                return AST.R_STL_Expr(s[3].getstr(), s[5], s[7], s[1], s[10])
            elif op == "W":
                return AST.W_STL_Expr(s[3].getstr(), s[5], s[7], s[1], s[10])
            elif op == "M":
                return AST.M_STL_Expr(s[3].getstr(), s[5], s[7], s[1], s[10])

        @pg.production("expr : val")
        def single_val_expr(s):
            """single value expression"""
            return s[0]

        @pg.production("val : INT")
        def int_val(s):
            """int values"""
            return AST.Int_Val(s[0].getstr())

        @pg.production("val : FLOAT")
        def float_val(s):
            """float values"""
            return AST.Float_Val(s[0].getstr())

        @pg.production("val : STRING")
        def string_val(s):
            """string values"""
            return AST.String_Val(s[0].getstr())

        @pg.production("val : BOOLEAN")
        def boolean_val(s):
            """boolean values"""
            return AST.Boolean_Val(s[0].getstr())

        self._parser = pg.build()

    # return the parsedAST
    def parse(self, token_stream):
        return self._parser.parse(token_stream)


def main():
    lexer = Lexer()
    parser = Parser()

    for expr in tool.repl(header="Please enter STL expressions to be parsed."):

        token_stream = lexer.lex(expr)
        parsed_expr = parser.parse(token_stream)
        print(parsed_expr)


if __name__ == "__main__":
    main()
