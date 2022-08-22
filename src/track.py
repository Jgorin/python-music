import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import os
from src.fx.gain import Gain
from src.fx.panpot import Panpot

class Track():
  def __init__(self, name, samplerate, fx):
    self.name = name
    self.samplerate = samplerate
    if len(fx) == 0 or type(fx[-2]) != Gain:
      fx.append(Gain())
    if len(fx) == 1 or type(fx[-1]) != Panpot:
      fx.append(Panpot())
    self.fx = fx
  
  def get_sample_length(self, tracks):
    return 0 if len(tracks) == 0 else max([o.sample_end for o in tracks])
  
  def repeat(self, function, inputs, length=None):
    if length is not None:
      length *= self.samplerate
    else:
      length = self.get_sample_length(inputs)
    res = np.zeros((length, 2))
    for input in inputs:
      function(res, input)
    return res
  
  def bounce(self, path):
    assert self.sum is not None, "Track must contain a definition for sum."
    sum = self.sum()
    full_path = f"{os.getcwd()}/{path}"
    local_path = f"{path}/{self.name}.wav"
    if len(sum) == 0:
      return
    if not os.path.exists(full_path):
      os.makedirs(full_path)
    wavfile.write(local_path, self.samplerate, (sum * 2**15).astype(np.int16))
  
  def apply_fx(self, input):
    res = input
    for f in self.fx:
      res = f.apply(res, self.samplerate)
    return res
  
  def set_volume(self, input, mode="decibels"):
    self.fx[-2].set_gain(input, mode)
  
  def plot(self, sum):
    y1 = []
    y2 = []
    x = []
    for sample in sum:
      x.append(len(x))
      y1.append(sample[0] + 1)
      y2.append(sample[1])
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()
