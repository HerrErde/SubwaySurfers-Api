import json
import random
import re
from datetime import UTC, datetime
from pathlib import Path

import httpx
from generator import *
from player_pb2 import (
    CreatePlayerRequest,
    UpdatePlayerRequest,
    PlayerResponse,
)

uuid_pattern = re.compile(
    r"\b[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\b"
)
tag_pattern = re.compile(r"^[A-Z0-9]{14}$")

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


def get_player_by_tag(playertag: str, authtoken: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerByTag"
    encoded_playertag = playertag.encode("utf-8")
    protobuf_payload = (
        b"\x0a" + len(encoded_playertag).to_bytes(1, "big") + encoded_playertag
    )

    prefix = b"\x00" + len(protobuf_payload).to_bytes(4, "big")
    body = prefix + protobuf_payload

    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return False, None

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = PlayerResponse()
        resp.ParseFromString(grpc_payload)
        uuid = resp.userdata.uuid
        return True, uuid
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        return False, None


def get_player_by_id(playerid: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerById"

    encoded_playerid = playerid.encode("utf-8")
    protobuf_payload = (
        b"\x0a" + len(encoded_playerid).to_bytes(1, "big") + encoded_playerid
    )

    prefix = b"\x00" + len(protobuf_payload).to_bytes(4, "big")
    body = prefix + protobuf_payload

    headers = {
        "User-Agent": user_agent,
        "grpc-accept-encoding": "identity,gzip",
        "Authorization": f"Bearer {authtoken}",
        "Content-Type": "application/grpc-web",
    }

    with httpx.Client(http2=True) as client:
        r = client.post(
            url,
            headers=headers,
            content=body,
        )

    raw = r.content

    if len(raw) < 5:
        print("Response too short")
        return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    resp = PlayerResponse()
    resp.ParseFromString(grpc_payload)
    uuid = resp.userdata.uuid
    return True, uuid


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


def main(friend_tag: str, amount: int):
    if not (tag_pattern.match(friend_tag) or uuid_pattern.match(friend_tag)):
        raise ValueError("Invalid player tag format.")

    is_uuid = uuid_pattern.match(friend_tag) is not None
    created = []
    remaining = amount

    download_missing_files()

    for _ in range(amount):
        try:
            name = generate_name()
            auth = auth_register()
            authtoken = auth.get("idToken")
            refresh_token = auth.get("refreshToken")

            player_resp = create_player(authtoken, name)
            update_player(authtoken, name)

            if is_uuid:
                playeruuid = friend_tag
            else:
                success, playeruuid = get_player_by_tag(friend_tag, authtoken)
                if not success:
                    print(f"Failed to get UUID for tag {friend_tag}")
                    continue

            success = send_invite(playeruuid, authtoken)

            created.append(
                {
                    "name": name,
                    "uuid": playeruuid,
                    "created": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                    "idToken": authtoken,
                    "refreshToken": refresh_token,
                    "friendInviteSent": success,
                }
            )
        except Exception as e:
            print(f"Error: {e}")
            continue

        remaining -= 1
        print(f"Remaining: {remaining}")

    # print(json.dumps(created, indent=2))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script.py <player_tag/player_uuid> <amount>")
        exit(1)
    friend_tag = sys.argv[1]
    amount = int(sys.argv[2])
    try:
        main(friend_tag, amount)
    except KeyboardInterrupt:
        print("\nExiting on user request.")
        exit(0)
