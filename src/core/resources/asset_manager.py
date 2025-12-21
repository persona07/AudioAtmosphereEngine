import pygame
import os

class AssetManager:
    def __init__(self):
        self._cache = {}

    def get_sound(self, path: str):
        if path in self._cache: return self._cache[path]
        if not os.path.exists(path):
            # print(f"[AssetManager] Missing: {path}") # Uncomment for debug
            return None
        try:
            sound = pygame.mixer.Sound(path)
            self._cache[path] = sound
            return sound
        except Exception as e:
            print(f"[AssetManager] Error {path}: {e}")
            return None