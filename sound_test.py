from SoundManager import SoundManager

sm = SoundManager()
sm.daemon = True
sm.start()

sm.play_sound('coin.wav', lambda: sm.play_sound('coin.wav'))

