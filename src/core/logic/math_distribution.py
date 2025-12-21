import random
import math
from src.constants import DistributionMode


class DistributionLogic:
    @staticmethod
    def get_next_value(mode: str, min_v: float, max_v: float) -> float:
        if min_v >= max_v: return min_v

        try:
            m = DistributionMode(mode)
        except ValueError:
            m = DistributionMode.UNIFORM

        if m == DistributionMode.UNIFORM:
            return random.uniform(min_v, max_v)
        elif m == DistributionMode.LINEAR_RISE:
            return min_v + (max_v - min_v) * math.sqrt(random.random())
        elif m == DistributionMode.LINEAR_FALL:
            return min_v + (max_v - min_v) * (1.0 - math.sqrt(random.random()))
        elif m == DistributionMode.PARABOLA:
            r = (random.random() + random.random()) / 2.0
            return min_v + (max_v - min_v) * r

        return random.uniform(min_v, max_v)