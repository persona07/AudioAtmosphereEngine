import random
import math


class DistributionLogic:
    @staticmethod
    def get_next_interval(mode: str, min_t: float, max_t: float) -> float:
        if mode == "uniform":
            # Равномерное распределение
            return random.uniform(min_t, max_t)

        elif mode == "linear_rise":
            # Линейное нарастание: вероятность выше ближе к концу интервала.
            # Формула: min + (diff) * sqrt(random)
            return min_t + (max_t - min_t) * math.sqrt(random.random())

        elif mode == "linear_fall":
            # Линейное убывание: вероятность выше в начале интервала.
            # Формула: min + (diff) * (1 - sqrt(random))
            return min_t + (max_t - min_t) * (1.0 - math.sqrt(random.random()))

        elif mode == "parabola":
            # Парабола, события чаще всего происходят в середине интервала.
            # Используем среднее арифметическое двух случайных чисел.
            rand_factor = (random.random() + random.random()) / 2.0
            return min_t + (max_t - min_t) * rand_factor

        else:
            # Дефолт
            return random.uniform(min_t, max_t)