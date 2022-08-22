import numpy as np

class Delay:
  def __init__(self, ms):
    self.ms = ms
  
  def apply(self, input, samplerate):
    samples = int((self.ms / 1000) * samplerate)
    out = np.zeros(input.shape)
    out[samples:,:] = input[0:len(input) - samples,:]
    return out
    
    