# Last Modified: 2020-12-15 17:32:51 EDT
# Simon Chu

import stl.error as error


class Type:
    """super type for all types"""

    def __init__(self, type_str):
        self.type_str = type_str

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.type_str == other.type_str
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return self.type_str != other.type_str
        else:
            # when other is None, self is of a type, return true
            return True

    def __str__(self):
        return self.type_str


class Int(Type):
    def __init__(self):
        super().__init__("Int")


class Boolean(Type):
    def __init__(self):
        super().__init__("Boolean")


class Float(Type):
    def __init__(self):
        super().__init__("Float")


class String(Type):
    def __init__(self):
        super().__init__("String")


class Signal(Type):
    def __init__(self):
        super().__init__("Signal")


class STL(Type):
    def __init__(self):
        super().__init__("STL")


class Unresolved(Type):
    def __init__(self):
        super().__init__("Unresolved")


def is_numeric(*type_objs):
    for type_obj in type_objs:
        if not (type_obj == Int() or type_obj == Float()):
            return False
    return True


class Type_Selector:
    """convert string-formatted types to type objects"""
    @staticmethod
    def select(type_str):
        if type_str == "INT":
            return Int()

        elif type_str == "BOOLEAN":
            return Boolean()

        elif type_str == "FLOAT":
            return Float()

        elif type_str == "STRING":
            return String()

        elif type_str == "STL":
            return STL()

        else:
            raise error.Type_Error("The type of " + type_str + " can not be resolved.")
