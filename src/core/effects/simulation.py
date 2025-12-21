import random
class EnvironmentalFX:
    @staticmethod
    def get_reverb_params(env_type: str):
        if env_type == "cave": return random.uniform(0.1, 0.2), 0.5
        return None