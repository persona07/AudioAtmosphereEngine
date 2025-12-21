import pygame
from src.constants import FadeType, HARD_CUT_MS
from src.core.logic.fader import FaderLogic


class AudioLayer:
    def __init__(self, name: str, sound_obj: pygame.mixer.Sound):
        self.name = name
        self.sound = sound_obj
        self.channel = None
        self.target_volume = 1.0
        self.current_volume = 0.0
        self.fade_speed = 1.0
        self.active = False

    def play(self, fade_time_ms=2000):
        if not self.sound: return
        if not self.active:
            self.channel = self.sound.play(loops=-1)
            self.active = True
            self.current_volume = 0.0
            if self.channel:
                self.channel.set_volume(0.0)

        self.target_volume = 1.0
        self.fade_speed = 1.0 / (fade_time_ms / 1000.0) if fade_time_ms > 0 else 100.0

    def stop(self, fade_time_ms=2000, hard_cut=False):
        self.target_volume = 0.0
        if hard_cut:
            fade_time_ms = HARD_CUT_MS
            self.active = False
        self.fade_speed = 1.0 / (fade_time_ms / 1000.0) if fade_time_ms > 0 else 100.0

    def update(self, dt: float):
        if not self.channel: return
        if abs(self.current_volume - self.target_volume) > 0.01:
            step = self.fade_speed * dt
            if self.current_volume < self.target_volume:
                self.current_volume = min(self.target_volume, self.current_volume + step)
            else:
                self.current_volume = max(self.target_volume, self.current_volume - step)

            factor = FaderLogic.get_volume_multiplier(self.current_volume)
            self.channel.set_volume(factor)

        if self.target_volume == 0 and self.current_volume <= 0.01:
            self.channel.stop()
            self.active = False