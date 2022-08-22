import re
import os
import scipy.io.wavfile as wavfile
import numpy as np

from src.clip_track import ClipTrack
from src.send_track import SendTrack
from src.master_track import MasterTrack

class Board:
  def __init__(self, name='new_board', tracks=None, bpm=120, samplerate=44100):
    if tracks is None:
      tracks = {}
    self.name = name
    self.tracks = tracks
    self.samplerate = samplerate
    if "master" not in self.tracks:
      self.tracks["master"] = MasterTrack("master", samplerate)
    self.bpm = bpm
  
  def format_name(self, name):
    if name in self.tracks:
      number = re.findall(r'\d+', name)
      if len(number) > 0:
        name = name[:-len(str(number[-1]))]
        name += f"{int(number[-1]) + 1}"
      else:
        name += "_1"
    return name

  def add_clip_track(self, name='new_clip_track', clips=None, patches=None, outputs=None):
    if clips is None:
      clips = []
    if patches is None:
      patches = []
    if outputs is None:
      outputs = [self.tracks["master"]]
    name = self.format_name(name)
    new_track = ClipTrack(name, samplerate=self.samplerate, clips=clips, patches=patches, outputs=outputs)
    self.tracks[name] = new_track
    self.tracks["master"].inputs.append(new_track)
    return new_track
  
  def add_send_track(self, name="new_send_track", inputs=None, patches=None, outputs=None):
    if inputs is None:
      inputs = []
    if patches is None:
      patches = []
    if outputs is None:
      outputs = [self.tracks["master"]]
    name = self.format_name(name)
    new_send = SendTrack(name, samplerate=self.samplerate, inputs=inputs, outputs=outputs, patches=patches)
    self.tracks[name] = new_send
    self.tracks["master"].inputs.append(new_send)
    return new_send
  
  def sum(self, length=None):
    return self.tracks["master"].sum(length)
  
  def load_stems(self, song_dir):
    dirs = os.listdir(song_dir)
    tracks = []
    for dir in dirs:
      track_name = dir.split('/')[-1].split('.')[0]
      track = self.add_clip_track(track_name)
      track.add_clip(f"{song_dir}/{dir}")
      tracks.append(track)
    return tracks
  
  def bounce(self, path):
    self.tracks["master"].bounce(path)
  
  def bounce_stems(self, path):
    master = self.tracks["master"]
    for input in master.inputs:
      input.bounce(path)
    
  def quick_load(self, path):
    t = self.add_clip_track()
    t.add_clip(path)
    return t