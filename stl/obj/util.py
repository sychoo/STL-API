# Simon Chu
# Mon Jan 11 18:39:08 EST 2021

from typing import Union
from stl.parsing.ast_collection.val import Int_Val, Float_Val, Boolean_Val, String_Val
from stl.parsing.ast_collection.core import Val


def py_obj_to_ll_obj(val: Union[int, float, bool, str], int_to_float: bool = False) -> Val:
    """convert the entry to the signal to low-level object for lexer and parser to floating point numbers

    note that signal entries consists of Integers and Floating-point numbers represented in strings

    int_to_float flag is to determine whether all integers are converted to float

    Usage:
        >>> py_obj_to_ll_obj(2)
        stl.parsing.ast_collection.val.Int_Val( 2 )
        >>> py_obj_to_ll_obj(2, int_to_float=True)
        stl.parsing.ast_collection.val.Float_Val( 2.0 )
    """
    # try:
    #     float(str)
    # except ValueError:
    #     raise error.Signal_Error("Invalid Signal Entry. Unable to convert entry to float type")
    #
    # return Float_Val(val)

    if isinstance(val, bool):
        return Boolean_Val(py_obj=val)

    elif isinstance(val, str):
        return String_Val(py_obj=val)

    if int_to_float:
        if isinstance(val, int) or isinstance(val, float):
            return Float_Val(py_obj=float(val))  # convert Python int type to float type
    else:
        if isinstance(val, int):
            return Int_Val(py_obj=val)

        elif isinstance(val, float):
            return Float_Val(py_obj=val)




