class FaderLogic:
    @staticmethod
    def get_volume_multiplier(progress: float, curve_type="logarithmic") -> float:
        t = max(0.0, min(1.0, progress))
        if curve_type == "linear": return t
        elif curve_type == "logarithmic": return t * t
        return t