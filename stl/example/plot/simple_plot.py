# Created by Simon Chu
# Program to plot -(x-4)^2 + 2x - 4. The x axis represent time (t), and the y axis represent an arbitrary value of a
# signal elements. The program then enters REPL loop to allow user to specify STL expressions to evaluate with respect
# to the signal represented by the graph

import matplotlib.pyplot as plt
import numpy as np

from stl.api import Signal, STL

import stl.tool as tool


def graph(formula: str, x_range: range) -> Signal:
    """plot a simple graph based on the formula and range of x coordinates"""
    x = np.array(x_range)
    y = eval(formula)

    plt.plot(x, y, '-ok', color='black')  
    
    plt.xlabel("Time (t)")
    plt.ylabel("Value (y)")
    plt.grid()

    signal = Signal()

    # enhance graph and process signal
    for x_coord, y_coord in zip(x, y):  # zip makes x, y pairs of tuple

        # plot the coordinate values as texts
        plt.text(x_coord, y_coord, '({}, {})'.format(x_coord, y_coord))

        # convert the coordinate information to Signal object
        # note that JSON does not recognize Numpy int64 datatype, thus have to convert to int type
        signal.append(py_dict={"y": int(y_coord)})

    # display the signal
    tool.print_warning("Signal is displayed below.")

    # non-blocking mode, will display until input() is terminated
    plt.show(block=False)

    return signal


def evaluate(time_begin: int, signal: Signal):

    # start the REPL mode user input evaluation expressions
    for stl_expr in tool.repl(header="Please enter STL expressions to be evaluated."):
        # TODO: call STL API to evaluate the STL expression stl_expr with respect to the signal
        # print(stl_expr)
        stl_spec = STL(stl_expr)
        stl_eval = stl_spec.eval(time_begin, signal)
        print(stl_eval)


def main():
    time_begin = 0
    signal = graph('-(x-4)**2+2*x-4', range(0, 11))  # plot default graph -(x-4)^2 + 2x - 4
    evaluate(time_begin, signal)


if __name__ == '__main__':
    main()

# properties to be checked
#
# -(x-4)^2+2x-4
#
# G[0, 10](y >= -20)
# G[0, 10](|y| <= 20) // absolute value
# 
# F[0, 10](y == 5)
# F[0, 10](|y| = 20) // absolute value
#
# X[0](y == -11)
# X[5](y < 5)
#
# (y > -4)U[5, 10](y <= -4)
