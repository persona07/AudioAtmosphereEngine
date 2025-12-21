import threading
import time
import json

from src.core.engine import AudioEngine

CONFIG_PATH = "assets/configs/scenarios.json"
ASSETS_ROOT = "assets/audio/"
MAX_HEARING_DIST = 100.0  # Дистанция, на которой звук пропадает

# Глобальные переменные
GLOBAL_STATE = {
    "running": True,  # Работает ли программа
    "current_dist": 0.0,  # Текущая дистанция до центра локации
    "target_location": None,  # Какую локацию включить
    "target_variant": None
}


def audio_thread_func():
    print("[Audio Thread] Started.")

    engine = AudioEngine(CONFIG_PATH, ASSETS_ROOT)

    # Запускаем первую сцену по умолчанию
    first_loc = list(engine.config["locations"].keys())[0]
    first_var = list(engine.config["locations"][first_loc].keys())[0]

    engine.set_scene(first_loc, first_var, "cut")

    current_loc_key = first_loc

    # Бесконечный цикл обновления звука
    while GLOBAL_STATE["running"]:
        start_time = time.time()

        # А. Проверка смены локации
        if GLOBAL_STATE["target_location"] and GLOBAL_STATE["target_location"] != current_loc_key:
            new_loc = GLOBAL_STATE["target_location"]
            new_var = GLOBAL_STATE["target_variant"]
            engine.set_scene(new_loc, new_var, "smooth")
            current_loc_key = new_loc
            GLOBAL_STATE["target_location"] = None  # Сброс команды

        # Расчет громкости от дистанции
        dist = GLOBAL_STATE["current_dist"]

        # Формула затухания (0.0 - 1.0)
        volume_factor = 1.0 - (dist / MAX_HEARING_DIST)
        volume_factor = max(0.0, min(1.0, volume_factor))
        volume_factor = volume_factor * volume_factor  # Квадратичное


        for layer in engine.active_layers.values():
            # Если слой активен, его базовая громкость 1.0
            if layer.channel:
                # Берем текущую громкость фейда и умножаем на дистанцию
                final_vol = layer.current_volume * volume_factor
                layer.channel.set_volume(final_vol)

        # Эмиттеры работают только если мы слышим локацию
        if volume_factor > 0.05:
            engine.update(0.05)
        time.sleep(0.05)

    print("[Audio Thread] Stopped.")


def main():
    print("--- CONSOLE AUDIO CONTROLLER ---")

    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)

    available_maps = {}

    print("\n[ID] LOCATION NAME")
    i = 1
    for loc, variants in data["locations"].items():
        for var in variants.keys():
            # Создаем короткое имя для удобства
            key = loc.split('_')[0]
            print(f" {key:<12} -> {loc} ({var})")
            available_maps[key] = (loc, var)
            i += 1
    print("-" * 40)

    t = threading.Thread(target=audio_thread_func)
    t.start()

    print("\nCOMMANDS:")
    print(" [name] [dist]  -> Change location & distance (e.g., 'forest 0', 'bunker 50')")
    print(" [dist]         -> Change only distance (e.g., '20')")
    print(" list           -> Show locations")
    print(" q              -> Quit")

    try:
        while True:
            user_input = input("\n> ").strip().lower()

            if user_input == 'q':
                break

            if user_input == 'list':
                print(list(available_maps.keys()))
                continue

            parts = user_input.split()

            try:
                if len(parts) == 1 and parts[0].isdigit():
                    dist = float(parts[0])
                    GLOBAL_STATE["current_dist"] = dist
                    print(f" >> Distance set to {dist}m")

                elif len(parts) >= 2:
                    name_key = parts[0]
                    dist = float(parts[1])

                    # Ищем полное название
                    found = None
                    for k, val in available_maps.items():
                        if name_key in k or name_key in val[0]:
                            found = val
                            break

                    if found:
                        GLOBAL_STATE["target_location"] = found[0]
                        GLOBAL_STATE["target_variant"] = found[1]
                        GLOBAL_STATE["current_dist"] = dist
                        print(f" >> Moving to {found[0]} at {dist}m...")
                    else:
                        print("Location not found")

                else:
                    print("Invalid format. Use: 'forest 10' or just '10'")

            except ValueError:
                print("Distance must be a number")

    except KeyboardInterrupt:
        pass
    finally:
        # Корректное завершение
        GLOBAL_STATE["running"] = False
        t.join()  # Ждем завершения аудио потока
        print("Bye.")


if __name__ == "__main__":
    main()