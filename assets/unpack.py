# https://assets.tower.sybo.net/v1.0/subway/9917a9a0-0de9-40fb-bb80-392ee596f705/bundle/1.0.0/characters-remote_assets_pixeljake_default_outfit_config_7a3d5cbdbef0e42b386ceea8f110c324.bundle

import os
import UnityPy


def unpack_all_assets(source_folder: str, destination_folder: str):
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            env = UnityPy.load(file_path)

            for obj in env.objects:
                try:
                    if obj.type.name not in ["Texture2D", "Sprite"]:
                        continue
                    data = obj.read()
                    name = getattr(data, "name", str(obj.path_id))
                    dest = os.path.join(destination_folder, name)
                    dest, _ = os.path.splitext(dest)
                    dest += ".png"
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    data.image.save(dest)
                except Exception:
                    continue

            for path, obj in env.container.items():
                try:
                    if obj.type.name not in ["Texture2D", "Sprite"]:
                        continue
                    data = obj.read()
                    dest = os.path.join(destination_folder, *path.split("/"))
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    dest, _ = os.path.splitext(dest)
                    dest += ".png"
                    data.image.save(dest)
                except Exception:
                    continue


def main():
    source_folder = "Android"
    destination_folder = "Extracted_Assets"
    os.makedirs(destination_folder, exist_ok=True)
    unpack_all_assets(source_folder, destination_folder)


main()
