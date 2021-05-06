from stl import STL, Signal

# TODO: create a signal and time_begin (like the Interpreter) and evaluate some STL Formulas
time_begin = 0  # global begin time
signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}}, "1": {"content": {"x": 2, "y": 1}}})  # signal to be evaluated
print(signal)

stl_spec = STL("1 + 1")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value, end=" = ")
print(str(stl_eval))
assert stl_eval.value == 2.0
print()

stl_spec = STL("x > 0")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value, end=" = ")
print(str(stl_eval))
assert stl_eval.value == True
print()

stl_spec = STL("0 < x < 1")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value, end=" = ")
print(str(stl_eval))
assert stl_eval.value == False
print()

stl_spec = STL("G[0, 1](0 < x < 1)")
stl_eval = stl_spec.eval(time_begin, signal)
print("satisfaction value: " + str(stl_eval.satisfy))
print("robustness value: " + str(stl_eval.robustness))
print(str(stl_eval))
assert stl_eval.satisfy == False
assert stl_eval.robustness == -1.0
print()

stl_spec = STL("G[0, 1]((x > 0) || (x < 1))")
stl_eval = stl_spec.eval(time_begin, signal)
print("satisfaction value: " + str(stl_eval.satisfy))
print("robustness value: " + str(stl_eval.robustness))
print(str(stl_eval))
assert stl_eval.satisfy == True
assert stl_eval.robustness == 1.0
print()

stl_spec = STL("G[0, 1](x > 3.0)")
stl_eval = stl_spec.eval(time_begin, signal)
print("satisfaction value: " + str(stl_eval.satisfy))
print("robustness value: " + str(stl_eval.robustness))
assert stl_eval.satisfy == False
assert stl_eval.robustness == -2.0
print()

stl_spec = STL("F[0, 1](x > 1.0)")
stl_eval = stl_spec.eval(time_begin, signal)
print("satisfaction value: " + str(stl_eval.satisfy))
#print("robustness value: " + str(stl_eval.robustness))
print(stl_eval.satisfy)
assert stl_eval.satisfy == True
#assert stl_eval.robustness == -2.0
print()

stl_spec = STL("X[0](x == 2)")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value)
print(stl_eval)
assert stl_eval.satisfy == True
assert stl_eval.robustness == 0.0
print()

signal = Signal(py_dict={"0": {"content": {"x": 1, "y": {"z": 2}}}, "1": {"content": {"x": 2, "y": {"z": 1}}}})  # modify the signal to add nested signals
print(signal)

stl_spec = STL("G[0, 1](x > y.z)")
stl_eval = stl_spec.eval(time_begin, signal)
print(stl_spec.value)
print(stl_eval)
assert stl_spec.satisfy(time_begin, signal) == False
assert stl_spec.robustness(time_begin, signal) == -1.0

