# 2021-05-06 13:49:49
from stl import STL, Signal

time_begin = 0  # global begin time
signal = Signal(py_dict={"0": {"content": {"x": 1, "y": 2}}, "1": {
                "content": {"x": 2, "y": 1}}})  # signal to be evaluated
print(signal)

# {
#     "0": {
#         "content": {
#             "x": 1,
#             "y": 2
#         }
#     },
#     "1": {
#         "content": {
#             "x": 2,
#             "y": 1
#         }
#     }
# }



# print("satisfaction value: " + str(stl_eval.satisfy))
# print("robustness value: " + str(stl_eval.robustness))
# print(str(stl_eval))


# ap-range will automatically decide which side to weaken based on the sign
# stl_eval = weakened_stl_spec_ap_range_1.eval(time_begin, signal)

# ap-range
# (x, y) <chained comp expr range weakening)
# (x) <single-sided range weakening)

# time-range
# (x, y) <chained comp expr range weakening)

stl_spec = STL("G[0, 1](0 < x < 1)")
stl_eval = stl_spec.eval(time_begin, signal)
weakened_stl_spec_ap_range_1 = stl_spec.weaken("ap-range", 2, 3)
# G[0, 1](0-2 < x < 1+3)
# G[0, 1](-2 < x < 4)

stl_spec = STL("G[0, 1](x < 1)")
stl_eval = stl_spec.eval(time_begin, signal)
weakened_stl_spec_ap_range_2 = stl_spec.weaken("ap-range", 2)
# G[0, 1](x < 1+2)
# G[0, 1](x < 3)

stl_spec = STL("G[0, 1](x > 0)")
stl_eval = stl_spec.eval(time_begin, signal)
weakened_stl_spec_ap_range_3 = stl_spec.weaken("ap-range", 3)
# G[0, 1](x > 0-3)
# G[0, 1](x > -3)

stl_spec = STL("G[0, 1](0 < x < 1)")
stl_eval = stl_spec.eval(time_begin, signal)
weakened_stl_spec_time_range_1 = stl_spec.weaken("time-range", 2, 3)
# G[0-2, 1+3](0 < x < 1)
# G[-2, 4](0 < x < 1)

# print(str(stl_eval))

print()

print("original STL: ")
print(stl_spec)

print("weakened ap-range-1 STL: ")
print(weakened_stl_spec_ap_range_1)

print("weakened ap-range-2 STL: ")
print(weakened_stl_spec_ap_range_2)

print("weakened ap-range-3 STL: ")
print(weakened_stl_spec_ap_range_3)

# TODO
# - check conformity of chained expr

print("weakened time-range-1 STL: ")
print(weakened_stl_spec_time_range_1)
# TODO
# - check validity of time bound
