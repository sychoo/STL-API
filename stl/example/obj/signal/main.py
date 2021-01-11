
# Thu Dec 17 13:43:57 EST 2020
# Simon Chu

from typing import Any

from stl.api import Signal
import stl.error as err


# sample Python program to demonstrate the usage of Signal api
# note that signal1, 2, 3, and 4 are equivalent upon creation

# ============== test signal creation (constructor) =================

# appending signal content using JSON string
signal1: Signal = Signal()
signal1.append(json_str='''{ "param" : 7 }''')
signal1.append(json_str='''{ "param" : 10 }''')

# appending signal content using Python dictionary
signal2: Signal = Signal()
signal2.append(py_dict={"param" : 7})
signal2.append(py_dict={"param" : 10})

# create a signal from a existing JSON-formatted signal
json_str = """
    {
        "0" : {
            "content" : {
                    "param" : 7
            }
        },

        "1" : {
            "content" : {
                    "param" : 10
            }
        }
    }
"""
signal3: Signal = Signal(json_str=json_str)

# create a signal from a python dictionary formatted signal
py_dict: dict[str, Any] = {
    "0" : {
        "content" : {
                "param" : 7
        }
    },

    "1" : {
        "content" : {
                "param" : 10
        }
    }
}

signal4: Signal = Signal(py_dict=py_dict)

assert signal1.json == signal2.json
assert signal1.json == signal3.json
assert signal1.json == signal4.json

# note that signal1, 2, 3, 4 are equivalent

# must throw an exception when there are ambiguity in constructing
try:
    signal_invalid: Signal = Signal(json_str=json_str, py_dict=py_dict)
except Exception as e:
    # check whether the exception raised is Signal_Error
    assert e.__class__ == err.Signal_Error

# ============== test get_quantifiable_keys ==========

json_str_2 = """
    {
        "0" : {
            "content" : {
                    "param" : 7
            }
        },

        "1" : {
            "content" : {
                    "param" : 10,
                    "param_2" : 15
            }
        }
    }
"""

signal5 = Signal(json_str_2)

assert signal5.get_quantifiable_keys() == ["param"]


# ====================== test verify_signal =================
json_str_invalid_1 = """
    {
        "1" : {
            "content" : {
                    "param" : 7
            }
        },

        "2" : {
            "content" : {
                    "param" : 10,
                    "param_2" : 15
            }
        }
    }
"""

json_str_invalid_2 = """
    {
        "0" : {
            "content" : {
                    "param" : 7
            }
        },

        "2" : {
            "content" : {
                    "param" : 10,
                    "param_2" : 15
            }
        }
    }
"""

try:
    signal_invalid = Signal(json_str_invalid_1)
except Exception as e:
    # check whether the exception raised is Signal_Error
    assert e.__class__ == err.Signal_Error

try:
    signal_invalid = Signal(json_str_invalid_2)
except Exception as e:
    # check whether the exception raised is Signal_Error
    assert e.__class__ == err.Signal_Error

