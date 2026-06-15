# adapted from CONFLUENCE: https://github.com/DarriEy/CONFLUENCE/blob/main/utils/optimization/de_optimizer.py
# The soil depth calibration uses two parameters:
#     - total_mult: Overall depth multiplier (0.1-5.0)
#     - shape_factor: Controls depth profile shape (0.1-3.0)
#       - shape_factor > 1: Deeper layers get proportionally thicker
#       - shape_factor < 1: Shallower layers get proportionally thicker
#       - shape_factor = 1: Uniform scaling
total_mult    | _depth_mult_
shape_factor  | _depth_shpFctr_