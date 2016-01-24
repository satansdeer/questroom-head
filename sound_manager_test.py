from SoundManager import *
import time

sm = SoundManager()
sm.daemon = True
sm.start()

sm.play_sound('coin.wav')
