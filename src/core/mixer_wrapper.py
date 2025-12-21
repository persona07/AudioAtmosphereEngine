import pygame

class MixerWrapper:
    @staticmethod
    def initialize(freq=44100, buffer=512, channels=64):
        if pygame.mixer.get_init(): return
        pygame.mixer.pre_init(freq, -16, 2, buffer)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(channels)
        pygame.mixer.set_reserved(8)