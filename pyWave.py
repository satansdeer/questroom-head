
import pyaudio, sys
from wavefile import WaveReader

p = pyaudio.PyAudio()
with WaveReader(sys.argv[1]) as r :

    # Print info
    print "Title:", r.metadata.title
    print "Artist:", r.metadata.artist
    print "Channels:", r.channels
    print "Format: 0x%x"%r.format
    print "Sample Rate:", r.samplerate

    # open pyaudio stream
    stream = p.open(
            format = pyaudio.paFloat32,
            channels = r.channels,
            rate = r.samplerate,
            frames_per_buffer = 512,
            output = True)

    # iterator interface (reuses one array)
    # beware of the frame size, not always 512, but 512 at least
    for frame in r.read_iter(size=512) :
        stream.write(frame, frame.shape[1])
        sys.stdout.write("."); sys.stdout.flush()

    stream.close()
