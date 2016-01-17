"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import numpy

wf = wave.open('full_robot.wav', 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

volume = 0.99
max_channels = 0
device_index = 0

print range(0, p.get_device_count())

for x in range(0, p.get_device_count()):
    device = p.get_device_info_by_index(x)
    print '====='
    print device
    print '-----'
    if device['maxOutputChannels'] > max_channels:
        max_channels = device['maxOutputChannels']
        device_index = device['index']

# define callback (2)
def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        numpy_array = numpy.fromstring(data, 'int16')
        numpy_array = numpy.asarray([numpy.int16(x*volume) for x in numpy_array])
        new_data = numpy_array.tostring()
        return (new_data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    channels=min(wf.getnchannels(), max_channels),
    output_device_index=device_index,
    rate=wf.getframerate(),
    output=True,
    stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
        time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
