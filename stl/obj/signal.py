# Wed 2020-12-16 17:11:04 EDT
# Created by Simon Chu
# define the standard format for the signal

import json
import stl.error as err

from typing import Any
from collections import OrderedDict
import stl.obj.util as util
import logging
# JSON reference
# json.loads(JSON str) -> dict (decode)
# json.dumps(dict) -> JSON str (encode)
import stl.error as error
from typing import Optional

class Signal:
    """handles signal processing, conversion between JSON and Python dictionary
    internal representation

    TODO: add timestamp entry to extend the capability of continous time evaluation
    Attributes:
        data: a the python dictionary object that holds the signal
        next_index: the index of the next signal to be inserted

    Usage:
        constructor
        >>> sig = Signal() # empty signal
        >>> sig_from_json = Signal(json_str = '{"0": {"content": {"x": 0, "y": 0}}}')
        >>> sig_from_dict = Signal(py_dict = {"0": {"content": {"x": 0, "y": 0}}})
        >>> sig_from_dict_nested = Signal(py_dict = {"0": {"content": {"x": 0, "y": {"z": 0}}}, "1": {"content": {"x": 0, "y": {"z": 2}}}})
        >>> sig_from_dict_nested.lookup("y.z")
        [0, 2]
        append new elements to signal
        >>> sig.append(json_str = '{"x": 7, "y": 7}')
        >>> sig.append(py_dict = {"x": 7, "y": 7})
    """

    def __init__(self, json_str: str = "", py_dict: dict[str, Any] = dict()) -> None:
        """initialize the Signal object

        Note:
            user cannot supply both json_str and py_dict parameters at once.

        Args:
            json_str (str): optional JSON string
            py_dict (dict): optional Python dictionary object
            
        
        Raises:
            Signal_Error: An error occurred when create or modify a signal
        """

        # case when both parameters are not given
        if not json_str and not py_dict:

            # initialize empty data
            self._signal_data: dict = dict()

            # set the next index to be inserted (initialize to 0)
            self._next_index: int = 0

        # user supplied both JSON and Python dictionary data
        elif json_str and py_dict:
            raise err.Signal_Error(
                "Cannot supply both JSON and Python dictionary data in the signal constructor. Please try again.")

        # one of the data is given
        else:
            # case when only JSON string is given or only Python dictionary is given
            # convert the json_str to py_dict
            if json_str and not py_dict:
                py_dict = json.loads(json_str)

            # add py_dict to signal
            # verify the dictionary
            is_verified, msg = Signal.static_verify_signal(py_dict)

            if is_verified:
                self._signal_data = py_dict
            else:
                raise err.Signal_Error("Signal specified is Invalid! " + msg)

            self._next_index = len(self._signal_data)

    def is_empty(self) -> bool:
        return len(self._signal_data) == 0

    def print_json(self) -> None:
        """print the json string"""
        print(self._get_json_str())

    def append(self, json_str=None, py_dict=None) -> None:
        """append an element to the signal"""

        # case when both parameters are not given
        if not json_str and not py_dict:
            raise err.Signal_Error("No signal content data is supplied! Signal is not appended.")

        # case when both parameters are supplied
        elif json_str and py_dict:
            raise err.Signal_Error("Ambiguity when adding to Signal. Both json_str and py_dict are supplied.")

        # case when one of the data is given
        else:
            # if json_str is supplied, convert it to Python dictionary
            if json_str and not py_dict:
                py_dict = json.loads(json_str)

            # add the newly added signal content to the "content" field of the signal data
            # initialize dictionary in the specific index
            self._signal_data[str(self._next_index)] = dict()
            self._signal_data[str(self._next_index)]["content"] = py_dict

            # increment the next index to be inserted
            self._next_index += 1

    # =========== getter, setter, and deleter ==========
    @property
    def signal_data(self) -> dict[str, Any]:
        return self._signal_data

    @signal_data.setter
    def signal_data(self, signal_data) -> None:
        self._signal_data = signal_data
        self._next_index = len(signal_data)

    @signal_data.deleter
    def signal_data(self) -> None:
        del self._signal_data

    @property
    def json(self) -> str:
        return self._get_json_str()

    def _get_json_str(self) -> str:
        """return the sorted keys/indented string representation of the JSON
        
        Returns:
            str: a formatted JSON string converted from the Python dictionary (self._signal_data
        """

        # sort the signal_data by the int value of the index
        # https://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key
        ordered_signal_data = OrderedDict(sorted(self._signal_data.items(), key=lambda item: int(item[0])))
        # return json.dumps(self._signal_data, sort_keys=True, indent=4)

        return json.dumps(ordered_signal_data, indent=4)

    # =========== /getter, setter, and deleter ==========

    def verify_signal(self) -> tuple[bool, str]:
        return Signal.static_verify_signal(self._signal_data)

    @staticmethod
    def static_verify_signal(signal_data: dict[str, Any]) -> tuple[bool, str]:
        # TODO: verify weather all indices exists in the bound use signal_val.py #verify self._signal_data

        start_index: int = 0
        signal_length: int = len(signal_data)
        # end_index = signal_length - 1

        # verifier 1: index must start with index 0 and end with index "length"
        # ensure signal data (python dictionary) keys have continous indices

        # generated expected dictionary keys (with stringified keys)
        expected_dict_keys = [str(i) for i in range(start_index, signal_length)]

        # compare with listified signal_data
        if expected_dict_keys != list(signal_data.keys()):
            msg: str = "Missing index 0" if "0" not in signal_data.keys() else "Missing indices for signal"
            return False, msg

        # if verifier has reached the end, return True for verification
        return True, ""

    def get_quantifiable_keys(self) -> list[str]:
        # wrapper for get_quantifiable_keys for current object
        return Signal.static_get_quantifiable_keys(self._signal_data)

    @staticmethod
    def static_get_quantifiable_keys(signal_data: dict) -> list[str]:
        """return all the common keys <union> throughout all signal contents that can be quantifiable"""
        if len(signal_data) == 0:
            # return empty list if self._signal_data is empty
            return list()

        elif len(signal_data) > 1:
            # assume signal index start with 0
            # note that set() extract a set of dictionary keys
            signal_content_common_key_set = set(signal_data["0"]["content"])

            # get the intersection of all signal elements keys
            for signal_index in signal_data.keys():
                signal_content_common_key_set = signal_content_common_key_set.intersection(
                    set(signal_data[signal_index]["content"]))

            return list(signal_content_common_key_set)

        else:
            # when there is only 1 element in the signal_data, return its keys
            return signal_data["0"]["content"].keys()

    def __repr__(self) -> str:
        """representation of object, easy to debug on Python REPL"""
        return str(self)

    def __str__(self) -> str:
        """get the string representation"""
        return self._get_json_str()

    def __len__(self) -> int:
        return len(self._signal_data)

    # TODO: lookup signal by identifier's name
    def lookup(self, id_name: str, ll: bool = False, begin_time: Optional[int] = None, end_time: Optional[int] = None):
        """ll flag: low-level flag, whether to convert the looked up python object to low-level (parser/lexer level)
        objects

        Usage:
            >>> from stl.api import Signal
            >>> sig = Signal(py_dict = {"0": {"content": {"x": 0, "y": {"z": 0}}}, "1": {"content": {"x": 0, "y": {"z": 2}}}})
            >>> sig.lookup("y.z")
            [0, 2]
            >>> sig.lookup("y.z", ll=True)
            [<stl.parsing.ast_collection.val.Float_Val object at 0x108493d00>, <stl.parsing.ast_collection.val.Float_Val object at 0x108493cd0>]
        """
        result = list()
        id_name_split: list[str] = id_name.split(".")

        # by default, begin and end range are the bound for the entire signal
        begin_range = 0
        end_range = len(self) - 1

        if begin_time is not None:
            begin_range = begin_time

        if end_time is not None:
            end_range = end_time

        if begin_range > end_range:
            raise error.Signal_Error("begin_range of signal must be smaller than end_range of signal! " +
                                     "begin_range = " + str(begin_range) +
                                     "end_range = " + str(end_range))

        if begin_range >= len(self) or begin_range < 0 or end_range >= len(self) or end_range < 0:
            raise error.Signal_Error("Signal Index Out of Range! " +
                                     "begin_range = " + str(begin_range) +
                                     ", end_range = " + str(end_range) +
                                     ", signal length = " + str(len(self)))

        for i in range(begin_range, end_range + 1):  # note that the end time will be included
            current_signal_content = self._signal_data[str(i)]["content"]

            try:
                for key in id_name_split:
                    # print(key)
                    current_signal_content = current_signal_content[key]
            except Exception as e:
                logging.exception(e)

            if ll:
                result.append(util.py_obj_to_ll_obj(current_signal_content, int_to_float=True))
            else:
                result.append(current_signal_content)

        return result
