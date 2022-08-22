import numpy as np
from src.utils.math import inverse_lerp, lerp

class Panpot:
  def __init__(self, left=-90, right=90):
    self.left = left
    self.right = right
  
  def apply(self, input, samplerate):
    left_interp = inverse_lerp(90, -90, self.left)
    right_interp = inverse_lerp(-90, 90, self.right)
    res = np.zeros(input.shape)
    res[:,0] = input[:,0] * left_interp + input[:,1] * (1 - right_interp)
    res[:,1] = input[:,0] * (1 - left_interp) + input[:,1] * right_interp
    return res