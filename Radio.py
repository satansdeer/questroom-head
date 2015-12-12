from __future__ import print_function
import threading
import time
import pygame
import sys

class Radio(threading.Thread):

    def __init__(self, step, tick):
        pygame.mixer.init()
        self.value = 0
        self.target_value = 20
        self.last_time_clock = 0
        self.step = step
        self.tick = tick
        self.noize_sound = pygame.mixer.Sound('noize.wav')
        super(Radio, self).__init__()

    def set_target_value(self, target_value):
        self.target_value = target_value

    def init_sounds(self, sound_descriptions, noize_name):
        self.sounds = map(lambda desc: pygame.mixer.Sound(desc[0]), sound_descriptions)
        self.ranges = map(lambda desc: desc[1::], sound_descriptions)
        first_values = [value[0] for value in self.ranges]
        second_values = [value[1] for value in self.ranges]
        self.negative_ranges = [(0, first_values[0])] + zip(second_values, first_values[1::])
        self.play_sounds()


    def play_sounds(self):
        self.noize_sound.play(-1)
        for sound in self.sounds:
            sound.play(-1)
            sound.set_volume(1)


    def update_sounds_volumes(self, value):
        for range_id, sound_range in enumerate(self.negative_ranges):
            if sound_range[0] <= value <= sound_range[1]:
                self.calculate_sound_volume(value, sound_range, range_id)


    def calculate_sound_volume(self, value, sound_range, range_id):
        range_diff = float(sound_range[1]) - float(sound_range[0])
        diff_half = range_diff/2
        value_in_range = float(value) - float(sound_range[0])
        one_percent = diff_half / 100
        if value_in_range < diff_half:
            percents = value_in_range / one_percent
            snd_id = range_id - 1
            if snd_id < 0:
                first_sound = self.noize_sound
            else:
                first_sound = self.sounds[snd_id]
            second_sound = self.noize_sound
        else:
            percents = (value_in_range - diff_half) / one_percent
            first_sound = self.noize_sound
            second_sound = self.sounds[range_id]

        for sound in self.sounds:
            sound.set_volume(0)

        first_sound.set_volume(1-percents/100)
        second_sound.set_volume(percents/100)


    def run(self):
        while True:
            clock = time.clock()
            if (clock - self.last_time_clock) < self.tick:
                continue
            if abs(self.target_value - self.value) <= self.step:
                continue
            if self.value < self.target_value:
                self.value += self.step
                self.update_sounds_volumes(self.value)
            elif self.value > self.target_value:
                self.value -= self.step
                self.update_sounds_volumes(self.value)
            self.last_time_clock = time.clock()



