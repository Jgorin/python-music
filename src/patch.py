from src.fx.gain import Gain

class Patch:
  def __init__(self, input, output, volume=0.0, mode="decibels"):
    self.input = input
    self.output = output
    self.fader = Gain(volume, mode)
  
  def set_volume(self, volume=0.0, mode="decibels"):
    self.fader.set_gain(volume, mode)
  
  def sum(self, length=None):
    return self.fader.apply(self.input.sum(length=length), self.input.samplerate)
  
  def remove(self):
    self.input.patches.remove(self)
    self.output.inputs.remove(self)