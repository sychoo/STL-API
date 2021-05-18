from stl import STL, Signal

time_begin = 0  # global begin time
signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}},
                         "1": {"content": {"x": 2, "y": 1}}})

#stl_spec = STL("G[0, 1](0 < x < 1)")
stl_eval = stl_spec.eval(time_begin, signal)

print()
#print("original STL expr: ")
#print(stl_spec)

print()
weakened_stl = stl_spec.weaken("ap-range", 2, 3)
#print(weakened_stl_spec_ap_range_1)
# G[0, 1](0-2 < x < 1+3)

# G[0, 1](-2 < x < 4)

print(weakened_stl.eval(time_begin, signal))
