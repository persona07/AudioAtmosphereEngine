import os


def print_debug_stats(engine):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"=== SCENE: {engine.current_scene} ===")

    print("\n--- Active Layers ---")
    for name, layer in engine.active_layers.items():
        status = "PLAY" if layer.active else "STOPPING"
        print(f"[{status}] {name} | Vol: {layer.current_volume:.2f}")

    print("\n--- Active Emitters ---")
    print(f"Count: {len(engine.active_emitters)}")