import math

def decibels_to_gain(db):
  return math.pow(10, db / 20)

def gain_to_decibels(gain):
  return 10 * math.log10(gain)

def lerp(a, b, v):
  return a + ((b - a) * v)

def inverse_lerp(a, b, v):
  return (v - a) / (b - a)