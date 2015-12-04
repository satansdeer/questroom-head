import pygame
from Getch import getch

pygame.mixer.init()
sounda = pygame.mixer.Sound("1.wav")
soundb = pygame.mixer.Sound("test.wav")
soundb.set_volume(0)

sounda.play(-1)
soundb.play(-1)

VOLUME_STEP = 0.03
volume = 1

while True:
    char = getch()
    if char == '1':
        volume += VOLUME_STEP
        sounda.set_volume(volume)
        soundb.set_volume(1-volume)
        print sounda.get_volume()
    else:
        volume -= VOLUME_STEP
        sounda.set_volume(volume)
        soundb.set_volume(1-volume)
        print sounda.get_volume()

