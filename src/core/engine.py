import os
from src.constants import SceneTransition, DEFAULT_FADE_MS, HARD_CUT_MS
from src.core.mixer_wrapper import MixerWrapper
from src.core.resources.asset_manager import AssetManager
from src.core.resources.config_loader import ConfigLoader
from src.components.layer import AudioLayer
from src.components.emitter import RandomEmitter
from src.components.listener import AudioListener

class AudioEngine:
    def __init__(self, config_path, assets_root):
        MixerWrapper.initialize()
        self.assets_root = assets_root
        self.assets = AssetManager()
        self.config = ConfigLoader.load(config_path)
        self.listener = AudioListener()
        self.active_layers = {}
        self.active_emitters = []
        self.current_scene = None

    def _get_full_path(self, local_path):
        return os.path.join(self.assets_root, local_path)

    def set_scene(self, location, variant, transition="smooth"):
        key = f"{location}_{variant}"
        print(f"[Engine] Switching to {key} ({transition})")

        loc_data = self.config.get("locations", {}).get(location, {}).get(variant)
        if not loc_data:
            print(f"[Engine] Scenario not found: {key}")
            return

        is_cut = (transition == SceneTransition.CUT.value)
        fade_time = HARD_CUT_MS if is_cut else DEFAULT_FADE_MS

        target_loops = set(loc_data.get("loops", []))
        current_loops = set(self.active_layers.keys())

        # Stop old
        for fname in current_loops - target_loops:
            self.active_layers[fname].stop(fade_time_ms=fade_time, hard_cut=is_cut)

        # Start new
        for fname in target_loops - current_loops:
            full_path = self._get_full_path(fname)
            sound = self.assets.get_sound(full_path)
            if sound:
                layer = AudioLayer(fname, sound)
                layer.play(fade_time_ms=fade_time)
                self.active_layers[fname] = layer
            elif fname in self.active_layers:
                self.active_layers[fname].target_volume = 1.0

        # Emitters
        self.active_emitters = []
        for em_conf in loc_data.get("emitters", []):
            conf_copy = em_conf.copy()
            conf_copy["file"] = self._get_full_path(em_conf["file"])
            self.assets.get_sound(conf_copy["file"]) # Preload
            self.active_emitters.append(RandomEmitter(conf_copy, self.assets))

        self.current_scene = key

    def update(self, dt):
        dead_layers = [k for k, v in self.active_layers.items() if not v.active and v.current_volume <= 0.01]
        for k in dead_layers: del self.active_layers[k]

        for layer in self.active_layers.values(): layer.update(dt)
        for emitter in self.active_emitters: emitter.update(dt)

    def set_listener_pos(self, x, y):
        self.listener.set_position(x, y)