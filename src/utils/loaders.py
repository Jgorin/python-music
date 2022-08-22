import scipy.io.wavfile as wavfile
import numpy as np

def load_wav(file):
  samplerate, data = wavfile.read(file)
  if data.dtype == np.int32:
    data = np.divide(data, 2**31)
  elif data.dtype == np.int16:
    data = np.divide(data, 2**15)
  elif data.dtype == np.uint8:
    data = np.divide(data, 2**8)
  else:
    raise Exception(f"Format {data.dtype} from file {file} not supported.")
  # if mono convert to stereo
  if len(data.shape) == 1:
    data = np.expand_dims(data, axis=1)
    data = np.append(data, data, axis=1)
  return samplerate, data
