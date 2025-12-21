import math

class StereoPanner:
    @staticmethod
    def apply_stereo(channel, s_pos, l_pos, max_dist):
        if not channel: return

        # Задаем значение прямо тут, если его нет в конфиге
        min_audible_volume = 0.1

        dx = s_pos[0] - l_pos[0]
        dy = s_pos[1] - l_pos[1]
        dist = math.sqrt(dx * dx + dy * dy)

        # 1. Если слишком далеко, не выключаем полностью
        if dist >= max_dist:
            channel.set_volume(min_audible_volume)
            return

        # 2. Расчет громкости
        attenuation = 1.0 - (dist / max_dist)

        # Смешиваем затухание с минимальным порогом
        final_volume = max(min_audible_volume, attenuation)

        # 3. Мягкое панорамирование
        pan = dx / (max_dist * 0.8)
        pan = max(-0.7, min(0.7, pan))

        # Баланс каналов
        left = final_volume * (1.0 - pan) / 2.0
        right = final_volume * (1.0 + pan) / 2.0

        channel.set_volume(left, right)