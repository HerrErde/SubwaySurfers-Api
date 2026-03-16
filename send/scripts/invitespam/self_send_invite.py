import os
import random

import httpx
from dotenv import load_dotenv
from generator import *
from player_pb2 import *

load_dotenv()
identityToken = str(os.environ.get("IDENTITYTOKEN", ""))

api_url = "https://subway.prod.sybo.net"
user_agent = "grpc-dotnet/2.63.0 (Mono Unity; CLR 4.0.30319.17020; netstandard2.0; arm64) com.kiloo.subwaysurf/3.46.9"


def framing(msg):
    payload = msg.SerializeToString()

    # gRPC-Web framing
    body = b"\x00" + len(payload).to_bytes(4, "big") + payload

    return body


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
    )

    body = framing(msg)

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
    resp = CreatePlayerResponse()
    resp.ParseFromString(grpc_payload)
    return resp


def update_player(authtoken, name):
    character, character_length, outfits_length = choose_character()
    board, upgrades, board_length, upgrades_length = choose_board()
    portrait, frame, background = choose_cosmetics()
    country = choose_country()
    achievements = achievements_length()

    url = api_url + "/rpc/player.ext.v1.PrivateService/UpdatePlayer"

    msg = UpdatePlayerRequest(
        name=name,
        level=random.randint(1, 10),
        highscore=random.randint(1, 50000),
        metadata={
            "stat_total_visited_destinations": str(random.randint(1, 80)),
            "stat_total_games": str(random.randint(1, 8000)),
            "stat_owned_characters": str(random.randint(1, character_length)),
            "stat_owned_characters_outfits": str(random.randint(1, outfits_length)),
            "stat_owned_boards": str(random.randint(1, board_length)),
            "stat_owned_boards_upgrades": str(
                random.randint(1, max(1, upgrades_length))
            ),
            "selected_portrait": portrait,
            "selected_frame": frame,
            "selected_country": country,
            "selected_character": character,
            "selected_board": board,
            "selected_board_upgrades": upgrades,
            "selected_background": background,
            "highscore_default": str(random.randint(1, 10000)),
            "stat_achievements": str(random.randint(1, achievements)),
            "stat_total_top_run_medals_bronze": str(random.randint(1, 50)),
            "stat_total_top_run_medals_silver": str(random.randint(1, 50)),
            "stat_total_top_run_medals_gold": str(random.randint(1, 50)),
            "stat_total_top_run_medals_diamond": str(random.randint(1, 50)),
            "stat_total_top_run_medals_champion": str(random.randint(1, 50)),
        },
    )

    body = framing(msg)

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
    resp = UpdatePlayerResponse()
    resp.ParseFromString(grpc_payload)
    return resp


def send_invite(authtoken, playeruuid):
    url = api_url + "/rpc/friends.ext.v1.PrivateService/SendInvite"

    msg = SendInviteRequest(
        userId=playeruuid,
    )

    body = framing(msg)

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
            update_player(authtoken, name)

            playeruuid = player_resp.player.uid
            send_invite(identityToken, playeruuid)

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
