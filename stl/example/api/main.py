from stl.api import STL, Signal

# TODO: create a signal and time_begin (like the Interpreter) and evaluate some STL Formulas
time_begin = 0
signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}}, "1": {"content": {"x": 2, "y": 1}}})

stl_spec = STL("1 + 1")
stl_eval = stl_spec.eval(time_begin, signal)
print("1 + 1 = " + str(stl_eval))

stl_spec = STL("G[0, 1](x > 3.0)")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value)
print("satisfaction value: " + str(stl_eval.satisfy))
print("robustness value: " + str(stl_eval.robustness))
print()

stl_spec_2 = STL("X[0](x == 2)")
stl_eval_2 = stl_spec_2.eval(time_begin, signal)
print(stl_spec_2.value)
print(stl_eval_2)
print()

signal2 = Signal(py_dict={"0": {"content": {"x": 1, "y": {"z": 2}}}, "1": {"content": {"x": 2, "y": {"z": 1}}}})

stl_spec = STL("G[0, 1](x > y.z)")
stl_eval = stl_spec.eval(time_begin, signal2)
print(stl_spec.value)
print("satisfaction value: " + str(stl_eval.satisfy))
print("robustness value: " + str(stl_eval.robustness))
