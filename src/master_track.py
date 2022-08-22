from src.track import Track
import numpy as np

class MasterTrack(Track):
  def __init__(self, name='master', samplerate=44100, inputs=None, fx=None):
    if inputs is None:
      inputs = []
    if fx is None:
      fx = []
    self.inputs = inputs
    super().__init__(name, samplerate, fx)
  
  def sum(self, length=None): 
    def f(res, input):
      data = input.sum(length)
      res[:data.shape[0]] += data
    return super().apply_fx(self.repeat(f, self.inputs, length))
  
  def plot(self):
    sum = self.sum()
    super().plot(sum)