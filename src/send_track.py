from src.track import Track
from src.patch import Patch
import numpy as np

class SendTrack(Track):
  def __init__(self, name="new_send", samplerate=44100, inputs=None, patches=None, outputs=None, fx=None):
    if inputs is None:
      inputs = []
    if patches is None:
      patches = []
    if outputs is None:
      outputs = []
    if fx is None:
      fx = []
    self.inputs = inputs
    self.patches = patches
    self.outputs = outputs
    self.sample_end = 0 if len(inputs) == 0 else max([c.sample_end for c in inputs])
    super().__init__(name, samplerate, fx)
  
  def get_send_sample_length(self):
    end = 0
    for input in self.inputs:
      if type(input) == Patch:
        sample_end = input.input.sample_end
      else:
        sample_end = input.sample_end
      if sample_end > end:
        end = sample_end
    return end
  
  def sum(self, length=None):
    if length is None:
      length = int(self.get_send_sample_length() / self.samplerate)
    def f(res, input):
      breakpoint()
      res += input.sum(length * self.samplerate)
    return super().apply_fx(self.repeat(f, self.inputs, length))

  def add_input(self, input):
    input.output.append(self)
    self.inputs.append(input)
  
  def add_patch(self, send, volume=0.0, mode="decibels"):
    patch = Patch(self, send, volume, mode)
    send.inputs.append(patch)
    self.patches.append(patch)
    return patch

  def remove_input(self, input):
    input.output.remove(self)
    self.inputs.remove(input)
  
  def plot(self):
    sum = self.sum()
    super().plot(sum)