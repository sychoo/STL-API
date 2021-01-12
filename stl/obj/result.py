# Created by Simon Chu
# Thu Jan  7 15:54:28 EST 2021

from typing import Optional, Union
import stl.error as error
from abc import ABCMeta, abstractmethod, ABC
from stl.tool import String_Builder
from stl.parsing.ast_collection.core import Val

from typing import Any, Optional, Union


class Eval_Result(metaclass=ABCMeta):
    """super class for all the evaluation result"""

    # abstract class -> satisfy: bool, robustness: float, probability: Optional[float]
    # Eval_Result can be either a stl.parsing.AST_Collections.val
    # or STL_Eval_Result

    def __init__(self,
                 value: Any = None,
                 satisfy: Optional[bool] = None,
                 robustness: Optional[Union[float, int]] = None,
                 probability: Optional[Union[float, int]] = None):
        self.value_val = value
        self.satisfy_val = satisfy
        self.robustness_val = robustness
        self.probability_val = probability

    @abstractmethod
    def __str__(self):
        """get the string representation of the evaluation result"""
        pass

    #######################
    # getters and setters #
    #######################

    @property
    def value(self):
        if self.value_val is not None:
            return self.value_val

    @value.setter
    def value(self, value: Any):
        self.value_val = value

    @property
    def satisfy(self):
        if self.satisfy_val is not None:
            return self.satisfy_val

    @satisfy.setter
    def satisfy(self, satisfy: bool):
        self.satisfy_val = satisfy

    @property
    def robustness(self):
        if self.robustness_val is not None:
            return self.robustness_val

    @robustness.setter
    def robustness(self, robustness: Union[float, int]):
        self.robustness_val = robustness

    @property
    def probability(self):
        if self.probability_val is not None:
            return self.probability_val

    @probability.setter
    def probability(self, probability: Union[float, int]):
        self.probability_val = probability


class Val_Eval_Result(Eval_Result, ABC):
    """wrapper class for the low-level Val object"""

    def __init__(self, value: Val):
        super().__init__(value=value.to_py_obj())

    def __str__(self):
        return str(self.value_val)


class STL_Expr_Eval_Result(Eval_Result, ABC):
    """stores the evaluation result for STL expressions

    Usage:
        >>> result_1 = STL_Expr_Eval_Result(True, 1.0, 0.99)
        >>> print(result_1)
        satisfy     : True
        robustness  : 1.0
        probability : 0.99
        >>> result_1.satisfy
        True
        >>> result_2 = STL_Expr_Eval_Result(True, 2.0)
        >>> result_2.probability
        Result_Error("probability attribute does not exist.")
        >>> result_3 = STL_Expr_Eval_Result(False, 1.0)
        Result_Error("satisfaction value does not match the robustness value")
        >>> result_4 = STL_Expr_Eval_Result(False, -1.0, 3.0)
        Result_Error("probability must be between 0 and 1")

    """

    def __init__(self, satisfy: bool,
                 robustness: float,
                 probability: Optional[float] = None):
        super().__init__(satisfy=satisfy, robustness=robustness, probability=probability)

        # ensure satisfaction matches the robustness
        if (satisfy and robustness < 0) or (not satisfy and robustness > 0):
            raise error.Result_Error("satisfaction value does not match the robustness value")

        # probability must be between 0 and 1
        if probability:
            if 0 <= probability <= 1:
                pass
            else:
                raise error.Result_Error("probability must be between 0 and 1")

    def __str__(self):
        sb = String_Builder()
        sb.append("satisfy     : ")
        sb.append(str(self.satisfy_val))
        sb.append("\n")

        sb.append("robustness  : ")
        sb.append(str(self.robustness_val))

        if self.probability:
            sb.append("\n")
            sb.append("probability : ")
            sb.append(str(self.probability_val))
        return str(sb)


class Eval_Result_Transformer:
    """
    detect type of evaluation result and transform the low-level (parsing-level) evaluation result
    to high-level (api-level) evaluation result. Note that

    Usage:
        >>> from stl.parsing.ast import Int_Val
        >>> integer = Int_Val(0)
        >>> integer_transformed = Eval_Result_Transformer(integer).transform()
        >>> print(integer_transformed)
        0
        >>> py_integer = Val_Eval_Result(integer)
        >>> py_integer_transformed = Eval_Result_Transformer(integer).transform()
        >>> type(py_integer_transformed)
        Val_Eval_Result

    """

    def __init__(self, eval_result: Union[Val, STL_Expr_Eval_Result]):
        self.eval_result = eval_result

    def transform(self) -> Eval_Result:
        if isinstance(self.eval_result, Val):
            return Val_Eval_Result(self.eval_result)
        elif isinstance(self.eval_result, Eval_Result):
            return self.eval_result
        # list is not an internal type. bypass, simply print out the list
        elif isinstance(self.eval_result, list):
            return self.eval_result
        else:
            raise error.Result_Error("Unsupported transformation of evaluation result of Type " +
                                     self.eval_result.__class__.__name__)


def main():
    # testing STL_Expr_Eval_Result
    result_1 = STL_Expr_Eval_Result(True, 1.0, 0.99)
    print(result_1)
    '''
    satisfy: True
    robustness: 1.0
    probability: 0.99
    '''

    print(result_1.satisfy)
    '''
    True
    '''

    result_2 = STL_Expr_Eval_Result(True, 2.0)
    try:
        print(result_2.probability)
    except error.Result_Error as e:
        pass
    '''
    Result_Error("probability attribute does not exist.")
    '''

    try:
        STL_Expr_Eval_Result(False, 1.0)
    except error.Result_Error as e:
        pass
    '''
    Result_Error("satisfaction value does not match the robustness value")
    '''

    try:
        STL_Expr_Eval_Result(False, -1.0, 3.0)
    except error.Result_Error as e:
        pass
    '''
    Result_Error("probability must be between 0 and 1")
    '''


if __name__ == "__main__":
    main()
