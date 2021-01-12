# Simon Chu
# tools.py
# Mon 2020-11-02 13:42:26 EST

from termcolor import colored
from sys import stdout
from io import StringIO
from typing import Optional

import logging  # for logging error messages
from signal import signal, SIGINT  # for gracefully start a new line when ctrl-C happens



# ========= PRINT TOOLS (TO STDOUT) =========
def print_error(error_msg: str, end: str = "\n") -> None:
    """print error message, this will prepend Error: to the string given in bolded red"""
    error_msg += end
    stdout.write(colored(error_msg, "red", attrs=["bold"]))


def print_warning(warning_msg: str, end: str = "\n") -> None:
    """print warning message, this will print the given string in bolded yellow"""
    warning_msg += end
    stdout.write(colored(warning_msg, "yellow", attrs=["bold"]))


def print_success(success_msg: str, end: str = "\n") -> None:
    """print warning message, this will print the given string in bolded yellow"""
    success_msg += end
    stdout.write(colored(success_msg, "green", attrs=["bold"]))


# ========= /PRINT TOOLS (TO STDOUT) =========


def str_to_bool(bool_str: str):
    if bool_str == "true":
        return True
    elif bool_str == "false":
        return False
    else:
        raise RuntimeError("string value \"" + bool_str + "\" is not recognized and cannot be converted to boolean.")


def bool_to_str(bool):
    if bool == True:
        return "true"
    elif bool == False:
        return "false"
    else:
        raise RuntimeError("boolean value \"" + bool + "\" is not recognized and cannot be converted to string.")


def check_token_length(token_stream):
    """find the number of tokens. note that the token stream pointer will not be reset"""
    token_num = token_length(token_stream)

    if token_num <= 0:
        exit(0)


def token_length(token_stream):
    """find the number of tokens"""
    token_num = 0
    for _ in token_stream:
        token_num += 1

    return token_num




def repl(header: Optional[str] = None) -> str:
    """enter a REPL (read-eval-print loop)

    Usage:
        >>> for usr_input in repl():
        >>>     # do something with the input

    TODO: add feature to retrieve previous input via up arrow
    """

    # start a new empty line when users click ctrl-C
    def handler(signal_received, frame):
        stdout.write("\nKeyboardInterrupt")
        stdout.write("\n")
        print_success(">>> ", end="")
        stdout.flush()

    # print user-supplied header
    if header:
        print_warning(header)

    while True:
        signal(SIGINT, handler)  # run the handler() function when SIGINT is received
        print_success(">>> ", end="")

        try:
            user_input = input()
            stdout.flush()
            yield user_input  # return the value to the caller

        except EOFError:  # exit when EOF (end-of-file) is reached
            stdout.write("\nEOF\n")
            exit(0)

        except Exception as e:  # catch all other exceptions
            pass
            # print(e)
            # logging.exception(e, exc_info=True)  # capture stack traces


# https://stackoverflow.com/questions/2414667/python-string-class-like-stringbuilder-in-c
class String_Builder:
    """accumulate string more efficiently"""
    string = None

    def __init__(self):
        self.string = StringIO()

    def append(self, string: str):
        self.string.write(string)

    def __str__(self):
        return self.string.getvalue()

