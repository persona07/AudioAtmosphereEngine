import json
import os
from src.core.errors import ConfigValidationError

class ConfigLoader:
    @staticmethod
    def load(path: str) -> dict:
        if not os.path.exists(path): return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ConfigValidationError(f"JSON Error in {path}: {e}")