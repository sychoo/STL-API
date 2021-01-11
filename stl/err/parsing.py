# 2020-12-23 12:20:13 EST

from stl.err.core import Error


class Parser_Error(Error):
    """super class for signal-related errors"""
    pass


class Type_Error(Error):
    """super class for all type-related error"""
    pass