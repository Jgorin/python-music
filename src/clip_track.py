from src.clip import Clip
from src.track import Track
from src.patch import Patch
import numpy as np

class ClipTrack(Track):
  def __init__(self, name='new_track', samplerate=44100, clips=None, patches=None, outputs=None, fx=None):
    if clips is None:
      clips = []
    if patches is None:
      patches = []
    if outputs is None:
      outputs = []
    if fx is None:
      fx = []
    self.clips = clips
    self.outputs = outputs
    self.patches = patches
    self.sample_end = 0 if len(self.clips) == 0 else max([c.sample_end for c in self.clips])
    super().__init__(name, samplerate, fx)
  
  def add_clip(self, path, start=0):
    new_clip = Clip(path, start)
    self.clips.append(new_clip)
    if new_clip.sample_end > self.sample_end:
      self.sample_end = new_clip.sample_end
    return new_clip
  
  def add_patch(self, send, volume=0.0, mode="decibels"):
    patch = Patch(self, send, volume, mode)
    send.inputs.append(patch)
    self.patches.append(patch)
    return patch
  
  def add_output(self, out):
    out.inputs.append(self)
    self.outputs.append(out)
    
  def remove_output(self, out):
    out.inputs.remove(self)
    self.outputs.remove(out)
    
  def sum(self, length=None):
    def f(res, input):
      res[input.sample_start:input.sample_end,:] = input.data[:length]
    return super().apply_fx(self.repeat(f, self.clips, length))
  
  def plot(self):
    sum = self.sum()
    super().plot(sum)