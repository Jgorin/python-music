from src.utils.loaders import load_wav
import numpy as np

class Clip:
  def __init__(self, path, start=0):
    self.path = path
    self.samplerate, self.data = load_wav(path)
    self.length = self.data.shape[0] / self.samplerate
    self.start = start 
    self.end = self.start + self.length
    self.sample_length = self.data.shape[0]
    self.sample_start = int(self.samplerate * self.start)
    self.sample_end = int(self.samplerate * self.end)