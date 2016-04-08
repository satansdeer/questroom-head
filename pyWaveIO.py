
"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
from wavefile import WaveReader

CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = WaveReader(sys.argv[1])

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=pyaudio.paFloat32,
                channels=wf.channels,
                rate=wf.samplerate,
                frames_per_buffer = 512,
                output=True)

# read data
# data = wf.read(CHUNK)

# play stream (3)
for data in wf.read_iter(size=512) :
# while len(data[0]) > 0:
    stream.write(data, data.shape[1])
    # data = wf.read(CHUNK)

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()
