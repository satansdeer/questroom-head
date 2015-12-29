from __future__ import print_function
from SoundManager import SoundManager

sm = SoundManager()
sm.daemon = True
sm.start()

sm.play_sound('robot_1.wav')

while True:
    pass