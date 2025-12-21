import pygame
import random
from src.core.logic.math_distribution import DistributionLogic
from src.core.resources.asset_manager import AssetManager

class RandomEmitter:
    def __init__(self, config: dict, asset_manager: AssetManager):
        self.file_path = config.get("file")
        self.mode = config.get("mode", "uniform")
        self.min_t = config.get("min", 5.0)
        self.max_t = config.get("max", 15.0)
        self.assets = asset_manager
        self.timer = 0.0
        self.next_trigger = DistributionLogic.get_next_value(self.mode, self.min_t, self.max_t)
        self.sound_obj = self.assets.get_sound(self.file_path)

    def update(self, dt: float):
        if not self.sound_obj: return
        self.timer += dt
        if self.timer >= self.next_trigger:
            self._trigger()
            self.timer = 0.0
            self.next_trigger = DistributionLogic.get_next_value(self.mode, self.min_t, self.max_t)

    def _trigger(self):
        channel = pygame.mixer.find_channel()
        if channel:
            vol = random.uniform(0.85, 1.0)
            channel.set_volume(vol)
            channel.play(self.sound_obj)