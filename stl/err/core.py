import stl.tool as tool


class Error(RuntimeError):
    """super class that supports printing error message in bold red texts
    
    Note:
        Error class is essentially a wrapper class for RuntimeError
    """
    def __init__(self, msg):
        tool.print_error(msg)