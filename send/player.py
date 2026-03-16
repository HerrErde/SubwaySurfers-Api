import httpx
from google.protobuf.field_mask_pb2 import FieldMask

from player_pb2 import *
from utils import *


def get_player_by_tag(playertag: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerByTag"

    msg = GetPlayerByTagRequest(
        tag=playertag,
    )
    body = framing(msg)

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

    try:
        resp = GetPlayerByTagResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player_by_id(playeruuid: str):
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayerById"

    msg = GetPlayerByIdRequest(
        uid=playeruuid,
    )

    body = framing(msg)

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

    try:
        resp = GetPlayerByIdResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())
        print("No valid response received.")


def get_player():
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetPlayer"

    msg = GetPlayerRequest()

    body = framing(msg)

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

    try:
        resp = GetPlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
        # print("payload bytes:", resp.SerializeToString())
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def create_player():
    url = api_url + "/rpc/player.ext.v1.PrivateService/CreatePlayer"

    msg = CreatePlayerRequest(
        name="StylingeDino",
        level=1,
        highscore=1,
        metadata={
            "stat_total_visited_destinations": "1",
            "stat_total_games": "1",
            "stat_owned_characters": "1",
            "stat_owned_characters_outfits": "1",
            "stat_owned_boards": "1",
            "stat_owned_boards_upgrades": "1",
            "stat_achievements": "1",
            "stat_total_top_run_medals_bronze": "1",
            "stat_total_top_run_medals_silver": "1",
            "stat_total_top_run_medals_gold": "1",
            "stat_total_top_run_medals_diamond": "1",
            "stat_total_top_run_medals_champion": "1",
            "selected_character": "jake.default",
            "selected_portrait": "boombox_graffiti_portrait",
            # "selected_frame": "jake_portrait",
            # "selected_background": "default_background",
            # "selected_board_upgrades": "default,trail",
            # "selected_board": "default",
            # "selected_country": "de",
            # "highscore_default": "1",
            "equipped_badge_tier_1": "0",
            "equipped_badge_1": "achievement_03",
        },
    )

    body = framing(msg)

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

    try:
        resp = CreatePlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def update_player():
    url = api_url + "/rpc/player.ext.v1.PrivateService/UpdatePlayer"

    msg = UpdatePlayerRequest(
        name="StylingeDino",
        level=3,
        highscore=1,
        metadata={
            "stat_total_visited_destinations": "1",
            "stat_total_games": "1",
            "stat_owned_characters": "1",
            "stat_owned_characters_outfits": "1",
            "stat_owned_boards": "1",
            "stat_owned_boards_upgrades": "1",
            "stat_achievements": "1",
            "stat_total_top_run_medals_bronze": "1",
            "stat_total_top_run_medals_silver": "1",
            "stat_total_top_run_medals_gold": "1",
            "stat_total_top_run_medals_diamond": "1",
            "stat_total_top_run_medals_champion": "1",
            "selected_character": "jake.default",
            "selected_portrait": "boombox_graffiti_portrait",
            # "selected_frame": "jake_portrait",
            # "selected_background": "default_background",
            # "selected_board_upgrades": "default,trail",
            # "selected_board": "default",
            # "selected_country": "de",
            # "highscore_default": "1",
            "equipped_badge_tier_1": "0",
            "equipped_badge_1": "achievement_03",
        },
        updateMask=FieldMask(paths=["name", "level", "highscore", "metadata"]),
        # player=Player(uid="019cbaf5-b428-7e63-aa49-770c03e5a978"),
    )

    body = framing(msg)

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

    try:
        resp = UpdatePlayerResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
        print("gRPC payload (hex):", grpc_payload.hex())
    except Exception as e:
        print("Failed to parse response:", e)
        print("gRPC payload (hex):", grpc_payload.hex())


def match():
    url = api_url + "/rpc/player.ext.v1.PrivateService/Match"

    msg = MatchRequest()

    body = framing(msg)

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = MatchResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


def get_config():
    url = api_url + "/rpc/player.ext.v1.PrivateService/GetConfig"

    msg = GetConfigRequest()

    body = framing(msg)

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
    elif r.content:
        if "text/html" in r.headers.get("Content-Type"):
            print("Content is html")
            return

    msg_len = int.from_bytes(raw[1:5], "big")
    grpc_payload = raw[5 : 5 + msg_len]

    try:
        resp = GetConfigResponse()
        resp.ParseFromString(grpc_payload)
        print(resp)
    except Exception as e:
        print("Failed to parse response:", e)
        message = r.headers.get("grpc-message")
        print("gRPC message:", message)
        print("gRPC payload (hex):", grpc_payload.hex())


# get_player_by_tag("N99635VZB9NFPD")
# get_player_by_id("fca24390-4e4e-4994-a02a-3aab323129a2")
# create_player()
# update_player()
# get_player()
# match()
get_config()
