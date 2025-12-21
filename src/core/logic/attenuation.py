class AttenuationLogic:

    @staticmethod
    def calculate_volume(current_dist: float, min_dist: float, max_dist: float, model="linear") -> float:

    #current_dist: Расстояние от игрока до источника
    #min_dist: Дистанция, где звук слышен на 100% (радиус источника)
    #max_dist: Дистанция, где звук полностью исчезает

        if current_dist <= min_dist:
            return 1.0
        if current_dist >= max_dist:
            return 0.0

        # Нормализованное расстояние (от 0.0 у min_dist до 1.0 у max_dist)
        distance_fraction = (current_dist - min_dist) / (max_dist - min_dist)

        if model == "linear":
            # Линейный спад.
            return 1.0 - distance_fraction

        elif model == "exponential":
            #  (1 - x)^2
            val = 1.0 - distance_fraction
            return val * val

        elif model == "step":
            # Ступенчатый
            if distance_fraction < 0.5:
                return 1.0
            elif distance_fraction < 0.8:
                return 0.5
            else:
                return 0.0

        return 1.0 - distance_fraction