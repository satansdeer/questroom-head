import pyaudio
import wave
import time
import sys
import numpy
from fractions import Fraction
import threading

def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
    return run

class Sound:

    CHUNK = 1024

    def __init__(self, sound_name):
        self.sound_name = sound_name
        self.wf = wave.open(sound_name, 'rb')
        self.p = pyaudio.PyAudio()
        self._volume = 1
        self.device_index, self.max_channels = self.get_valid_device_info(self.p)


    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        numpy_array = numpy.fromstring(data, 'int16') * self._volume
        new_data = numpy_array.astype('int16').tostring()
        return (new_data, pyaudio.paContinue)


    def open_stream(self):
        stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=min(self.wf.getnchannels(), self.max_channels),
            output_device_index=1,
            rate=self.wf.getframerate(),
            output=True)
        return stream


    @run_in_thread
    def play(self, repeat_count = 1):
        stream = self.open_stream()
        stream.start_stream()
        while repeat_count != 0:
            repeat_count -= 1
            data = self.wf.readframes(self.CHUNK)
            while data != '':
                stream.write(data)
                data = self.wf.readframes(self.CHUNK)

            self.wf.rewind()
            data = self.wf.readframes(self.CHUNK)

        stream.stop_stream()
        stream.close()
        self.wf.close()
        self.p.terminate()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        self._volume_fraction = Fraction(self._volume).limit_denominator()

    def get_valid_device_info(self, p):
        max_channels = 0
        device_index = 0
        for x in range(0, p.get_device_count()):
            device = p.get_device_info_by_index(x)
            if device['maxOutputChannels'] > max_channels:
                max_channels = device['maxOutputChannels']
                device_index = device['index']
        return (device_index, max_channels)
