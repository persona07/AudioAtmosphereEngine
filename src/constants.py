from enum import Enum

class DistributionMode(Enum):
    UNIFORM = "uniform"         # Равномерно
    LINEAR_RISE = "linear_rise" # Нарастание
    LINEAR_FALL = "linear_fall" # Убывание
    PARABOLA = "parabola"       # Парабола

class FadeType(Enum):
    LINEAR = "linear"
    LOGARITHMIC = "logarithmic"
    CUT = "cut"

class SceneTransition(Enum):
    SMOOTH = "smooth"
    CUT = "cut"

DEFAULT_FADE_MS = 2000
HARD_CUT_MS = 20