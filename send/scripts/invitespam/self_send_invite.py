import os
import random
from datetime import UTC, datetime
from dotenv import load_dotenv

import httpx
from generator import *
from player_pb2 import (
    CreatePlayerRequest,
    UpdatePlayerRequest,
    PlayerResponse,
)

load_dotenv()
identityToken = str(os.environ.get("IDENTITYTOKEN", ""))


api_url = "https://subway.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.46.9"


def auth_register():
    url = api_url + "/v2.0/auth/register"
    with httpx.Client(http2=True) as client:
        r = client.post(url, headers={"Content-Type": "application/json"})
        r.raise_for_status()
        return r.json()


def create_player(authtoken, name):
    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"
    msg = CreatePlayerRequest(
        name=name,
        selected_board="default",
        selected_board_upgrades="default",
        selected_character="jake.default",
        selected_country="de",
        selected_background="default_background",
        selected_frame="default_frame",
        selected_portrait="jake_portrait",
        stat_total_visited_destinations=0,
        stat_total_games=0,
    )
    payload = msg.SerializeToString()
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload
    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }
    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)
    raw = r.content
    if len(raw) < 5:
        raise RuntimeError("CreatePlayer response too short")
    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    resp = PlayerResponse()
    resp.ParseFromString(grpc_payload)
    return resp


def update_player(authtoken, name):
    character = choose_character()
    board, upgrades = choose_board()
    portrait, frame, background = choose_cosmetics()
    country = choose_country()

    url = api_url + "/rpc/player.ext.v1.PrivateService/UpdatePlayer"

    msg = UpdatePlayerRequest(
        name=name,
        level=random.randint(1, 10),
        highscore=random.randint(1, 50000),
        metadata={
            "stat_total_visited_destinations": str(random.randint(1, 80)),
            "stat_total_games": str(random.randint(1, 8000)),
            "stat_owned_characters": str(random.randint(1, 240)),
            "stat_owned_characters_outfits": str(random.randint(1, 214)),
            "stat_owned_boards": str(random.randint(1, 272)),
            "stat_owned_boards_upgrades": str(random.randint(1, 158)),
            "selected_portrait": portrait,
            "selected_frame": frame,
            "selected_country": country,
            "selected_character": character,
            "selected_board": board,
            "selected_board_upgrades": upgrades,
            "selected_background": background,
            "highscore_default": str(random.randint(1, 10000)),
            "stat_achievements": str(random.randint(1, 27)),
            "stat_total_top_run_medals_bronze": str(random.randint(1, 50)),
            "stat_total_top_run_medals_silver": str(random.randint(1, 50)),
            "stat_total_top_run_medals_gold": str(random.randint(1, 50)),
            "stat_total_top_run_medals_diamond": str(random.randint(1, 50)),
            "stat_total_top_run_medals_champion": str(random.randint(1, 50)),
        },
    )

    payload = msg.SerializeToString()
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload
    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }
    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)
    raw = r.content
    if len(raw) < 5:
        raise RuntimeError("CreatePlayer response too short")
    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]
    resp = PlayerResponse()
    resp.ParseFromString(grpc_payload)
    return resp


def send_invite(playeruuid, authtoken):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/SendInvite"
    encoded = playeruuid.encode("utf-8")
    payload = b"\x0a" + len(encoded).to_bytes(1, "big") + encoded
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload
    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }
    with httpx.Client(http2=True) as client:
        r = client.post(url, headers=headers, content=body)
        r.raise_for_status()
    return True


def main(amount: int):
    remaining = amount

    download_missing_files()

    for _ in range(amount):
        try:
            name = generate_name()
            auth = auth_register()
            authtoken = auth.get("idToken")

            player_resp = create_player(authtoken, name)
            playeruuid = player_resp.user_data.uuid
            update_player(authtoken, name)

            send_invite(playeruuid, identityToken)

        except Exception as e:
            print(f"Error: {e}")
            continue

        remaining -= 1
        print(f"Remaining: {remaining}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <amount>")
        exit(1)
    amount = int(sys.argv[1])
    try:
        main(amount)
    except KeyboardInterrupt:
        print("\nExiting on user request.")
        exit(0)
