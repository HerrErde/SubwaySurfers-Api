import json
import random
import os
import requests


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "names.json")) as f:
    NAMES_DATA = json.load(f)

with open(os.path.join(BASE_DIR, "boards_data.json")) as f:
    BOARDS = json.load(f)

with open(os.path.join(BASE_DIR, "characters_data.json")) as f:
    CHARACTERS = json.load(f)

with open(os.path.join(BASE_DIR, "playerprofile_data.json")) as f:
    PROFILE_DATA = json.load(f)

with open(os.path.join(BASE_DIR, "country_iso.txt")) as f:
    ISO_CODES = [line.strip() for line in f if line.strip()]


def generate_name():
    return (
        f"{random.choice(NAMES_DATA['adjectives'])}{random.choice(NAMES_DATA['names'])}"
    )


def choose_board():
    board = random.choice(BOARDS)
    board_id = board["id"]
    upgrades = board.get("upgrades", [])

    if not upgrades:
        upgrade_str = "default"
    else:
        chosen_upgrades = random.sample(upgrades, k=random.randint(0, len(upgrades)))
        upgrade_str = (
            ",".join(upg["id"] for upg in chosen_upgrades)
            if chosen_upgrades
            else "default"
        )

    return board_id, upgrade_str


def choose_character():
    character = random.choice(CHARACTERS)
    char_id = character["id"]
    outfits = character.get("outfits", [])

    outfit_id = random.choice(outfits)["id"] if outfits else "default"
    return f"{char_id}.{outfit_id}"


def choose_cosmetics():
    portraits = PROFILE_DATA.get("profilePortraits", ["default_portrait"])
    frames = PROFILE_DATA.get("profileFrames", ["default_frame"])
    backgrounds = PROFILE_DATA.get("profileBackgrounds", ["default_background"])

    return (random.choice(portraits), random.choice(frames), random.choice(backgrounds))


def choose_country():
    return random.choice(ISO_CODES)


FILES = ["boards_data.json", "characters_data.json", "playerprofile_data.json"]

BASE_URL = "https://github.com/HerrErde/subway-source/releases/latest/download/"


def download_missing_files():
    for file in FILES:
        file_path = os.path.join(BASE_DIR, file)
        if not os.path.exists(file_path):
            url = f"{BASE_URL}{file}"
            print(f"Downloading {file} from {url}...")
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Saved {file} to {file_path}")
            else:
                print(f"Failed to download {file}: HTTP {response.status_code}")


if __name__ == "__main__":
    download_missing_files()
    board, upgrades = choose_board()
    character = choose_character()
    portrait, frame, background = choose_cosmetics()
    country = choose_country()
