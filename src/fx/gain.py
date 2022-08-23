from src.utils.math import decibels_to_gain
from src.utils.math import gain_to_decibels

class Gain:
  def __init__(self, input=0.0, mode="decibels"):
    self.set_gain(input, mode)
  
  def apply(self, input, samplerate):
    print(input.shape)
    return input * self.gain
  
  def set_gain(self, input, mode="decibels"):
    if mode == "decibels":
      self.gain = decibels_to_gain(input)
    elif mode == "amplitude":
      self.gain = input
    else:
      raise Exception("Mode {mode} is not supported...")
