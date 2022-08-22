from src.board import Board
from src.fx.delay import Delay
import os
import numpy as np

# sample rate is 48k
song_path = f"{os.getcwd()}/test/data/song1"

board = Board(name="demo", samplerate=44100)
master = board.tracks["master"]
# tracks = board.load_stems(f"{song_path}/stems")
track = board.quick_load("/Users/josh/personal/python_music/stereo_test.wav")

delay = board.add_send_track("delay")
track.add_patch(delay, -10)
track.remove_output(master)

# t1 = board.quick_load("/Users/josh/personal/python_music/stereo_test.wav")
# delay_send = board.add_send_track("delay")
# delay_send.set_volume(-10)
# delay_send.fx.append(Delay(200))

# t1.add_send(delay_send)

board.bounce_stems("bounces/delay_stems")