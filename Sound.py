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

for x in xrange(0, p.get_device_count()):
    if p.get_device_info_by_index(x)['maxOutputChannels'] > max_channels:
        max_channels = p.get_device_info_by_index(x)['maxOutputChannels']

print "Max channels: %s" % max_channels

# define callback (2)
def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        numpy_array = numpy.fromstring(data, 'int16')
        numpy_array = numpy.asarray([numpy.int16(x*volume) for x in numpy_array])
        new_data = numpy_array.tostring()
        return (new_data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    output_device_index=3,
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
